from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.user import UserCreate, UserResponse, Token
from ..services.auth_service import login_for_access_token, create_user
from ..dependencies import get_current_user, get_current_admin_user
from ..models.user import User

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
