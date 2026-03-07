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
    
    # 今日新增患者
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    new_patients_today = db.query(func.count(Patient.id)).filter(
        Patient.created_at >= today_start
    ).scalar()

    # 复诊计划总数
    total_appointments = db.query(func.count(Appointment.id)).scalar()

    # 今日复诊数量
    today_appointments = db.query(func.count(Appointment.id)).filter(
        func.date(Appointment.appointment_date) == datetime.now().date()
    ).scalar()
    
    # 待复诊数量
    pending_appointments = db.query(func.count(Appointment.id)).filter(
        Appointment.status == "pending"
    ).scalar()
    
    # 今日完成复诊
    completed_appointments_today = db.query(func.count(Appointment.id)).filter(
        func.date(Appointment.appointment_date) == datetime.now().date(),
        Appointment.status == "completed"
    ).scalar()

    # 对话总数
    total_dialogues = db.query(func.count(Dialogue.id)).scalar()
    
    # 今日对话数量
    today_dialogues = db.query(func.count(Dialogue.id)).filter(
        func.date(Dialogue.created_at) == datetime.now().date()
    ).scalar()
    
    # 昨日对话数量（用于计算增长率）
    yesterday = datetime.now().date() - timedelta(days=1)
    yesterday_dialogues = db.query(func.count(Dialogue.id)).filter(
        func.date(Dialogue.created_at) == yesterday
    ).scalar()
    
    # 对话增长率
    dialogue_growth_rate = 0
    if yesterday_dialogues > 0:
        dialogue_growth_rate = round(((today_dialogues - yesterday_dialogues) / yesterday_dialogues) * 100, 1)
    elif today_dialogues > 0:
        dialogue_growth_rate = 100

    # 人工接管数量
    handover_count = db.query(func.count(Dialogue.id)).filter(
        Dialogue.is_handover == 1
    ).scalar()
    
    # 知识库总数
    from ..models.knowledge_base import KnowledgeBase
    total_knowledge = db.query(func.count(KnowledgeBase.id)).filter(
        KnowledgeBase.is_active == 1
    ).scalar()
    
    # 本周新增知识
    week_start = today_start - timedelta(days=today_start.weekday())
    new_knowledge_this_week = db.query(func.count(KnowledgeBase.id)).filter(
        KnowledgeBase.created_at >= week_start,
        KnowledgeBase.is_active == 1
    ).scalar()

    return {
        "total_patients": total_patients,
        "new_patients_today": new_patients_today,
        "total_appointments": total_appointments,
        "today_appointments": today_appointments,
        "pending_appointments": pending_appointments,
        "completed_appointments_today": completed_appointments_today,
        "total_dialogues": total_dialogues,
        "today_dialogues": today_dialogues,
        "dialogue_growth_rate": dialogue_growth_rate,
        "handover_count": handover_count,
        "total_knowledge": total_knowledge,
        "new_knowledge_this_week": new_knowledge_this_week
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
