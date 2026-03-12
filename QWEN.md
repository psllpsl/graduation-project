# 毕业设计项目上下文文档

> **项目名称**：基于 AI 智能客服的牙科修复复诊提醒与管理系统
> **最后更新**：2026 年 3 月 12 日
> **项目状态**：✅ 全部完成（后端 + 小程序 + Streamlit 后台 + AI）
> **文档版本**：v3.1（最终内容版）

---

## 📋 项目概述

这是一个**医疗健康类软件系统**，旨在为牙科修复患者提供 7×24 小时智能随访服务。系统通过微信小程序为患者提供自然语言对话服务，通过自动化提醒与专业咨询降低漏复诊率，提升患者治疗依从性。

### 核心价值
- **降低漏复诊率**：自动化复诊提醒 + 专业术后指导
- **减轻医护负担**：AI 客服替代重复性电话咨询
- **提升患者体验**：微信小程序 + 即时专业回复

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     牙科修复复诊提醒与管理系统                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  微信小程序  │  │ Streamlit 后台│  │  AI 引擎     │             │
│  │   (患者端)   │  │   (医护端)   │  │ (智能客服)  │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│              ┌───────────────────────┐                          │
│              │   FastAPI 后端服务     │                          │
│              │   (业务逻辑中枢)       │                          │
│              └───────────┬───────────┘                          │
│                          │                                      │
│         ┌────────────────┼────────────────┐                     │
│         ▼                ▼                ▼                     │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐                │
│   │  MySQL    │   │ 知识库     │   │  AI 服务    │                │
│   │  数据库    │   │  (RAG)     │   │ (AutoDL)   │                │
│   └───────────┘   └───────────┘   └───────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### 五大核心模块

| 模块 | 定位 | 技术栈 | 状态 |
|------|------|--------|------|
| **微信小程序** | 患者交互入口 | 原生小程序框架 | ✅ 完成 |
| **FastAPI 后端** | 系统服务中枢 | FastAPI + SQLAlchemy + Pydantic | ✅ 完成 |
| **AI 智能客服** | 系统"大脑" | Qwen2.5-7B + RAG + LoRA | ✅ 部署 |
| **Streamlit 后台** | 医护操作平台 | Streamlit + Plotly | ✅ 完成 |
| **基础设施** | 运行保障 | MySQL + JWT 认证 | ✅ 完成 |

---

## 📁 项目结构

```
D:\Project\毕业设计\
├── backend/                    # FastAPI 后端服务
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   ├── dependencies.py    # 依赖注入（认证等）
│   │   ├── models/            # SQLAlchemy 模型层
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   ├── treatment_record.py
│   │   │   ├── appointment.py
│   │   │   ├── dialogue.py
│   │   │   ├── knowledge_base.py
│   │   │   └── system_config.py
│   │   ├── schemas/           # Pydantic 数据验证层
│   │   │   └── ...
│   │   ├── api/               # API 路由层
│   │   │   ├── auth.py        # 认证接口
│   │   │   ├── patients.py    # 患者接口
│   │   │   ├── appointments.py# 复诊接口
│   │   │   ├── dialogues.py   # 对话接口
│   │   │   ├── knowledge.py   # 知识库接口
│   │   │   └── stats.py       # 统计接口
│   │   ├── services/          # 业务逻辑层
│   │   │   ├── auth_service.py
│   │   │   └── ai_service.py  # AI 服务
│   │   └── utils/             # 工具函数
│   │       ├── security.py    # 密码加密
│   │       ├── jwt.py         # JWT 工具
│   │       └── redis_cache.py # Redis 缓存
│   ├── tests/                 # 测试目录
│   ├── requirements.txt       # Python 依赖
│   ├── start_server.bat       # Windows 启动脚本
│   └── README.md              # 后端文档
├── data/                      # 数据与 AI 相关
│   ├── knowledge/
│   │   └── knowledge_base_v3.json   # 知识库（804 条）
│   ├── train/
│   │   └── train.json               # 训练集（500 条）
│   ├── scripts/               # 数据处理脚本
│   └── README.md              # 数据集文档
├── docs/                      # 文档目录
│   └── 数据库设计/
│       ├── ER 图.md
│       ├── 数据字典.md
│       ├── create_tables.sql  # 建表脚本
│       └── init_data.sql      # 初始化数据
├── 01-数据库设计与搭建指南.md
├── 02-FastAPI 后端框架搭建指南.md
├── 03-AI 训练与知识库构建指南.md
├── 04-微信小程序前端搭建指南.md  # 新增
├── 毕业设计组成说明文档.md
└── QWEN.md                    # 本文档
```

