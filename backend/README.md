# 牙科修复复诊提醒系统 - FastAPI 后端

基于 AI 智能客服的牙科修复复诊提醒与管理系统的后端服务。

## 技术栈

- **框架**: FastAPI 0.109.0
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0
- **缓存**: Redis 6.0+
- **认证**: JWT (PyJWT)
- **数据验证**: Pydantic V2

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── config.py            # 配置文件
│   ├── database.py          # 数据库连接
│   ├── dependencies.py      # 依赖注入（认证等）
│   ├── models/              # 数据模型层
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── treatment_record.py
│   │   ├── appointment.py
│   │   ├── dialogue.py
│   │   ├── knowledge_base.py
│   │   └── system_config.py
│   ├── schemas/             # 数据验证层
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   ├── dialogue.py
│   │   ├── knowledge_base.py
│   │   └── system_config.py
│   ├── api/                 # API 路由层
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证接口
│   │   ├── patients.py      # 患者接口
│   │   ├── appointments.py  # 复诊接口
│   │   ├── dialogues.py     # 对话接口
│   │   ├── knowledge.py     # 知识库接口
│   │   └── stats.py         # 统计接口
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py  # 认证服务
│   │   └── ai_service.py    # AI 服务
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── security.py      # 密码加密
│       ├── jwt.py           # JWT 工具
│       └── redis_cache.py   # Redis 缓存
├── tests/                   # 测试目录
│   ├── __init__.py
│   └── test_api.py
├── .env                     # 环境变量配置
├── .gitignore
├── requirements.txt
├── start_server.bat         # Windows 启动脚本
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```env
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=dental_clinic
DATABASE_USER=root
DATABASE_PASSWORD=123456

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 3. 启动服务

**Windows 用户**：
```bash
start_server.bat
```

**手动启动**：
```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 认证接口
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/me` - 获取当前用户信息

### 患者管理
- `GET /api/patients/` - 获取患者列表
- `GET /api/patients/{id}` - 获取患者详情
- `POST /api/patients/` - 创建患者
- `PUT /api/patients/{id}` - 更新患者
- `DELETE /api/patients/{id}` - 删除患者

### 复诊管理
- `GET /api/appointments/` - 获取复诊计划列表
- `GET /api/appointments/{id}` - 获取复诊详情
- `POST /api/appointments/` - 创建复诊计划
- `PUT /api/appointments/{id}` - 更新复诊计划
- `DELETE /api/appointments/{id}` - 删除复诊计划

### 对话管理
- `GET /api/dialogues/` - 获取对话记录列表
- `POST /api/dialogues/` - 创建对话（AI 回复）
- `GET /api/dialogues/session/{session_id}` - 获取会话历史
- `POST /api/dialogues/{id}/handover` - 标记人工接管

### 知识库
- `GET /api/knowledge/` - 获取知识库列表
- `GET /api/knowledge/{id}` - 获取知识详情
- `POST /api/knowledge/` - 创建知识条目
- `GET /api/knowledge/search/query` - 搜索知识

### 数据统计
- `GET /api/stats/overview` - 概览统计
- `GET /api/stats/appointments/trend` - 复诊趋势
- `GET /api/stats/dialogues/daily` - 对话统计
- `GET /api/stats/appointments/compliance` - 复诊依从性

## 运行测试

```bash
pytest tests/
```

## API 接口清单

### 认证模块 (/api/auth)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /login | 用户登录 |
| POST | /register | 用户注册（需管理员权限） |
| GET | /me | 获取当前用户信息 |

### 患者管理 (/api/patients)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取患者列表 |
| GET | /{id} | 获取患者详情 |
| POST | / | 创建患者 |
| PUT | /{id} | 更新患者 |
| DELETE | /{id} | 删除患者（需管理员权限） |
| GET | /search/phone/{phone} | 按手机号搜索 |

### 复诊管理 (/api/appointments)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取复诊计划列表 |
| GET | /{id} | 获取复诊详情 |
| GET | /patient/{patient_id} | 获取患者的复诊计划 |
| POST | / | 创建复诊计划 |
| PUT | /{id} | 更新复诊计划 |
| DELETE | /{id} | 删除复诊计划 |
| PATCH | /{id}/status | 更新复诊状态 |

### 对话管理 (/api/dialogues)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取对话记录列表 |
| POST | / | 创建对话（AI 回复） |
| GET | /session/{session_id} | 获取会话历史 |
| POST | /{id}/handover | 标记人工接管 |
| GET | /handover/pending | 获取待人工接管对话 |

### 知识库 (/api/knowledge)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | 获取知识库列表 |
| GET | /{id} | 获取知识详情 |
| POST | / | 创建知识条目（需管理员权限） |
| PUT | /{id} | 更新知识条目（需管理员权限） |
| DELETE | /{id} | 删除知识条目（需管理员权限） |
| GET | /search/query | 搜索知识 |
| GET | /categories | 获取分类列表 |

### 数据统计 (/api/stats)
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /overview | 概览统计 |
| GET | /appointments/trend | 复诊趋势 |
| GET | /dialogues/daily | 每日对话统计 |
| GET | /patients/gender | 患者性别分布 |
| GET | /appointments/status | 复诊状态分布 |
| GET | /dialogues/types | 对话类型统计 |
| GET | /appointments/compliance | 复诊依从性 |

## 注意事项

1. **首次运行前**需要确保 MySQL 数据库已创建并导入初始化数据
2. **Redis 服务**需要运行以支持会话缓存功能
3. **JWT 密钥**在生产环境中请修改为随机字符串（可使用 `openssl rand -hex 32` 生成）
4. **AI 服务**需要配置 `AI_SERVICE_URL` 才能调用大模型

## 许可证

MIT License

---

**最后更新**: 2026 年 2 月 22 日
