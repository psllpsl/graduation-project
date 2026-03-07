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
from typing import Optional


class WxLoginRequest(BaseModel):
    """微信登录请求"""
    code: str


class WxLoginResponse(BaseModel):
    """微信登录响应"""
    access_token: str
    token_type: str = "bearer"
    openid: str
    user: dict = None


class RegisterRequest(BaseModel):
    """注册请求（需要管理员确认）"""
    username: str
    password: str
    real_name: str
    role: str = "doctor"
    phone: Optional[str] = None
    admin_username: str  # 管理员用户名
    admin_password: str  # 管理员密码


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    target_username: str  # 要重置密码的用户名
    admin_username: str  # 管理员用户名
    admin_password: str  # 管理员密码（用于验证）
    new_password: str  # 新密码


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
        
        # 获取用户信息
        user = db.query(User).filter(User.username == form_data.username).first()
        user_info = {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "role": user.role,
            "phone": user.phone
        } if user else None
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_info
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="用户注册（需要管理员确认）")
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    注册新用户（需要管理员密码确认）

    - **username**: 用户名
    - **password**: 密码
    - **real_name**: 真实姓名
    - **role**: 角色（admin/doctor，默认 doctor）
    - **phone**: 手机号
    - **admin_username**: 管理员用户名
    - **admin_password**: 管理员密码（用于验证）
    """
    try:
        # 验证管理员身份
        from ..utils.security import verify_password
        admin = db.query(User).filter(User.username == request.admin_username).first()
        
        if not admin or admin.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="管理员身份验证失败"
            )
        
        if not verify_password(request.admin_password, admin.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="管理员密码错误"
            )
        
        # 检查用户名是否存在
        existing_user = db.query(User).filter(User.username == request.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        user = create_user(
            db=db,
            username=request.username,
            password=request.password,
            real_name=request.real_name,
            role=request.role if request.role else "doctor",
            phone=request.phone
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/reset-password", summary="重置密码（需要管理员确认）")
async def reset_password(
    target_username: str,
    admin_username: str,
    admin_password: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    重置用户密码（需要管理员确认）
    """
    from ..utils.security import verify_password, hash_password
    
    # 验证管理员
    admin = db.query(User).filter(User.username == admin_username).first()
    if not admin or admin.role != "admin":
        raise HTTPException(403, "管理员验证失败")
    if not verify_password(admin_password, admin.password_hash):
        raise HTTPException(401, "管理员密码错误")
    
    # 查找用户
    user = db.query(User).filter(User.username == target_username).first()
    if not user:
        raise HTTPException(404, "用户不存在")
    
    # 更新密码
    user.password_hash = hash_password(new_password)
    db.commit()
    
    return {"message": "密码重置成功", "username": target_username}


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
