# FastAPI 后端服务

> 牙科修复复诊管理系统的后端 API 服务

## 📋 功能特性

- ✅ **用户认证** - JWT Token + bcrypt 密码加密
- ✅ **患者管理** - CRUD + 筛选 + 微信登录
- ✅ **复诊管理** - CRUD + 状态更新
- ✅ **对话管理** - AI 对话 + 人工接管 + 会话管理
- ✅ **知识库** - CRUD + 分类搜索
- ✅ **数据统计** - 可视化数据接口
- ✅ **用户管理** - 注册 + 重置密码（需 admin 确认）

## 🚀 快速开始

### 1. 安装依赖

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境

编辑 `.env` 文件或 `app/config.py`：

```python
# 数据库配置
DATABASE_URL = "mysql+pymysql://root:密码@localhost:3306/dental_clinic"

# JWT 配置
SECRET_KEY = "your-secret-key"

# AI 服务配置
AI_SERVICE_URL = "https://实例 ID.seetacloud.com:端口/generate"
```

### 3. 启动服务

```bash
# 方式一：使用启动脚本
start_server.bat

# 方式二：手动启动
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问 API

- **API 文档**：http://localhost:8000/docs
- **ReDoc**：http://localhost:8000/redoc

## 📁 项目结构

```
backend/
├── app/
│   ├── main.py              # 应用入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── dependencies.py      # 依赖注入
│   ├── models/              # SQLAlchemy 模型
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   └── ...
│   ├── schemas/             # Pydantic 数据验证
│   ├── api/                 # API 路由
│   │   ├── auth.py          # 认证接口
│   │   ├── patients.py      # 患者接口
│   │   └── ...
│   └── services/            # 业务逻辑
│       └── ai_service.py    # AI 服务
├── tests/                   # 测试
├── requirements.txt         # 依赖
└── start_server.bat         # 启动脚本
```

## 🔐 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| doctor_zhang | admin123 | 医生 |
| doctor_li | admin123 | 护士 |

## 📞 API 接口

### 认证模块
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册（需 admin 确认）
- `POST /api/auth/reset-password` - 重置密码（需 admin 确认）
- `GET /api/auth/me` - 获取当前用户信息

### 患者管理
- `GET /api/patients/` - 获取患者列表
- `POST /api/patients/` - 创建患者
- `PUT /api/patients/{id}` - 更新患者
- `DELETE /api/patients/{id}` - 删除患者

### 复诊管理
- `GET /api/appointments/` - 获取复诊列表
- `POST /api/appointments/` - 创建复诊
- `PATCH /api/appointments/{id}/status` - 更新状态
- `DELETE /api/appointments/{id}` - 删除复诊

### 对话管理
- `POST /api/dialogues/` - 创建对话（AI 回复）
- `GET /api/dialogues/` - 获取对话列表
- `POST /api/dialogues/{id}/handover` - 标记人工接管

---

**版本**：v3.0  
**最后更新**：2026-03-07
