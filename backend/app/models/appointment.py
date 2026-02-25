from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Appointment(Base):
    """复诊计划模型"""

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, comment="患者 ID")
    appointment_date = Column(DateTime, nullable=False, comment="复诊日期")
    appointment_type = Column(String(50), nullable=False, comment="复诊类型")
    status = Column(String(20), nullable=False, default="pending", comment="状态：pending/completed/cancelled")
    reminder_sent = Column(Integer, nullable=False, default=0, comment="是否已发送提醒：0/1")
    reminder_time = Column(DateTime, nullable=True, comment="提醒发送时间")
    notes = Column(Text, nullable=True, comment="复诊备注")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

    # 关联关系
    patient = relationship("Patient", back_populates="appointments")

    def __repr__(self):
        return f"<Appointment(id={self.id}, patient_id={self.patient_id})>"
