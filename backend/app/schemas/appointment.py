from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal


class AppointmentBase(BaseModel):
    """复诊计划基础 Schema"""
    appointment_date: datetime = Field(..., description="复诊日期时间")
    appointment_type: str = Field(..., max_length=50, description="复诊类型")
    notes: Optional[str] = Field(None, description="复诊备注")


class AppointmentCreate(AppointmentBase):
    """创建复诊计划请求"""
    patient_id: int = Field(..., gt=0, description="患者 ID")


class AppointmentUpdate(BaseModel):
    """更新复诊计划请求"""
    appointment_date: Optional[datetime] = None
    appointment_type: Optional[str] = Field(None, max_length=50)
    status: Optional[Literal["pending", "completed", "cancelled"]] = None
    notes: Optional[str] = None


class AppointmentResponse(AppointmentBase):
    """复诊计划响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    status: str
    reminder_sent: bool
    reminder_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
