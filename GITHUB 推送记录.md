# GitHub 推送记录

仓库地址：https://github.com/psllpsl/graduation-project.git

---

## 推送历史

### v3.1 - 2026-03-03（安全更新）✅

**提交信息：** security: 脱敏处理敏感信息

**更新内容:**
- ✅ 移除所有文档中的真实 AppID
- ✅ 移除 AutoDL 实例地址（使用占位符）
- ✅ 移除数据库密码示例
- ✅ 移除局域网 IP 地址
- ✅ 新增敏感信息说明.md
- ✅ 新增 sanitize_for_github.py 脱敏脚本

**文件变更:**
- 修改 21 个文档文件
- 新增 2 个文件

**提交哈希：** c867b2f

**推送状态：** ✅ 已推送到 GitHub

---

### v3.0 - 2026-03-03

**提交信息：** feat: 完成微信小程序前端开发

**更新内容:**
- ✅ 完成微信小程序 4 个核心页面（对话、复诊、知识、个人中心）
- ✅ 实现微信登录与 Token 管理
- ✅ 实现 AI 对话功能（支持快捷问题、会话历史）
- ✅ 实现复诊计划查看与状态管理
- ✅ 实现知识库浏览与搜索功能
- ✅ 优化后端接口（患者 Token 认证、公开接口）
- ✅ 优化 AI 提示词（名字：小齿，放宽输出限制）
- ✅ 实现真机测试配置（局域网 IP）
- ✅ 创建网络配置说明文档

**文件变更:**
- 新增 miniprogram/ 目录（完整小程序项目）
- 修改 backend/app/api/auth.py（添加 wx-login 接口）
- 修改 backend/app/api/patients.py（添加 by-openid 接口）
- 修改 backend/app/api/dialogues.py（添加 chat 接口）
- 修改 backend/app/api/knowledge.py（公开访问）
- 修改 backend/app/api/appointments.py（患者接口）
- 修改 backend/app/services/ai_service.py（提示词优化）
- 新增 backend/start_server.py（交互式启动脚本）
- 新增 backend/start.bat（一键启动）
- 新增 miniprogram/网络配置说明.md

**提交哈希：** d01ba8d

**推送状态：** ✅ 已推送到 GitHub

---

### v2.2 - 2026-02-28

**提交信息：** feat: 增强对话删除功能和 AI 服务稳定性

**更新内容:**
- 新增 4 个删除接口：删除单条对话/会话对话/患者对话/清空所有
- 改进 AutoDL API 调用：确保 URL 以/generate 结尾
- 添加详细的日志记录便于调试
- 优化 HTTP 异常处理机制
- 简化启动脚本，统一使用 Python 启动器

**文件变更:**
- 修改 backend/app/api/dialogues.py（新增 62 行删除接口代码）
- 修改 backend/app/services/ai_service.py（增强日志和异常处理）
- 修改 backend/start_server.bat（简化启动脚本）
- 新增 backend/start_server.py（Python 启动器）

**提交哈希：** 7912aa4

**推送状态：** ✅ 已推送到 GitHub

---

### v2.1 - 2026-02-27

**提交信息：** v2.1: 修正 AI 服务配置 + 文档更新

**更新内容:**
- 修正 backend/.env 中的 AI_SERVICE_URL
- 更新 backend/README.md（AI 服务配置）
- 新增 backend/AI 服务配置说明.md
- 新增 文档更新总结.md
- 删除测试脚本（test_ai_connection.py、test_dialogue.py）

**文件变更:**
- 修改 2 个文档文件
- 新增 2 个文档文件
- 删除 2 个测试文件

**推送状态：** ✅ 已推送到 GitHub

---

### v2.0 - 2026-02-27

**提交信息：** v2.0: 文档整理与 AI 部署更新

**更新内容:**
- 删除冗余文档校对报告（3 个）
- 删除 data 目录冗余报告（4 个）
- 更新 data/README.md（v6.2）
- 更新数据集构建完成报告（v6.2）
- 更新毕业设计组成说明文档

**文件变更:**
- 删除 7 个冗余文档
- 修改 2 个文档文件

**推送状态：** ⏳ 待推送

---

### v1.5 - 2026-02-26

**提交信息：** v1.5: 修正训练集数据量为 500 条

