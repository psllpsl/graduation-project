from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from ..config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT Access Token

    Args:
        data: 要编码的数据（如用户 ID、角色）
        expires_delta: 过期时间增量

    Returns:
        JWT Token 字符串
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    验证 JWT Token

    Args:
        token: JWT Token 字符串

    Returns:
        解码后的数据，验证失败返回 None
    """
    try:
        print(f"正在验证 Token，SECRET_KEY: {settings.SECRET_KEY[:10]}...")
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print(f"Token 验证成功：{payload}")
        return payload
    except Exception as e:
        print(f"Token 验证失败：{e}")
        return None
