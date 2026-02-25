from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class DialogueBase(BaseModel):
    """对话基础 Schema"""
    user_message: str = Field(..., description="用户消息")
    message_type: str = Field(default="consultation", description="消息类型")


class DialogueCreate(DialogueBase):
    """创建对话请求"""
    patient_id: int = Field(..., gt=0, description="患者 ID")
    session_id: str = Field(..., max_length=64, description="会话 ID")


class DialogueResponse(DialogueBase):
    """对话响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    session_id: str
    ai_response: str
    is_handover: bool
    created_at: datetime
