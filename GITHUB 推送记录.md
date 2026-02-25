# GitHub 推送记录

仓库地址：https://github.com/psllpsl/graduation-project.git

---

## 推送历史

### v1.1 - 2026-02-25

**提交信息：** v1.0: 添加 GitHub 推送记录文档

**更新内容：**
- 添加 GitHub 推送记录文档，用于追踪历史版本

**提交哈希：** aa12b19

---

### v1.0 - 2026-02-25（初始版本）

**提交信息：** Initial commit: 毕业设计项目

**更新内容：**
- 项目初始上传
- 包含完整的后端代码（backend/）
- 数据库设计文档（docs/数据库设计/）
- 项目说明文档

**文件清单：**
- backend/ - FastAPI 后端项目
  - app/ - 应用主代码
  - tests/ - 测试文件
  - requirements.txt - 依赖列表
- docs/数据库设计/ - 数据库相关文档
  - ER 图.md
  - create_tables.sql
  - init_data.sql
  - 数据字典.md
- 根目录文档
  - 01-数据库设计与搭建指南.md
  - 02-FastAPI 后端框架搭建指南.md
  - 毕业设计组成说明文档.md
  - 文档校对与更新报告.md
  - 《毕业设计（论文）开题报告》.txt

**提交哈希：** 656ae6f

**文件数量：** 54 个文件

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
