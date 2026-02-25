from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PatientBase(BaseModel):
    """患者基础 Schema"""
    name: str = Field(..., max_length=50, description="姓名")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    age: Optional[int] = Field(None, ge=0, le=150, description="年龄")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    medical_history: Optional[str] = Field(None, description="既往病史")
    allergy_history: Optional[str] = Field(None, description="过敏史")


class PatientCreate(PatientBase):
    """创建患者请求"""
    openid: str = Field(..., max_length=64, description="微信用户标识")


class PatientUpdate(BaseModel):
    """更新患者请求"""
    name: Optional[str] = Field(None, max_length=50)
    gender: Optional[str] = Field(None, max_length=10)
    age: Optional[int] = Field(None, ge=0, le=150)
    phone: Optional[str] = Field(None, max_length=20)
    medical_history: Optional[str] = None
    allergy_history: Optional[str] = None


class PatientResponse(PatientBase):
    """患者响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    openid: str
    created_at: datetime
    updated_at: datetime
