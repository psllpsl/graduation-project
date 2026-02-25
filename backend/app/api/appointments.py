from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from ..models.appointment import Appointment
from ..dependencies import get_current_user
from ..models.user import User

router = APIRouter()


@router.get("/", response_model=List[AppointmentResponse], summary="获取复诊计划列表")
async def get_appointments(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    status_filter: Optional[str] = Query(None, description="状态筛选：pending/completed/cancelled"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取复诊计划列表（支持分页和状态筛选）
    """
    query = db.query(Appointment)

    if status_filter:
        query = query.filter(Appointment.status == status_filter)

    appointments = query.offset(skip).limit(limit).all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse, summary="获取复诊计划详情")
async def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据 ID 获取复诊计划详细信息
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )
    return appointment


@router.get("/patient/{patient_id}", response_model=List[AppointmentResponse], summary="获取患者的复诊计划")
async def get_appointments_by_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定患者的所有复诊计划
    """
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).order_by(Appointment.appointment_date).all()
    return appointments


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED, summary="创建复诊计划")
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新的复诊计划

    - **patient_id**: 患者 ID
    - **appointment_date**: 复诊日期时间
    - **appointment_type**: 复诊类型
    - **notes**: 复诊备注
    """
    appointment = Appointment(**appointment_data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse, summary="更新复诊计划")
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新复诊计划信息
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )

    # 更新字段
    update_data = appointment_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除复诊计划")
async def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除复诊计划
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )

    db.delete(appointment)
    db.commit()
    return None


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse, summary="更新复诊状态")
async def update_appointment_status(
    appointment_id: int,
    new_status: str = Query(..., description="新状态：pending/completed/cancelled"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新复诊计划状态
    """
    if new_status not in ["pending", "completed", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的状态值"
        )

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )

    appointment.status = new_status
    db.commit()
    db.refresh(appointment)
    return appointment
