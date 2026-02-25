from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class KnowledgeBaseBase(BaseModel):
    """知识库基础 Schema"""
    category: str = Field(..., max_length=50, description="知识分类")
    title: str = Field(..., max_length=200, description="知识标题")
    content: str = Field(..., description="知识内容")
    keywords: Optional[str] = Field(None, max_length=255, description="关键词")
    source: Optional[str] = Field(None, max_length=200, description="来源")


class KnowledgeBaseCreate(KnowledgeBaseBase):
    """创建知识请求"""
    is_active: bool = True


class KnowledgeBaseUpdate(BaseModel):
    """更新知识请求"""
    category: Optional[str] = Field(None, max_length=50)
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    keywords: Optional[str] = Field(None, max_length=255)
    source: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None


class KnowledgeBaseResponse(KnowledgeBaseBase):
    """知识响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
