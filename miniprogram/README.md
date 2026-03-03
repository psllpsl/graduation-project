# 牙科修复复诊助手 - 微信小程序

> 基于 AI 智能客服的牙科修复复诊提醒与管理系统 - 患者端

---

## 📋 项目概述

本小程序是牙科修复复诊提醒与管理系统患者端，提供 7×24 小时智能术后随访服务。

### 核心功能

| 功能模块 | 说明 |
|----------|------|
| **AI 智能对话** | 与 AI 助手进行自然语言对话，咨询术后问题 |
| **复诊计划** | 查看个人复诊时间表、确认/取消复诊 |
| **术后知识** | 浏览牙科修复相关知识和注意事项 |
| **个人中心** | 个人信息管理、订阅消息提醒 |

---

## 🚀 快速开始

### 1. 环境准备

- **微信开发者工具**：https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html
- **基础库版本**：3.3.4 或更高
- **Node.js**：14.x 或更高（可选，用于使用 npm 包）

### 2. 导入项目

1. 打开微信开发者工具
2. 点击「+」→「导入项目」
3. 选择项目目录：`D:\Project\毕业设计\miniprogram`
4. 填写 AppID（测试账号可使用测试号）
5. 点击「导入」

### 3. 配置后端地址

编辑 `app.js`，修改 `baseUrl` 配置：

```javascript
globalData: {
  // 修改为你的后端 API 地址
  baseUrl: 'http://localhost:8000/api',
  // ...
}
```

**注意**：
- 开发环境可使用 `http://localhost:8000/api`
- 需要在微信公众平台配置服务器域名
- 真机测试时需使用公网 IP 或内网穿透工具

### 4. 编译运行

1. 点击「编译」按钮
2. 在模拟器中查看效果
3. 使用「真机调试」在手机上测试

---

## 📁 项目结构

```
miniprogram/
├── app.js                    # 小程序入口文件
├── app.json                  # 全局配置
├── app.wxss                  # 全局样式
├── project.config.json       # 项目配置
├── sitemap.json              # 搜索配置
├── images/                   # 图片资源
│   └── README.md            # 图标说明
├── pages/                    # 页面目录
│   ├── index/               # 对话主界面
│   │   ├── index.wxml
│   │   ├── index.wxss
│   │   ├── index.js
│   │   └── index.json
│   ├── profile/             # 个人中心
│   │   ├── profile.wxml
│   │   ├── profile.wxss
│   │   ├── profile.js
│   │   └── profile.json
│   ├── appointment/         # 复诊计划
│   │   ├── appointment.wxml
│   │   ├── appointment.wxss
│   │   ├── appointment.js
│   │   └── appointment.json
│   └── knowledge/           # 术后知识
│       ├── knowledge.wxml
│       ├── knowledge.wxss
│       ├── knowledge.js
│       └── knowledge.json
├── utils/                    # 工具模块
│   ├── api.js               # API 请求封装
│   └── util.js              # 通用工具函数
├── components/               # 自定义组件（可选）
│   └── chat/                # 聊天组件
├── SUBSCRIBE_MESSAGE.md     # 订阅消息配置指南
└── README.md                # 本文档
```

---

## 🎨 页面说明

### 1. 对话页面（pages/index）

**功能**：
- AI 智能对话
- 快捷问题
- 多轮对话上下文
- 消息历史记录

**接口**：
- `POST /api/dialogues` - 发送消息
- `GET /api/dialogues/session/{sessionId}` - 获取会话历史

### 2. 复诊计划（pages/appointment）

**功能**：
- 复诊列表展示
- 复诊状态统计
- 确认/取消复诊
- 复诊详情查看

**接口**：
- `GET /api/appointments/patient/{patientId}` - 获取复诊列表
- `PUT /api/appointments/{id}/status` - 更新复诊状态

### 3. 术后知识（pages/knowledge）

**功能**：
- 知识分类浏览
- 知识搜索
- 知识详情查看

**接口**：
- `GET /api/knowledge` - 获取知识列表
- `GET /api/knowledge/categories` - 获取分类列表
- `GET /api/knowledge/search` - 搜索知识

