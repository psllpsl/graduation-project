from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础 Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    real_name: str = Field(..., max_length=50, description="真实姓名")
    role: str = Field(default="doctor", description="角色：admin/doctor")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


class UserCreate(UserBase):
    """创建用户请求"""
    password: str = Field(..., min_length=6, description="密码")


class UserUpdate(BaseModel):
    """更新用户请求"""
    real_name: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    role: Optional[str] = Field(None)


class UserResponse(UserBase):
    """用户响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserInDB(UserResponse):
    """数据库用户（含密码）"""
    password_hash: str


class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None
