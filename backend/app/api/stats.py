from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from ..database import get_db
from ..dependencies import get_current_user
from ..models.user import User
from ..models.patient import Patient
from ..models.appointment import Appointment
from ..models.dialogue import Dialogue

router = APIRouter()


@router.get("/overview", summary="获取概览统计数据")
async def get_overview_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取系统概览统计数据
    """
    # 患者总数
    total_patients = db.query(func.count(Patient.id)).scalar()

    # 复诊计划总数
    total_appointments = db.query(func.count(Appointment.id)).scalar()

    # 待复诊数量
    pending_appointments = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "pending"
    ).scalar()

    # 对话总数
    total_dialogues = db.query(func.count(Dialogue.id)).scalar()

    # 人工接管数量
    handover_count = db.query(func.count(Dialogue.id)).filter(
        Dialogue.is_handover == 1
    ).scalar()

    return {
        "total_patients": total_patients,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
        "total_dialogues": total_dialogues,
        "handover_count": handover_count
    }


@router.get("/appointments/trend", summary="获取复诊趋势统计")
async def get_appointments_trend(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取最近 N 天的复诊趋势
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 按日期统计复诊数量
    results = db.query(
        func.date(Appointment.appointment_date).label("date"),
        func.count(Appointment.id).label("count")
    ).filter(
        Appointment.appointment_date >= start_date,
        Appointment.appointment_date <= end_date
    ).group_by(
        func.date(Appointment.appointment_date)
    ).all()

    return [
        {"date": str(r.date), "count": r.count}
        for r in results
    ]


@router.get("/dialogues/daily", summary="获取每日对话统计")
async def get_daily_dialogues(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取最近 N 天的对话统计
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    results = db.query(
        func.date(Dialogue.created_at).label("date"),
        func.count(Dialogue.id).label("count")
    ).filter(
        Dialogue.created_at >= start_date
    ).group_by(
        func.date(Dialogue.created_at)
    ).all()

    return [
        {"date": str(r.date), "count": r.count}
        for r in results
    ]


@router.get("/patients/gender", summary="获取患者性别分布")
async def get_patient_gender_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取患者性别分布统计
    """
    results = db.query(
        Patient.gender,
        func.count(Patient.id).label("count")
    ).group_by(Patient.gender).all()

    return [
        {"gender": r.gender or "未知", "count": r.count}
        for r in results
    ]


@router.get("/appointments/status", summary="获取复诊状态分布")
async def get_appointment_status_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取复诊状态分布统计
    """
    results = db.query(
        Appointment.status,
        func.count(Appointment.id).label("count")
    ).group_by(Appointment.status).all()

    return [
        {"status": r.status, "count": r.count}
        for r in results
    ]


@router.get("/dialogues/types", summary="获取对话类型统计")
async def get_dialogue_types_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取对话类型分布统计
    """
    results = db.query(
        Dialogue.message_type,
        func.count(Dialogue.id).label("count")
    ).group_by(Dialogue.message_type).all()

    return [
        {"type": r.message_type, "count": r.count}
        for r in results
    ]


@router.get("/appointments/compliance", summary="获取复诊依从性统计")
async def get_appointment_compliance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取复诊依从性统计（已完成/总计划）
    """
    total = db.query(func.count(Appointment.id)).scalar()
    completed = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "completed"
    ).scalar()

    compliance_rate = (completed / total * 100) if total > 0 else 0

    return {
        "total": total,
        "completed": completed,
        "compliance_rate": round(compliance_rate, 2)
    }
