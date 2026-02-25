from passlib.context import CryptContext

# 创建密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    对密码进行哈希加密

    Args:
        password: 原始密码

    Returns:
        加密后的密码哈希
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 原始密码
        hashed_password: 加密后的密码哈希

    Returns:
        验证结果
    """
    return pwd_context.verify(plain_password, hashed_password)
