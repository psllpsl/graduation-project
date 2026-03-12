from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from ..models.patient import Patient
from ..dependencies import get_current_user, get_current_admin_user
from ..models.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from ..config import settings

router = APIRouter()


def get_patient_id_from_token(credentials: HTTPAuthorizationCredentials) -> Optional[int]:
    """从 JWT Token 中提取 patient_id"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        if not credentials:
            logger.warning("No credentials provided")
            return None
            
        token = credentials.credentials
        logger.info(f"Token received: {token[:20]}...")
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        logger.info(f"Token payload: {payload}")
        
        sub = payload.get("sub")
        logger.info(f"Token sub: {sub}")
        
        if sub and sub.startswith("patient:"):
            patient_id = int(sub.split(":")[1])
            logger.info(f"Extracted patient_id from sub: {patient_id}")
            return patient_id
            
        patient_id = payload.get("patient_id")
        if patient_id:
            logger.info(f"Extracted patient_id from payload: {patient_id}")
            return int(patient_id)
            
        logger.warning("patient_id not found in token")
    except (JWTError, ValueError, KeyError) as e:
        logger.error(f"Token decode error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    return None


# 注意：带固定前缀的路由必须放在动态参数路由之前
# 否则 /openid/xxx 会被 /{patient_id} 匹配

@router.get("/check-complete", summary="检查患者信息是否完善")
async def check_patient_complete(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
):
    """
    检查当前登录患者的信息是否完善

    判断标准：phone 字段不为空即认为信息完善
    """
    patient_id = get_patient_id_from_token(credentials)

    if not patient_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录"
        )

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )

    # 检查是否完善（phone 不为空即认为完善）
    is_complete = bool(patient.phone)

    return {
        "is_complete": is_complete,
        "patient_id": patient.id,
        "name": patient.name,
        "phone": patient.phone
    }


@router.post("/complete", response_model=PatientResponse, summary="患者完善个人信息（小程序专用）")
async def complete_patient_info(
    patient_data: PatientUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
):
    """
    患者首次登录时完善个人信息
    
    需要填写：
    - name: 姓名
    - gender: 性别
    - age: 年龄
    - phone: 手机号
    - medical_history: 既往病史（可选）
    - allergy_history: 过敏史（可选）
    """
    patient_id = get_patient_id_from_token(credentials)

    if not patient_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="请先登录"
        )

    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )

    # 更新信息
    update_data = patient_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    return patient


@router.get("/by-openid/{openid}", response_model=PatientResponse, summary="根据 openid 获取患者信息")
async def get_patient_by_openid(
    openid: str,
    db: Session = Depends(get_db)
):
    """
    根据微信 openid 获取患者信息
    用于小程序登录后获取患者详情
    """
    patient = db.query(Patient).filter(Patient.openid == openid).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="患者不存在"
        )
    return patient


@router.get("/", response_model=List[PatientResponse], summary="获取患者列表")
async def get_patients(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数（最大 1000）"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取患者列表（支持分页）

    - **skip**: 跳过记录数
    - **limit**: 返回记录数（最大 1000）
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
