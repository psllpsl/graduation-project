from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Dialogue(Base):
    """对话记录模型"""

    __tablename__ = "dialogues"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 ID")
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, comment="患者 ID")
    session_id = Column(String(64), nullable=False, comment="会话 ID")
    user_message = Column(Text, nullable=False, comment="用户消息")
    ai_response = Column(Text, nullable=False, comment="AI 回复")
    message_type = Column(String(20), nullable=False, default="consultation", comment="消息类型")
    is_handover = Column(Integer, nullable=False, default=0, comment="是否人工接管：0/1")
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="对话时间")

    # 关联关系
    patient = relationship("Patient", back_populates="dialogues")

    def __repr__(self):
        return f"<Dialogue(id={self.id}, session_id={self.session_id})>"