### 4. 个人中心（pages/profile）

**功能**：
- 微信登录授权
- 个人信息展示
- 订阅消息提醒
- 退出登录

**接口**：
- `POST /api/auth/wx-login` - 微信登录
- `GET /api/auth/me` - 获取用户信息

---

## 🔧 配置说明

### AppID 配置

在 `project.config.json` 中修改：

```json
{
  "appid": "your-appid-here",
  // ...
}
```

### 服务器域名配置

在微信公众平台配置：

1. 登录 https://mp.weixin.qq.com/
2. 开发 → 开发管理 → 开发设置
3. 服务器域名配置：
   - request 合法域名：`https://your-domain.com`
   - socket 合法域名：`wss://your-domain.com`
   - uploadFile 合法域名：`https://your-domain.com`
   - downloadFile 合法域名：`https://your-domain.com`

### 订阅消息模板

参考 `SUBSCRIBE_MESSAGE.md` 文档配置订阅消息。

---

## 🧪 测试

### 开发环境测试

```bash
# 1. 启动后端服务
cd ../backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload

# 2. 在微信开发者工具中编译
# 3. 使用真机调试功能
```

### 测试账号

可使用微信提供的测试账号：
- 测试号管理：https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo/list

---

## 📦 构建与发布

### 1. 代码上传

在微信开发者工具中：
1. 点击右上角「上传」
2. 填写版本号和备注
3. 点击「上传」

### 2. 提交审核

1. 登录微信公众平台
2. 版本管理 → 开发版本 → 选择版本 → 提交审核

### 3. 发布上线

审核通过后：
1. 版本管理 → 审核版本 → 发布

---

## ⚠️ 注意事项

### 开发规范

1. **代码规范**：遵循微信小程序开发规范
2. **命名规范**：
   - 文件名：`kebab-case`（如 `user-info.js`）
   - 变量名：`camelCase`
   - 常量名：`UPPER_CASE`

### 性能优化

1. **图片优化**：
   - 使用合适的图片格式（PNG/WebP）
   - 控制图片大小（单张不超过 40KB）
   - 使用 CDN 托管大图

2. **分包加载**（后续优化）：
   - 将不常用页面分包
   - 主包大小控制在 2MB 以内

3. **数据缓存**：
   - 使用 `wx.setStorage` 缓存常用数据
   - 合理使用下拉刷新和上拉加载

### 安全注意

1. **敏感信息**：
   - 不要在前端存储敏感信息
   - 使用后端进行数据验证
   - 使用 HTTPS 传输数据

2. **用户隐私**：
   - 遵循微信小程序隐私保护规范
   - 明确告知用户信息使用目的
   - 提供用户信息删除渠道

---

## 🆘 常见问题

### Q1: 真机调试时无法连接后端？

**A**: 
- 确保手机和电脑在同一局域网
- 使用电脑 IP 地址替代 localhost
- 检查防火墙设置

### Q2: 订阅消息无法发送？

**A**: 
- 检查模板 ID 是否正确
- 确认用户已授权订阅
- 检查 Access Token 是否有效

### Q3: 对话界面卡顿？

**A**: 
- 减少单次加载的消息数量
- 使用虚拟列表优化长列表
- 优化图片加载

---

## 📚 参考资料

- [微信小程序官方文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [微信开放社区](https://developers.weixin.qq.com/community/)
- [小程序设计指南](https://developers.weixin.qq.com/miniprogram/design/)

---

## 📝 开发日志

| 日期 | 内容 | 开发者 |
|------|------|--------|
| 2026-03-03 | 项目初始化，完成基础框架 | - |
| 2026-03-03 | 完成对话页面开发 | - |
| 2026-03-03 | 完成复诊计划页面开发 | - |
| 2026-03-03 | 完成知识库页面开发 | - |
| 2026-03-03 | 完成个人中心页面开发 | - |

---

**版本**：v1.0.0
**创建日期**：2026 年 3 月 3 日
**最后更新**：2026 年 3 月 3 日
