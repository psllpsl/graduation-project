from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from .config import settings
from .database import get_db
from .models.user import User
from .utils.jwt import verify_token

# OAuth2 方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户

    Args:
        token: JWT Token
        db: 数据库会话

    Returns:
        当前用户对象

    Raises:
        HTTPException: 认证失败
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 验证 Token
    payload = verify_token(token)
    if payload is None:
        print(f"Token 验证失败：{token}")
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        print(f"Token 中没有 user_id: {payload}")
        raise credentials_exception

    print(f"Token 解析成功 - user_id: {user_id}")

    # 将 user_id 从字符串转换为整数
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        print(f"user_id 转换失败：{user_id}")
        raise credentials_exception

    # 查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        print(f"数据库中未找到用户 ID: {user_id}")
        raise credentials_exception

    print(f"用户验证成功：{user.username}")
    return user


def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前管理员用户

    Args:
        current_user: 当前登录用户

    Returns:
        管理员用户对象

    Raises:
        HTTPException: 权限不足
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理员角色"
        )
    return current_user