---

## 🛠️ 技术栈

### 后端技术

| 类别 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **框架** | FastAPI | 0.109.0 | RESTful API |
| **ORM** | SQLAlchemy | 2.0.25 | 数据库操作 |
| **验证** | Pydantic | 2.5.3 | 数据校验 |
| **数据库** | MySQL | 8.0+ | 关系型存储 |
| **缓存** | Redis | 6.0+ | 会话缓存 |
| **认证** | JWT (PyJWT) | 2.8+ | 令牌认证 |
| **调度** | APScheduler | 3.10.4 | 定时任务 |
| **HTTP** | httpx | 0.26.0 | API 调用 |

### AI 技术

| 技术 | 说明 |
|------|------|
| **基座模型** | Qwen2.5-7B-Instruct（阿里云通义千问） |
| **微调方式** | LoRA（低秩适应微调） |
| **训练平台** | AutoDL 云平台（RTX 4090 GPU） |
| **训练框架** | LLaMA Factory |
| **推理框架** | vLLM / Transformers |
| **知识检索** | RAG（检索增强生成）+ MySQL 关键词匹配 |
| **提示工程** | System Prompt + Few-shot + 上下文 |

### 前端技术（待开发）

| 模块 | 技术 |
|------|------|
| **患者端** | 微信小程序（原生 WXML/WXSS/JavaScript） |
| **医护端** | Streamlit + Plotly |

---

## 🚀 快速开始

### 1. 环境准备

```bash
# Python 版本要求：3.10+
python --version

# 进入后端目录
cd backend
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```env
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=dental_clinic
DATABASE_USER=root
DATABASE_PASSWORD=你的密码

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT 配置
SECRET_KEY=your-secret-key-change-in-production

