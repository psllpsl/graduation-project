from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class TreatmentRecord(Base):
    """治疗记录模型"""

    __tablename__ = "treatment_records"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, comment="患者 ID")
    treatment_type = Column(String(50), nullable=False, comment="治疗类型")
    treatment_date = Column(Date, nullable=False, comment="治疗日期")
    tooth_position = Column(String(50), nullable=True, comment="牙位")
    material = Column(String(100), nullable=True, comment="修复材料")
    dentist_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="医生 ID")
    notes = Column(Text, nullable=True, comment="治疗备注")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")

    # 关联关系
    patient = relationship("Patient", back_populates="treatment_records")
    dentist = relationship("User", back_populates="treatment_records")

    def __repr__(self):
        return f"<TreatmentRecord(id={self.id}, patient_id={self.patient_id})>"
