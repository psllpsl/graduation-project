from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from ..database import Base


class SystemConfig(Base):
    """系统配置模型"""

    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    config_key = Column(String(100), unique=True, nullable=False, comment="配置键")
    config_value = Column(Text, nullable=False, comment="配置值")
    description = Column(String(255), nullable=True, comment="配置说明")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

    def __repr__(self):
        return f"<SystemConfig(id={self.id}, key={self.config_key})>"
