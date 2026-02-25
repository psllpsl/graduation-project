"""
API 接口测试文件
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "牙科修复复诊提醒系统 API" in response.json()["message"]


def test_health_check():
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_failure():
    """测试登录失败（无效凭据）"""
    response = client.post(
        "/api/auth/login",
        data={"username": "invalid_user", "password": "wrong_password"}
    )
    assert response.status_code == 401


def test_get_patients_unauthorized():
    """测试未授权访问患者列表"""
    response = client.get("/api/patients/")
    assert response.status_code == 401


def test_openapi_schema():
    """测试 OpenAPI  schema"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "paths" in response.json()


def test_docs_available():
    """测试 Swagger UI 可访问"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_available():
    """测试 ReDoc 可访问"""
    response = client.get("/redoc")
    assert response.status_code == 200
