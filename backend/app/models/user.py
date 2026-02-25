from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    """用户模型（医护人员）"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="加密密码")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    role = Column(String(20), nullable=False, default="doctor", comment="角色：admin/doctor")
    phone = Column(String(20), nullable=True, comment="手机号")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

    # 关联关系
    treatment_records = relationship("TreatmentRecord", back_populates="dentist")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
