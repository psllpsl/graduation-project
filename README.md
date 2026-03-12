# 牙科修复复诊提醒与管理系统 - 最终版本

> **项目名称**：基于 AI 智能客服的牙科修复复诊提醒与管理系统
> **版本**：v3.1
> **完成日期**：2026 年 3 月 12 日
> **项目状态**：✅ 全部完成

---

## 📁 文件夹结构

```
最终内容/
├── backend/                    # FastAPI 后端服务
│   ├── app/                   # 应用源代码
│   ├── tests/                 # 测试文件
│   ├── requirements.txt       # Python 依赖
│   └── README.md              # 后端说明
├── streamlit_app/             # Streamlit 医护后台
│   ├── pages/                 # 多页面应用
│   ├── utils/                 # 工具模块
│   ├── requirements.txt       # Python 依赖
│   └── README.md              # 后台说明
├── miniprogram/               # 微信小程序患者端
│   ├── pages/                 # 4 个核心页面
│   ├── utils/                 # 工具模块
│   └── README.md              # 小程序说明
├── data/                      # 数据集
│   ├── knowledge/             # 知识库（804 条）
│   ├── train/                 # 训练集（500 条）
│   └── README.md              # 数据集说明
├── docs/                      # 数据库设计文档
│   └── 数据库设计/            # ER 图、数据字典、SQL 脚本
├── QWEN.md                    # 项目上下文文档
├── 完整部署与使用指南.md       # 部署和使用说明
├── 毕业设计组成说明文档.md     # 系统组成说明
├── 项目完成总结.md             # 项目总结
├── 测试报告.md                 # 系统测试报告
├── 指导日志.md                 # 教师指导记录
├── 更新日志.md                 # 版本更新记录
├── GITHUB 推送记录.md          # GitHub 推送历史
├── .gitignore                 # Git 忽略文件配置
├── stop_all.bat               # 停止所有服务
├── reset_test_data.bat        # 重置测试数据
└── requirements.txt           # 后端依赖
```

---

## 🚀 快速开始

### 1. 环境准备

**Python 版本**：3.10+
**数据库**：MySQL 8.0+
**缓存**：Redis 6.0+

### 2. 安装依赖

```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# Streamlit 后台依赖
cd ../streamlit_app
pip install -r requirements.txt
```

### 3. 配置数据库

```bash
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE dental_clinic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 导入表结构
USE dental_clinic;
SOURCE docs/数据库设计/create_tables.sql;

# 导入测试数据
SOURCE docs/数据库设计/init_data.sql;
```

### 4. 启动服务

```bash
# 停止所有旧进程
stop_all.bat

# 启动后端
cd backend
start_server.bat

# 启动 Streamlit 后台（新窗口）
cd ../streamlit_app
start.bat
```

### 5. 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **后端 API** | http://localhost:8000/docs | API 文档 |
| **Streamlit** | http://localhost:8501 | 医护后台 |
| **小程序** | 微信开发者工具 | 患者端 |

### 6. 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| doctor_zhang | admin123 | 医生 |
| doctor_li | admin123 | 护士 |

---

## 📊 核心数据

| 项目 | 数量 |
|------|------|
| **后端 API 接口** | 45+ |
| **Streamlit 页面** | 6 |
| **小程序页面** | 4 |
| **数据库表** | 7 |
| **知识库条目** | 804 |
| **训练数据** | 500 |
| **代码行数** | ~6000 |

---

## 🎯 功能特性

### 后端 API
- ✅ 用户认证（JWT + 微信登录 + 注册/重置密码）
- ✅ 患者管理（CRUD + 搜索 + 信息完善）
- ✅ 复诊管理（CRUD + 状态更新 + 患者确认/取消）
- ✅ 对话管理（AI 对话 + 人工接管 + 删除功能）
- ✅ 知识库（CRUD + 分类搜索）
- ✅ 数据统计（7 个统计接口）

### Streamlit 后台
- ✅ 仪表盘（数据可视化）
- ✅ 患者管理
- ✅ 复诊管理
- ✅ 对话监管
- ✅ 知识库管理
- ✅ 系统设置

### 微信小程序
- ✅ AI 对话（智能咨询）
- ✅ 复诊查看（确认/取消）
- ✅ 知识浏览（搜索/分类）
- ✅ 个人中心

---

## 📝 重要说明

### 微信配置

编辑 `backend/app/api/auth.py`，配置微信 AppID 和 AppSecret：

```python
# 微信配置（需要在微信公众平台获取）
appid = "wxYOUR_APPID_HERE"  # 替换为你的小程序 AppID
secret = "YOUR_SECRET_HERE"  # 替换为你的小程序 AppSecret
```

**获取测试账号**：https://developers.weixin.qq.com/miniprogram/dev/devtools/sandbox.html

### 小程序网络配置

编辑 `miniprogram/app.js`，修改 `baseUrl`：

```javascript
globalData: {
    baseUrl: 'http://你的电脑 IP:8000/api'
}
```

---

## 📚 文档说明（答辩必需）

| 文档 | 用途 |
|------|------|
| **QWEN.md** | 项目上下文文档（技术字典） |
| **完整部署与使用指南.md** | 详细部署和使用说明 |
| **毕业设计组成说明文档.md** | 系统组成和开发步骤 |
| **项目完成总结.md** | 项目整体总结 |
| **测试报告.md** | 系统测试报告（104 个用例） |
| **指导日志.md** | 教师指导记录（8 次） |
| **更新日志.md** | 版本更新记录 |
| **GITHUB 推送记录.md** | GitHub 推送历史 |
| **.gitignore** | Git 忽略文件配置 |

---

## ⚠️ 注意事项

1. **虚拟环境**：`backend/venv` 和 `streamlit_app/venv` 未包含，请自行创建
2. **敏感信息**：代码中使用占位符，请自行配置真实值
3. **AI 服务**：AI 模型已部署到 AutoDL，需自行配置或使用本地模型
4. **数据库密码**：请根据实际情况修改配置

---

## 📞 常用命令

```bash
# 停止所有服务
stop_all.bat

# 重置测试数据
reset_test_data.bat

# 查看 API 文档
# 浏览器访问：http://localhost:8000/docs
```

---

**最后更新**：2026 年 3 月 12 日
**文档版本**：v3.1
**项目完成度**：100% ✅
