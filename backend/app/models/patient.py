from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Patient(Base):
    """患者模型"""

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    openid = Column(String(64), unique=True, nullable=False, comment="微信用户标识")
    name = Column(String(50), nullable=False, comment="姓名")
    gender = Column(String(10), nullable=True, comment="性别")
    age = Column(Integer, nullable=True, comment="年龄")
    phone = Column(String(20), nullable=True, index=True, comment="手机号")
    id_card = Column(String(18), nullable=True, comment="身份证号")
    medical_history = Column(Text, nullable=True, comment="既往病史")
    allergy_history = Column(Text, nullable=True, comment="过敏史")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="注册时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

    # 关联关系
    treatment_records = relationship("TreatmentRecord", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    dialogues = relationship("Dialogue", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.name})>"
