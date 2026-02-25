from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from ..database import Base


class KnowledgeBase(Base):
    """知识库模型"""

    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    category = Column(String(50), nullable=False, comment="知识分类")
    title = Column(String(200), nullable=False, comment="知识标题")
    content = Column(Text, nullable=False, comment="知识内容")
    keywords = Column(String(255), nullable=True, comment="关键词")
    source = Column(String(200), nullable=True, comment="来源")
    is_active = Column(Integer, nullable=False, default=1, comment="是否启用：0/1")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

    def __repr__(self):
        return f"<KnowledgeBase(id={self.id}, title={self.title})>"
