from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from ..models.patient import Patient
from ..dependencies import get_current_user, get_current_admin_user
from ..models.user import User

router = APIRouter()


@router.get("/", response_model=List[PatientResponse], summary="获取患者列表")
async def get_patients(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取患者列表（支持分页）

    - **skip**: 跳过记录数
    - **limit**: 返回记录数（最大 100）
    """
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients


@router.get("/{patient_id}", response_model=PatientResponse, summary="获取患者详情")
async def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据 ID 获取患者详细信息
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    return patient


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED, summary="创建患者")
async def create_patient(
    patient_data: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新患者

    - **openid**: 微信用户标识
    - **name**: 姓名
    - **gender**: 性别
    - **age**: 年龄
    - **phone**: 手机号
    - **medical_history**: 既往病史
    - **allergy_history**: 过敏史
    """
    # 检查 openid 是否已存在
    existing = db.query(Patient).filter(Patient.openid == patient_data.openid).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该微信用户已注册"
        )

    patient = Patient(**patient_data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.put("/{patient_id}", response_model=PatientResponse, summary="更新患者信息")
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新患者信息
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )

    # 更新字段
    update_data = patient_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除患者")
async def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # 需要管理员权限
):
    """
    删除患者（需要管理员权限）
    """
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )

    db.delete(patient)
    db.commit()
    return None


@router.get("/search/phone/{phone}", response_model=List[PatientResponse], summary="按手机号搜索患者")
async def search_patient_by_phone(
    phone: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据手机号搜索患者
    """
    patients = db.query(Patient).filter(Patient.phone.like(f"%{phone}%")).limit(10).all()
    return patients