**修正内容:**
- 训练集数量：154 条 → 500 条（实际值）
- 更新 data/README.md
- 更新 data/数据集构建完成报告.md
- 更新 03-AI 训练与知识库构建指南.md
- 更新 毕业设计组成说明文档.md

**提交哈希：** 73d6998

**文件变更：**
- 修改 5 个文档文件
- +49 行，-51 行

**推送状态：** ✅ 已推送到 GitHub

---

### v1.4 - 2026-02-26

**提交信息：** v1.4: 根据实际内容更新所有文档

**更新内容：**
- 更新知识库数据量：804 条（实际值）
- 更新训练集数据量：154 条（实际值）
- 更新后端项目完成清单（PROJECT_COMPLETE.md）
- 更新数据集 README 和构建报告
- 更新毕业设计组成说明文档（添加当前项目状态）
- 更新三大指南文档（版本号更新至 v1.4）
- 添加 Redis 缓存技术说明
- 新增 .gitignore 规则（排除大文件 PDF）

**提交哈希：** 0faed1b

**文件变更：**
- 修改 8 个文档文件
- 新增 data/ 目录完整内容（知识库 804 条、训练集 154 条、脚本 15 个）
- 总计：32 个文件，+6948 行，-367 行

**推送状态：** ✅ 已推送到 GitHub

---

### v1.3 - 2026-02-25

**提交信息：** v1.3: 调整数据集目标，统一文档版本

**更新内容：**
- 知识库目标：800 条
- 训练集目标：150 条
- 更新所有相关文档（README、构建报告、指南等）
- 文档版本统一为 v1.3
- 新增 data/ 目录及数据集相关文件

**提交哈希：** 742cccf

**文件变更：**
- 新增 13 个文件
- 插入 32665 行，删除 9 行
- 新增 data/ 目录结构（知识库、训练集、脚本等）

**推送状态：** ✅ 已推送到 GitHub

---

### v1.1 - 2026-02-25

**提交信息：** v1.1: 更新推送记录文档

**更新内容：**
- 添加 GitHub 推送记录文档
- 用于追踪历史版本

**提交哈希：** 342c2ad

**推送状态：** ✅ 已推送到 GitHub

---

### v1.0 - 2026-02-25（初始版本）

**提交信息：** Initial commit: 毕业设计项目

**更新内容：**
- 项目初始上传
- 包含完整的后端代码（backend/）
- 数据库设计文档（docs/数据库设计/）
- 项目说明文档

**提交哈希：** 656ae6f

**文件数量：** 54 个文件

**推送状态：** ✅ 已推送到 GitHub

---

## 使用说明

### 推送更新

当需要推送新版本时，执行：

```bash
git add .
git commit -m "更新说明"
git push
```

### 查看历史版本

```bash
# 查看提交历史
git log --oneline

# 查看某个版本的详情
git show <commit-hash>

# 切换到某个历史版本
git checkout <commit-hash>
```

### 版本对比

```bash
# 对比两个版本
git diff <commit-hash-1> <commit-hash-2>

# 对比当前工作区与上次提交
git diff HEAD
```

---

## 版本标签（可选）

如需给重要版本打标签：

```bash
# 创建标签
git tag -a v1.0 -m "初始版本"

# 推送标签到 GitHub
git push origin v1.0
```

---

## 当前状态

**本地版本**：v3.1
**远程版本**：v3.1
**待推送**：无

**安全状态**：✅ 已脱敏处理

**文档清单**（14 个核心文档）：
- 毕业设计组成说明文档.md (v2.1)
- 01-数据库设计与搭建指南.md (v1.4)
- 02-FastAPI 后端框架搭建指南.md (v1.4)
- 03-AI 训练与知识库构建指南.md (v2.0)
- GITHUB 推送记录.md (v3.0)
- 文档更新总结.md (v1.0)
- 文档整理报告.md (v1.0)
- QWEN.md (v2.0)
- backend/README.md (v1.2)
- backend/PROJECT_COMPLETE.md (v1.2)
- backend/AI 服务配置说明.md (v1.0)
- backend/启动说明.md (v1.0)
- data/README.md (v6.2)
- data/数据集构建完成报告.md (v6.2)
- docs/数据库设计/数据字典.md (v1.0)
- docs/数据库设计/ER 图.md (v1.0)
- miniprogram/README.md (v1.0)
- miniprogram/开发记录.md (v1.0)
- miniprogram/网络配置说明.md (v1.0)
