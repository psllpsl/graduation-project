import httpx
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from ..models.knowledge_base import KnowledgeBase
from ..config import settings
from ..utils.redis_cache import cache
import logging

logger = logging.getLogger(__name__)


class AIService:
    """
    AI 智能客服服务类
    负责与大模型 API 交互，实现对话生成
    支持 AutoDL 部署的 Qwen2.5 模型
    """

    def __init__(self):
        """
        初始化 AI 服务
        """
        self.api_url = settings.AI_SERVICE_URL
        self.service_type = settings.AI_SERVICE_TYPE
        self.max_tokens = settings.AI_MAX_TOKENS
        self.temperature = settings.AI_TEMPERATURE
        self.timeout = settings.AI_TIMEOUT_SECONDS

    def generate_response(
        self,
        user_message: str,
        patient_id: Optional[int] = None,
        session_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> str:
        """
        生成 AI 回复

        Args:
            user_message: 用户消息
            patient_id: 患者 ID（用于获取病史等信息）
            session_id: 会话 ID（用于获取对话历史）
            db: 数据库会话（用于检索知识库）

        Returns:
            AI 回复内容
        """
        # 1. 获取对话历史（从数据库）
        context = self._get_session_context(session_id, db, max_turns=3)
        
        # 2. 获取患者信息（如果有）
        patient_info = self._get_patient_info(patient_id, db)
        
        # 3. 检索相关知识（从数据库）
        knowledge = []
        if db:
            knowledge = self.search_knowledge(db, user_message, limit=3)
        
        # 4. 构建 System Prompt
        system_prompt = self._build_system_prompt(knowledge, patient_info)
        
        # 5. 调用 AI 服务
        if self.api_url and self.service_type == "autodl":
            return self._call_autodl_api(user_message, system_prompt, context)
        elif self.api_url:
            return self._call_llm_api(system_prompt, user_message)
        else:
            return self._get_fallback_response(user_message, knowledge)

    def _call_autodl_api(self, user_message: str, system_prompt: str, context: str) -> str:
        """
        调用 AutoDL 部署的 Qwen2.5 推理服务
        """
        try:
            # 构建完整的用户输入（包含对话历史）
            if context:
                full_prompt = f"{context}\n\n用户：{user_message}"
            else:
                full_prompt = user_message

            # 添加强制约束指令
            constraint = """
（注意：回答必须简短，80 字以内，不要追问问题，不要使用标题和分点格式）"""

            # 确保 API URL 以 /generate 结尾
            api_url = self.api_url
            if not api_url.endswith("/generate"):
                api_url = api_url.rstrip("/") + "/generate"

            logger.info(f"Calling AutoDL API: {api_url}")
            logger.info(f"Request data: prompt={full_prompt[:50]}..., max_tokens={self.max_tokens}")

            with httpx.Client(timeout=self.timeout, verify=False) as client:
                response = client.post(
                    api_url,
                    json={
                        "prompt": full_prompt + constraint,
                        "system_prompt": system_prompt,
                        "max_tokens": self.max_tokens,
                        "temperature": 0.5
                    }
                )
                
                logger.info(f"Response status: {response.status_code}")
                
                if response.status_code == 404:
                    logger.error(f"404 Error - URL may be incorrect. Current URL: {api_url}")
                    logger.error(f"Base URL from settings: {self.api_url}")
                
                response.raise_for_status()
                result = response.json()
                logger.info(f"Response JSON keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")

                text = result.get("text", "")
                if text:
                    # 后处理：截断过长回复
                    return self._post_process_response(text)
                return self._get_fallback_response(user_message)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error: {e}")
            logger.error(f"Response content: {e.response.text if hasattr(e.response, 'text') else 'N/A'}")
            return self._get_fallback_response(user_message)
        except httpx.RequestError as e:
            logger.error(f"Request Error: {e}")
            return self._get_fallback_response(user_message)
        except Exception as e:
            logger.error(f"AutoDL API error: {e}")
            return self._get_fallback_response(user_message)

    def _post_process_response(self, text: str) -> str:
        """
        后处理 AI 回复：截断过长内容，移除追问
        """
        import re
        
        # 1. 检测结束场景（用户说谢谢/好的等），强制返回简短回复
        if any(kw in text.lower() for kw in ['谢谢', '感谢', '不客气']):
            # 如果 AI 开始追问，直接截断
            if '请问' in text:
                idx = text.find('请问')
                if idx > 0:
                    text = text[:idx].strip()
                    # 加上结束语
                    if not text.endswith(('。', '！', '！')):
                        text += '。'
                    text += ' 祝您早日康复！'
                    return text
        
        # 2. 如果回复太长，截断到 120 字
        if len(text) > 120:
            for punct in ['。', '！', '？']:
                idx = text.find(punct, 60)
                if idx > 0:
                    text = text[:idx+1]
                    break
            else:
                text = text[:100] + "..."
        
        # 3. 移除追问（以"请问"开头的句子及之后所有内容）
        if '请问' in text:
            idx = text.find('请问')
            text = text[:idx].strip()
        
        # 4. 移除标题格式（【xxx】）
        text = re.sub(r'[\n]*【[^】]+】[\n]*', '\n', text)
        
        # 5. 移除序号（1. 2. 3.）
        text = re.sub(r'\n\d+\.', '.', text)
        
        # 6. 移除分点符号（- xxx）
        text = re.sub(r'\n-', '，', text)
        
        # 7. 清理多余换行
        text = re.sub(r'\n{2,}', '\n', text)
        
        return text.strip()

    def _call_llm_api(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用大模型 API（通用格式）

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户消息

        Returns:
            AI 回复内容
        """
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    self.api_url,
                    json={
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result.get("response", result.get("choices", [{}])[0].get("message", {}).get("content", "抱歉，我暂时无法回答您的问题。"))
        except Exception as e:
            logger.error(f"AI API call error: {e}")
            return "抱歉，系统暂时无法连接 AI 服务，请稍后再试。"

    def _build_system_prompt(self, knowledge: Optional[List[str]] = None, patient_info: Optional[Dict] = None) -> str:
        """
        构建 System Prompt

        Args:
            knowledge: 相关知识片段
            patient_info: 患者信息

        Returns:
            System Prompt 字符串
        """
        base_prompt = """你是一名专业的牙科修复 AI 智能客服助手。

【回答格式要求 - 必须遵守】
1. 字数：严格控制在 80-120 字以内
2. 格式：使用简单段落，不要用标题、分点、序号
3. 风格：像医生面对面说话一样自然
4. 结尾：不要追问"请问您..."，直接给出建议即可

【对话结束识别】
当用户说"谢谢/好的/知道了/没事了"等，礼貌告别即可，如："不客气，祝您早日康复！"

【安全原则】
1. 紧急情况（剧烈疼痛、大量出血）→ 建议立即就医
2. 不提供诊断，只给一般性建议
3. 个体差异建议咨询主治医生"""

        # 添加知识片段（精简版）
        if knowledge:
            knowledge_text = knowledge[0][:200]
            base_prompt += f"\n\n【参考】{knowledge_text}"

        # 添加患者信息
        if patient_info:
            if patient_info.get('allergy_history') and patient_info['allergy_history'] != '无':
                base_prompt += f"\n\n【过敏】{patient_info['allergy_history']}"

        return base_prompt

    def _get_session_context(self, session_id: Optional[str], db: Optional[Session] = None, max_turns: int = 3) -> str:
        """
        从数据库获取会话历史上下文（不依赖 Redis）
        
        Args:
            session_id: 会话 ID
            db: 数据库会话
            max_turns: 最大保留多少轮对话
            
        Returns:
            格式化的对话历史字符串
        """
        if not session_id or not db:
            return ""
        
        from ..models.dialogue import Dialogue
        
        # 从数据库查询最近 N 轮对话
        dialogues = db.query(Dialogue).filter(
            Dialogue.session_id == session_id
        ).order_by(Dialogue.created_at.desc()).limit(max_turns).all()
        
        if not dialogues:
            return ""
        
        # 反转顺序（从旧到新）
        dialogues = list(reversed(dialogues))
        
        # 格式化为对话历史
        context_parts = []
        for d in dialogues:
            context_parts.append(f"用户：{d.user_message}")
            context_parts.append(f"AI: {d.ai_response}")
        
        return "\n".join(context_parts)

    def _get_patient_info(self, patient_id: Optional[int], db: Optional[Session]) -> Optional[Dict]:
        """
        获取患者信息（用于个性化回复）
        
        Args:
            patient_id: 患者 ID
            db: 数据库会话
            
        Returns:
            患者信息字典
        """
        if not patient_id or not db:
            return None
        
        from ..models.patient import Patient
        
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            return None
        
        return {
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "medical_history": patient.medical_history,
            "allergy_history": patient.allergy_history
        }

    def search_knowledge(self, db: Session, query: str, limit: int = 5) -> List[str]:
        """
        检索相关知识

        Args:
            db: 数据库会话
            query: 查询关键词
            limit: 返回数量限制

        Returns:
            知识内容列表
        """
        # 从缓存中查找
        cache_key = f"knowledge_search:{query}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        # 从数据库查询（多字段匹配）
        keywords = [k for k in query.split() if len(k) >= 2]  # 过滤单字
        results = []
        seen_titles = set()

        for keyword in keywords:
            items = db.query(KnowledgeBase).filter(
                KnowledgeBase.is_active == 1,
                (KnowledgeBase.content.like(f"%{keyword}%")) |
                (KnowledgeBase.title.like(f"%{keyword}%")) |
                (KnowledgeBase.keywords.like(f"%{keyword}%"))
            ).order_by(KnowledgeBase.created_at.desc()).limit(limit).all()

            for item in items:
                if item.title not in seen_titles:
                    results.append(item.content)
                    seen_titles.add(item.title)

        # 缓存结果（30 分钟）
        from datetime import timedelta
        cache.set(cache_key, results, expire=timedelta(minutes=30))

        return results[:limit]

    def _get_fallback_response(self, user_message: str, knowledge: Optional[List[str]] = None) -> str:
        """
        获取默认回复（用于 AI 服务不可用时）
        """
        if knowledge:
            return f"根据相关知识：\n{knowledge[0]}\n\n建议您咨询主治医生获取个性化指导。"
        
        # 关键词匹配回复
        if "复诊" in user_message:
            return "关于复诊时间，建议您按照医生嘱咐的时间前来复查。一般情况下：\n- 种植牙术后 7 天拆线\n- 种植牙术后 3-6 个月进行二期手术\n- 固定义齿戴牙后 1 周、1 个月、3 个月复查\n- 活动义齿初戴后 1 周、1 个月复查\n\n具体时间请以您的主治医生安排为准。"
        elif "疼" in user_message or "痛" in user_message:
            return "术后轻微疼痛是正常现象，一般 3-5 天会逐渐缓解。建议您：\n1. 按医嘱服用止痛药\n2. 避免用手术侧咀嚼\n3. 保持口腔清洁\n\n如果疼痛剧烈或持续加重，请及时联系医生或前来就诊。"
        elif "出血" in user_message:
            return "术后 24 小时内少量渗血是正常现象。建议您：\n1. 轻咬纱布 30-60 分钟止血\n2. 避免频繁吐口水或吮吸伤口\n3. 不要吃太烫的食物\n\n如果出血不止或出血量大，请立即就医。"
        elif "刷牙" in user_message or "漱口" in user_message:
            return "术后口腔清洁建议：\n1. 术后 24 小时内不要刷牙，可用医生开的漱口水轻轻漱口\n2. 24 小时后可正常刷牙，但避开手术区域\n3. 饭后用温盐水或漱口水漱口，保持口腔清洁"
        elif "吃" in user_message or "饮食" in user_message:
            return "术后饮食建议：\n1. 术后 2 小时内不要进食\n2. 术后 1 周内吃温凉软食，避免用手术侧咀嚼\n3. 1 个月后可逐渐恢复正常饮食\n4. 避免过硬、过烫、辛辣刺激的食物"
        else:
            return "感谢您的咨询。关于牙科修复术后护理，建议您：\n1. 严格遵照医嘱服药\n2. 保持口腔清洁\n3. 按时复诊\n4. 如有不适及时联系医生\n\n请问还有什么可以帮助您的？"


# 创建全局 AI 服务实例
_ai_service_instance: Optional[AIService] = None


def get_ai_service() -> AIService:
    """
    获取 AI 服务实例

    Returns:
        AI 服务实例
    """
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
