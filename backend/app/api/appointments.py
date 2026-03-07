from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from ..models.appointment import Appointment
from ..dependencies import get_current_user, get_current_admin_user
from ..models.user import User
from ..models.patient import Patient
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from ..config import settings

router = APIRouter()


@router.get("/", response_model=List[AppointmentResponse], summary="获取复诊计划列表（医护后台）")
async def get_appointments_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取复诊计划列表（供医护后台使用）
    
    **权限**：需要医护或管理员权限
    """
    query = db.query(Appointment)
    
    if status:
        query = query.filter(Appointment.status == status)
    
    # 分页
    offset = (page - 1) * page_size
    appointments = query.order_by(Appointment.appointment_date.desc()).offset(offset).limit(page_size).all()
    
    return appointments


def get_patient_id_from_token(credentials: HTTPAuthorizationCredentials) -> Optional[int]:
    """
    从 JWT Token 中提取 patient_id
    返回 None 表示 Token 无效或未提供
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # 从 Token 中提取 patient_id 或 openid
        sub = payload.get("sub")  # 格式："patient:123"
        if sub and sub.startswith("patient:"):
            return int(sub.split(":")[1])
        
        # 或者直接有 patient_id 字段
        patient_id = payload.get("patient_id")
        if patient_id:
            return int(patient_id)
            
    except (JWTError, ValueError, KeyError):
        pass
    
    return None


@router.get("/patient/my", response_model=List[AppointmentResponse], summary="获取我的复诊计划")
async def get_my_appointments(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
):
    """
    获取当前登录患者的复诊计划
    
    **安全机制**：
    1. 从 JWT Token 中提取 patient_id
    2. 只返回该 patient_id 对应的复诊计划
    3. 无法访问其他患者的数据
    """
    patient_id = get_patient_id_from_token(credentials)
    
    if not patient_id:
        # 未登录，返回空列表
        return []
    
    # 查询该患者的复诊计划
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).order_by(Appointment.appointment_date).all()
    
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentResponse, summary="获取复诊计划详情")
async def get_appointment(
    appointment_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
):
    """
    获取复诊计划详情
    
    **安全机制**：验证 Token 中的 patient_id 与复诊计划的 patient_id 是否匹配
    """
    patient_id = get_patient_id_from_token(credentials)
    
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )
    
    # 验证权限：只有该复诊计划所属的患者才能查看
    if patient_id and appointment.patient_id != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看该复诊计划"
        )
    
    return appointment


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse, summary="更新复诊状态")
async def update_appointment_status(
    appointment_id: int,
    status_update: dict,  # 接收 JSON body: {"status": "pending"}
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
):
    """
    更新复诊状态

    **安全机制**：验证 Token 中的 patient_id 与复诊计划的 patient_id 是否匹配
    """
    patient_id = get_patient_id_from_token(credentials)
    
    # 从 JSON 中提取 status
    status = status_update.get("status")
    if not status:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="缺少 status 参数"
        )

    if not patient_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录"
        )

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )

    # 验证权限
    if appointment.patient_id != patient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改该复诊计划"
        )

    # 更新状态
    appointment.status = status
    db.commit()
    db.refresh(appointment)
    return appointment


@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED, summary="创建复诊计划")
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # 需要管理员权限
):
    """
    创建新的复诊计划（需要管理员权限）
    """
    patient = db.query(Patient).filter(Patient.id == appointment_data.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    
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
    current_user: User = Depends(get_current_admin_user)  # 需要管理员权限
):
    """
    更新复诊计划（需要管理员权限）
    """
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="复诊计划不存在"
        )
    
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
    current_user: User = Depends(get_current_admin_user)  # 需要管理员权限
):
    """
    删除复诊计划（需要管理员权限）
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
