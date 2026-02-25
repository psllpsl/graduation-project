from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class SystemConfigBase(BaseModel):
    """系统配置基础 Schema"""
    config_key: str = Field(..., max_length=100, description="配置键")
    config_value: str = Field(..., description="配置值")
    description: Optional[str] = Field(None, max_length=255, description="配置说明")


class SystemConfigCreate(SystemConfigBase):
    """创建系统配置请求"""
    pass


class SystemConfigUpdate(BaseModel):
    """更新系统配置请求"""
    config_value: Optional[str] = None
    description: Optional[str] = Field(None, max_length=255)


class SystemConfigResponse(SystemConfigBase):
    """系统配置响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
