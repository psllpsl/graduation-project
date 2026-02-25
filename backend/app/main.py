from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api import auth, patients, appointments, dialogues, knowledge, stats

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",      # Swagger UI 地址
    redoc_url="/redoc",    # ReDoc 地址
    openapi_url="/openapi.json"
)

# 配置 CORS（跨域）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用牙科修复复诊提醒系统 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}


# 注册 API 路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(patients.router, prefix="/api/patients", tags=["患者管理"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["复诊管理"])
app.include_router(dialogues.router, prefix="/api/dialogues", tags=["对话管理"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识库"])
app.include_router(stats.router, prefix="/api/stats", tags=["数据统计"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
