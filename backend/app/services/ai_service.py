import httpx
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from ..models.knowledge_base import KnowledgeBase
from ..config import settings
from ..utils.redis_cache import cache


class AIService:
    """
    AI 智能客服服务类
    负责与大模型 API 交互，实现对话生成
    """

    def __init__(self):
        """
        初始化 AI 服务
        """
        self.api_url = settings.AI_SERVICE_URL
        self.max_tokens = settings.AI_MAX_TOKENS
        self.temperature = settings.AI_TEMPERATURE

    def generate_response(
        self,
        user_message: str,
        context: Optional[str] = None,
        knowledge: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> str:
        """
        生成 AI 回复

        Args:
            user_message: 用户消息
            context: 对话上下文
            knowledge: 相关知识片段
            session_id: 会话 ID

        Returns:
            AI 回复内容
        """
        # 构建 System Prompt
        system_prompt = self._build_system_prompt(knowledge)

        # 构建用户消息
        if context:
            user_prompt = f"对话历史：\n{context}\n\n用户问题：{user_message}"
        else:
            user_prompt = user_message

        # 如果有配置的 AI 服务地址，调用 API
        if self.api_url:
            return self._call_llm_api(system_prompt, user_prompt)

        # 否则返回默认回复
        return self._get_default_response(user_message)

    def _build_system_prompt(self, knowledge: Optional[List[str]] = None) -> str:
        """
        构建 System Prompt

        Args:
            knowledge: 相关知识片段

        Returns:
            System Prompt 字符串
        """
        base_prompt = """你是一名专业的牙科修复 AI 智能客服助手。你的职责是：
1. 为患者提供牙科修复术后的专业指导和咨询
2. 回答关于复诊时间、术后护理、注意事项等问题
3. 语气友好、专业、易懂，体现关怀
4. 对于紧急情况（如剧烈疼痛、大量出血），建议立即就医
5. 不提供诊断，只提供一般性建议

请根据以下知识内容回答用户问题："""

        if knowledge:
            knowledge_text = "\n".join([f"- {k}" for k in knowledge])
            return f"{base_prompt}\n\n{knowledge_text}"

        return base_prompt

    def _call_llm_api(self, system_prompt: str, user_prompt: str) -> str:
        """
        调用大模型 API

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户消息

        Returns:
            AI 回复内容
        """
        try:
            with httpx.Client(timeout=30.0) as client:
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
            print(f"AI API call error: {e}")
            return "抱歉，系统暂时无法连接 AI 服务，请稍后再试。"

    def _get_default_response(self, user_message: str) -> str:
        """
        获取默认回复（用于没有配置 AI 服务时）

        Args:
            user_message: 用户消息

        Returns:
            默认回复内容
        """
        # 简单的关键词匹配回复
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

    def search_knowledge(self, db: Session, query: str, limit: int = 3) -> List[str]:
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

        # 从数据库查询
        keywords = query.split()
        results = []

        for keyword in keywords:
            items = db.query(KnowledgeBase).filter(
                KnowledgeBase.is_active == 1,
                KnowledgeBase.content.like(f"%{keyword}%")
            ).limit(limit).all()

            for item in items:
                if item.content not in results:
                    results.append(item.content)

        # 缓存结果（30 分钟）
        from datetime import timedelta
        cache.set(cache_key, results, expire=timedelta(minutes=30))

        return results[:5]


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
