from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """应用配置"""

    # 应用基础配置
    APP_NAME: str = "牙科修复复诊提醒系统 API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    APP_DESCRIPTION: str = "基于 AI 智能客服的牙科修复复诊提醒与管理系统 - 后端 API 接口"

    # 数据库配置
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str = "dental_clinic"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "123456"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"  # 生产环境请修改为随机字符串
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 小时

    # AI 服务配置
    AI_SERVICE_URL: Optional[str] = None  # AI 服务地址
    AI_SERVICE_TYPE: str = "autodl"  # AI 服务类型：autodl / local / api
    AI_MAX_TOKENS: int = 150
    AI_TEMPERATURE: float = 0.7
    AI_TIMEOUT_SECONDS: int = 60  # AI 请求超时时间（秒）

    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_SESSION_EXPIRE: int = 1800  # 30 分钟

    # 跨域配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
    ]

    # 任务调度配置
    SCHEDULER_API_ENABLED: bool = True
    SCHEDULER_TIMEZONE: str = "Asia/Shanghai"

    @property
    def DATABASE_URL(self) -> str:
        """构造数据库连接 URL"""
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            f"?charset=utf8mb4"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
