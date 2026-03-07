"""
API 客户端模块
封装与 FastAPI 后端的通信
"""
import requests
from typing import Optional, Dict, Any, List

# 后端 API 地址
BASE_URL = "http://localhost:8000/api"


class APIClient:
    """FastAPI 后端 API 客户端"""
    
    BASE_URL = BASE_URL  # 导出 BASE_URL 常量
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _request(self, method: str, url: str, **kwargs) -> Any:
        """通用请求方法"""
        kwargs["headers"] = kwargs.get("headers", {})
        kwargs["headers"].update(self.headers)

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            # 204 No Content 没有返回值
            if response.status_code == 204:
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败：{str(e)}")

    # ==================== 认证相关 ====================

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """用户登录"""
        data = {"username": username, "password": password}
        result = self._request("POST", f"{BASE_URL}/auth/login", data=data)
        if "access_token" in result:
            self.token = result["access_token"]
            self.headers["Authorization"] = f"Bearer {self.token}"
        return result

    def get_current_user(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self._request("GET", f"{BASE_URL}/auth/me")

    # ==================== 患者管理 ====================

    def get_patients(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取患者列表"""
        # 后端使用 skip/limit 参数，需要转换
        skip = (page - 1) * page_size
        params = {"skip": skip, "limit": page_size}
        return self._request("GET", f"{BASE_URL}/patients/", params=params)

    def get_patient(self, patient_id: int) -> Dict[str, Any]:
        """获取患者详情"""
        return self._request("GET", f"{BASE_URL}/patients/{patient_id}")

    def create_patient(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建患者"""
        return self._request("POST", f"{BASE_URL}/patients/", json=data)

    def update_patient(self, patient_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新患者"""
        return self._request("PUT", f"{BASE_URL}/patients/{patient_id}", json=data)

    def delete_patient(self, patient_id: int) -> Dict[str, Any]:
        """删除患者"""
        return self._request("DELETE", f"{BASE_URL}/patients/{patient_id}")

    # ==================== 复诊管理 ====================

    def get_appointments(self, page: int = 1, page_size: int = 20,
                         status: Optional[str] = None) -> Dict[str, Any]:
        """获取复诊计划列表"""
        # 后端使用 skip/limit 参数
        skip = (page - 1) * page_size
        params = {"skip": skip, "limit": page_size}
        if status:
            params["status"] = status
        return self._request("GET", f"{BASE_URL}/appointments/", params=params)

    def get_appointment(self, appointment_id: int) -> Dict[str, Any]:
        """获取复诊详情"""
        return self._request("GET", f"{BASE_URL}/appointments/{appointment_id}")

    def create_appointment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建复诊计划"""
        return self._request("POST", f"{BASE_URL}/appointments/", json=data)

    def update_appointment(self, appointment_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新复诊计划"""
        return self._request("PUT", f"{BASE_URL}/appointments/{appointment_id}", json=data)

    def delete_appointment(self, appointment_id: int) -> Dict[str, Any]:
        """删除复诊计划"""
        return self._request("DELETE", f"{BASE_URL}/appointments/{appointment_id}")

    def update_appointment_status(self, appointment_id: int, status: str) -> Dict[str, Any]:
        """更新复诊状态"""
        data = {"status": status}
        return self._request("PATCH", f"{BASE_URL}/appointments/{appointment_id}/status", json=data)

    # ==================== 对话管理 ====================

    def get_dialogues(self, page: int = 1, page_size: int = 20,
                      patient_id: Optional[int] = None) -> Dict[str, Any]:
        """获取对话记录列表"""
        # 后端使用 skip/limit 参数
        skip = (page - 1) * page_size
        params = {"skip": skip, "limit": page_size}
        if patient_id:
            params["patient_id"] = patient_id
        return self._request("GET", f"{BASE_URL}/dialogues/", params=params)

    def get_dialogue_session(self, session_id: str) -> Dict[str, Any]:
        """获取会话历史"""
        return self._request("GET", f"{BASE_URL}/dialogues/session/{session_id}")

    def handover_dialogue(self, dialogue_id: int, reason: str) -> Dict[str, Any]:
        """标记人工接管"""
        data = {"reason": reason}
        return self._request("POST", f"{BASE_URL}/dialogues/{dialogue_id}/handover", json=data)

    def get_handover_pending(self) -> Dict[str, Any]:
        """获取待人工接管对话"""
        return self._request("GET", f"{BASE_URL}/dialogues/handover/pending")

    # ==================== 知识库 ====================

    def get_knowledge(self, page: int = 1, page_size: int = 20,
                      category: Optional[str] = None) -> Dict[str, Any]:
        """获取知识库列表"""
        params = {"page": page, "page_size": page_size}
        if category:
            params["category"] = category
        return self._request("GET", f"{BASE_URL}/knowledge/", params=params)

    def get_knowledge_item(self, knowledge_id: int) -> Dict[str, Any]:
        """获取知识详情"""
        return self._request("GET", f"{BASE_URL}/knowledge/{knowledge_id}")

    def create_knowledge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建知识条目"""
        return self._request("POST", f"{BASE_URL}/knowledge/", json=data)

    def update_knowledge(self, knowledge_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新知识条目"""
        return self._request("PUT", f"{BASE_URL}/knowledge/{knowledge_id}", json=data)

    def delete_knowledge(self, knowledge_id: int) -> Optional[Dict[str, Any]]:
        """删除知识条目"""
        try:
            response = requests.request(
                "DELETE",
                f"{BASE_URL}/knowledge/{knowledge_id}",
                headers=self.headers
            )
            response.raise_for_status()
            # 204 No Content 没有返回值
            return None
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败：{str(e)}")

    def get_knowledge_categories(self) -> List[str]:
        """获取分类列表"""
        return self._request("GET", f"{BASE_URL}/knowledge/categories")

    # ==================== 统计接口 ====================

    def get_stats_overview(self) -> Dict[str, Any]:
        """获取概览统计"""
        return self._request("GET", f"{BASE_URL}/stats/overview")

    def get_appointments_trend(self, days: int = 7) -> Dict[str, Any]:
        """获取复诊趋势"""
        params = {"days": days}
        return self._request("GET", f"{BASE_URL}/stats/appointments/trend", params=params)

    def get_dialogues_daily(self, days: int = 7) -> Dict[str, Any]:
        """获取对话统计"""
        params = {"days": days}
        return self._request("GET", f"{BASE_URL}/stats/dialogues/daily", params=params)

    def get_patients_gender(self) -> Dict[str, Any]:
        """获取患者性别分布"""
        return self._request("GET", f"{BASE_URL}/stats/patients/gender")

    def get_appointments_status(self) -> Dict[str, Any]:
        """获取复诊状态分布"""
        return self._request("GET", f"{BASE_URL}/stats/appointments/status")


# 全局客户端实例
_api_client: Optional[APIClient] = None


def get_api_client(token: Optional[str] = None) -> APIClient:
    """获取 API 客户端实例"""
    global _api_client
    if _api_client is None or token:
        _api_client = APIClient(token)
    return _api_client
