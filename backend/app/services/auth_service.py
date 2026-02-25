from datetime import timedelta
from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.security import hash_password, verify_password
from ..utils.jwt import create_access_token
from ..config import settings


def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    验证用户登录

    Args:
        db: 数据库会话
        username: 用户名
        password: 密码

    Returns:
        验证通过返回用户对象，否则返回 None
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def login_for_access_token(db: Session, username: str, password: str) -> str:
    """
    登录并获取 Access Token

    Args:
        db: 数据库会话
        username: 用户名
        password: 密码

    Returns:
        JWT Token

    Raises:
        ValueError: 认证失败
    """
    user = authenticate_user(db, username, password)
    if not user:
        raise ValueError("用户名或密码错误")

    # 创建 Token（sub 必须是字符串）
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return access_token


def create_user(db: Session, username: str, password: str, real_name: str,
                role: str = "doctor", phone: str = None) -> User:
    """
    创建新用户

    Args:
        db: 数据库会话
        username: 用户名
        password: 密码
        real_name: 真实姓名
        role: 角色
        phone: 手机号

    Returns:
        创建的用户对象

    Raises:
        ValueError: 用户名已存在
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise ValueError("用户名已存在")

    # 创建用户
    user = User(
        username=username,
        password_hash=hash_password(password),
        real_name=real_name,
        role=role,
        phone=phone
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
