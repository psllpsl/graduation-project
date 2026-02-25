from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 连接前 ping 测试
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 最大溢出连接数
    echo=settings.DEBUG   # 打印 SQL 日志（开发环境）
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话依赖
    用于 FastAPI 的依赖注入
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
