from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate, UserResponse, Token
from ..services.auth_service import login_for_access_token, create_user
from ..dependencies import get_current_user, get_current_admin_user
from ..models.user import User
from ..models.patient import Patient
from pydantic import BaseModel
from datetime import timedelta


class WxLoginRequest(BaseModel):
    """微信登录请求"""
    code: str


class WxLoginResponse(BaseModel):
    """微信登录响应"""
    access_token: str
    token_type: str = "bearer"
    openid: str
    user: dict = None


router = APIRouter()


@router.post("/login", response_model=Token, summary="用户登录")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口

    - **username**: 用户名
    - **password**: 密码

    返回 JWT Token，用于后续接口认证。
    """
    try:
        access_token = login_for_access_token(
            db=db,
            username=form_data.username,
            password=form_data.password
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="用户注册")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # 需要管理员权限
):
    """
    注册新用户（需要管理员权限）

    - **username**: 用户名
    - **password**: 密码
    - **real_name**: 真实姓名
    - **role**: 角色（admin/doctor）
    - **phone**: 手机号
    """
    try:
        user = create_user(
            db=db,
            username=user_data.username,
            password=user_data.password,
            real_name=user_data.real_name,
            role=user_data.role,
            phone=user_data.phone
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户的信息
    """
    return current_user


@router.post("/wx-login", response_model=WxLoginResponse, summary="微信登录")
async def wx_login(
    request: WxLoginRequest,
    db: Session = Depends(get_db)
):
    """
    微信小程序登录接口（开发测试版）
    
    注意：此为测试模式，使用模拟的 openid
    生产环境请替换为真实的微信 API 调用
    """
    # 开发模式：使用模拟的 openid
    # 使用固定的测试 openid（方便调试）
    openid = "test_openid_" + request.code[-6:] if request.code else "test_openid_123456"
    
    # 查询或创建患者
    patient = db.query(Patient).filter(Patient.openid == openid).first()
    
    if not patient:
        # 创建新患者
        patient = Patient(
            openid=openid,
            name=f"用户_{openid[-4:].upper()}",  # 默认昵称，如：用户_A1B2
            gender=None,
            age=None,
            phone=None,
            medical_history=None,
            allergy_history=None
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
    
    # 3. 生成 JWT Token
    from ..utils.jwt import create_access_token
    from ..config import settings
    
    token_data = {
        "sub": f"patient:{patient.id}",
        "openid": openid,
        "role": "patient"
    }
    
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=token_data, expires_delta=expire)
    
    # 4. 返回结果
    return WxLoginResponse(
        access_token=access_token,
        token_type="bearer",
        openid=openid,
        user={
            "id": patient.id,
            "openid": openid,
            "name": patient.name,
            "phone": patient.phone,
            "gender": patient.gender,
            "age": patient.age
        }
    )