# AI 服务配置（已部署到 AutoDL）
# 注意：实例 ID 会变化，请根据实际情况配置
AI_SERVICE_URL=https://你的实例 ID.seetacloud.com:端口/generate
AI_SERVICE_TYPE=autodl
AI_MAX_TOKENS=150
AI_TEMPERATURE=0.7
AI_TIMEOUT_SECONDS=60
```

### 4. 启动服务

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

### 5. 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 数据库设计

### 数据库概览

- **数据库名**：`dental_clinic`
- **字符集**：`utf8mb4`
- **表数量**：7 张

### 数据表清单

| 表名 | 说明 | 主要字段 |
|------|------|----------|
| `users` | 用户表（医护/管理员） | id, username, password_hash, role, real_name |
| `patients` | 患者档案表 | id, openid, name, gender, age, phone, medical_history |
| `treatment_records` | 治疗记录表 | id, patient_id, treatment_type, treatment_date, dentist_id |
| `appointments` | 复诊计划表 | id, patient_id, appointment_date, status, reminder_sent |
| `dialogues` | 对话日志表 | id, patient_id, session_id, user_message, ai_response |
| `knowledge_base` | 知识库表 | id, category, title, content, keywords, source |
| `system_config` | 系统配置表 | id, config_key, config_value, description |

### 实体关系

```
users ||--o{ treatment_records : "执行"
patients ||--o{ treatment_records : "拥有"
patients ||--o{ appointments : "制定"
patients ||--o{ dialogues : "产生"
```

---

## 🔌 API 接口

### 认证模块 (`/api/auth`)

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/login` | 用户登录（返回 Token + 用户信息） |
| POST | `/register` | 用户注册（需管理员密码确认） |
| POST | `/reset-password` | 重置密码（需管理员密码确认） |
| POST | `/wx-login` | 微信登录（小程序专用） |
| GET | `/me` | 获取当前用户信息 |

### 患者管理 (`/api/patients`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 获取患者列表（分页） |
| GET | `/{id}` | 获取患者详情 |
| POST | `/` | 创建患者 |
| PUT | `/{id}` | 更新患者 |
| DELETE | `/{id}` | 删除患者（需管理员） |
| GET | `/search/phone/{phone}` | 按手机号搜索 |
| GET | `/by-openid/{openid}` | 按 openid 查询 |
| POST | `/complete` | 患者完善个人信息（小程序） |
| GET | `/check-complete` | 检查患者信息是否完善 |

### 复诊管理 (`/api/appointments`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 获取复诊计划列表（分页、筛选） |
| GET | `/{id}` | 获取复诊详情 |
| GET | `/patient/my` | 获取我的复诊计划（患者端） |
| POST | `/` | 创建复诊计划（需管理员） |
| PUT | `/{id}` | 更新复诊计划（需管理员） |
| DELETE | `/{id}` | 删除复诊计划（需管理员） |
| PATCH | `/{id}/status` | 更新复诊状态（医护端） |
| PATCH | `/patient/{id}/status` | 更新复诊状态（患者端） |

### 对话管理 (`/api/dialogues`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 获取对话记录列表（分页） |
| POST | `/chat` | 患者对话接口（自动获取 patient_id） |
| POST | `/` | 创建对话（AI 回复） |
| GET | `/session/{session_id}` | 获取会话历史 |
| POST | `/{id}/handover` | 标记/取消人工接管 |
| GET | `/handover/pending` | 获取待人工接管对话 |
| DELETE | `/{id}` | 删除单条对话 |
| DELETE | `/session/{session_id}` | 删除会话的所有对话 |
| DELETE | `/patient/{patient_id}` | 删除患者的所有对话 |
| DELETE | `/` | 清空所有对话 |

### 知识库 (`/api/knowledge`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 获取知识库列表（分页、分类筛选） |
| GET | `/{id}` | 获取知识详情 |
| POST | `/` | 创建知识条目（需管理员） |
| PUT | `/{id}` | 更新知识条目（需管理员） |
| DELETE | `/{id}` | 删除知识条目（需管理员） |
| GET | `/search/query` | 搜索知识（公开接口） |
| GET | `/categories` | 获取分类列表（公开接口） |

### 数据统计 (`/api/stats`)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/overview` | 概览统计（患者/复诊/对话/知识） |
| GET | `/appointments/trend` | 复诊趋势（最近 N 天） |
| GET | `/dialogues/daily` | 对话统计（最近 N 天） |
| GET | `/patients/gender` | 患者性别分布 |
| GET | `/appointments/status` | 复诊状态分布 |
| GET | `/dialogues/types` | 对话类型统计 |
| GET | `/appointments/compliance` | 复诊依从性统计 |

---

## 🤖 AI 服务配置

### AutoDL 部署

AI 模型已部署到 AutoDL 云平台（RTX 4090 GPU），配置如下：

```env
AI_SERVICE_URL=https://你的实例 ID.seetacloud.com:端口/generate
AI_SERVICE_TYPE=autodl
AI_MAX_TOKENS=150
AI_TEMPERATURE=0.7
AI_TIMEOUT_SECONDS=60
```

### 测试连接

1. 访问 http://localhost:8000/docs
2. 登录获取 Token（调用 `/api/auth/login`）
3. 调用 `POST /api/dialogues/` 接口测试对话

### 知识库统计

| 数据集 | 位置 | 数据量 | 用途 |
|--------|------|--------|------|
| **知识库** | `data/knowledge/knowledge_base_v3.json` | **804 条** | RAG 检索、MySQL 导入 |
| **训练集** | `data/train/train.json` | **500 条** | LoRA 微调训练 |

**数据来源**：《口腔修复学》第 8 版（人民卫生出版社）

---

## 📝 开发规范

### 代码风格

- **Python**：遵循 PEP 8 规范
- **命名**：
  - 文件/目录：`snake_case`（如 `ai_service.py`）
  - 类名：`PascalCase`（如 `AIService`）
  - 常量：`UPPER_CASE`（如 `DATABASE_URL`）

### 项目分层

```
app/
├── models/      # 数据模型层（SQLAlchemy ORM）
├── schemas/     # 数据验证层（Pydantic）
├── api/         # API 路由层（FastAPI Router）
├── services/    # 业务逻辑层
└── utils/       # 工具函数
```

### 认证流程

1. 调用 `POST /api/auth/login` 获取 JWT Token
2. 在请求头中添加 `Authorization: Bearer <token>`
3. 后端通过 `get_current_user` 依赖验证身份

---

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_api.py -v
```

### 测试 API

使用 Swagger UI 或 Postman 测试接口：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| `backend/README.md` | 后端服务详细文档 |
| `data/README.md` | 数据集构建文档 |
| `docs/数据库设计/ER 图.md` | 数据库 ER 图设计 |
| `docs/数据库设计/数据字典.md` | 详细表结构说明 |
| `01-数据库设计与搭建指南.md` | 数据库入门指南 |
| `02-FastAPI 后端框架搭建指南.md` | 后端搭建指南 |
| `03-AI 训练与知识库构建指南.md` | AI 训练指南 |
| `毕业设计组成说明文档.md` | 毕业设计整体说明 |

---

## 📈 项目状态（截至 2026-03-07）

### 已完成模块

| 模块 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| 数据库设计与搭建 | ✅ 完成 | 100% | 7 张表，含测试数据 |
| FastAPI 后端框架 | ✅ 完成 | 100% | 完整 CRUD API（40+ 接口） |
| 认证授权模块 | ✅ 完成 | 100% | JWT + 患者 Token + 用户注册/密码重置 + 微信登录 |
| AI 模型微调训练 | ✅ 完成 | 100% | LoRA 微调 500 条 |
| AI 服务部署 | ✅ 完成 | 100% | AutoDL RTX 4090 |
| 知识库构建 | ✅ 完成 | 100% | 804 条专业知识 |
| **微信小程序** | ✅ 完成 | 100% | **4 个页面，完整功能** |
| 后端 AI 集成 | ✅ 完成 | 100% | 对话/复诊/知识接口 |
| **Streamlit 后台** | ✅ 完成 | 100% | **6 个页面，完整功能** |
| 用户管理功能 | ✅ 完成 | 100% | 注册/重置密码（需 admin 确认） |

### 核心功能

| 功能 | 小程序端 | 医护后台 | 状态 |
|------|---------|---------|------|
| **用户认证** | 微信登录 | 账号密码登录 + 注册/重置密码 | ✅ 完成 |
| **AI 对话** | 智能咨询 | 对话监管 + 人工接管 + 清理 | ✅ 完成 |
| **复诊管理** | 查看复诊 + 确认/取消 | 创建/修改/删除 + 状态更新 | ✅ 完成 |
| **知识库** | 浏览查询 + 搜索 | 增删改查 + 分类管理 | ✅ 完成 |
| **数据统计** | - | 仪表盘可视化（7 个统计接口） | ✅ 完成 |
| **患者管理** | 个人信息完善 | 增删改查 + 筛选 | ✅ 完成 |
| **用户管理** | - | 注册/重置密码（需 admin 确认） | ✅ 完成 |

### 技术亮点

1. **AI 智能客服**
   - Qwen2.5-7B-Instruct 微调
   - RAG 检索增强生成
   - 牙科修复专业知识库（804 条）

2. **多端协同**
   - 微信小程序（患者端）
   - Streamlit Web（医护端）
   - FastAPI 后端（统一 API）

3. **安全机制**
   - JWT Token 认证
   - bcrypt 密码加密
   - 管理员权限验证（注册/重置密码）

4. **数据可视化**
   - 复诊趋势图
   - 对话量统计
   - 患者性别分布
   - 复诊状态分布

---

## ⚠️ 注意事项

1. **数据库**：首次运行前需确保 MySQL 数据库已创建并导入初始化数据
2. **端口占用**：如有端口冲突，运行 `stop_all.bat` 停止所有服务后重启
3. **JWT 密钥**：生产环境请修改 `SECRET_KEY` 为随机字符串
4. **AI 服务**：需配置 `AI_SERVICE_URL` 才能调用大模型
5. **密码安全**：所有密码使用 bcrypt 加密存储，不可逆

---

## 📞 常用命令

### 快速启动（推荐）

```bash
# 停止所有服务
stop_all.bat

# 启动后端服务
cd backend
start_server.bat

# 启动 Streamlit 后台
cd streamlit_app
start.bat
```

### 手动启动

```bash
# 启动 MySQL（Docker 方式）
docker start mysql-dental

# 启动后端服务（先配置 AI 服务地址）
cd backend
python start_server.py

# 或手动启动
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 启动 Streamlit
cd streamlit_app
venv\Scripts\activate
streamlit run app.py

# 运行测试
cd backend && pytest tests/ -v

# 查看 API 文档
# 浏览器访问：http://localhost:8000/docs

# 小程序开发
# 使用微信开发者工具打开 miniprogram 目录
```

### 测试数据重置

```bash
# 清空所有测试数据（ID 重新从 1 开始）
reset_test_data.bat
```

### 停止所有服务

```bash
# 强制停止所有 Python 进程
stop_all.bat
```

---

**最后更新**：2026 年 3 月 12 日
**文档版本**：v3.1（最终内容版）
**项目完成度**：100% ✅
