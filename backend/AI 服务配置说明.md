# 后端 AI 服务配置说明

## 📝 当前配置（截至 2026-02-27）

### AutoDL 服务地址

```env
AI_SERVICE_URL=https://uu769760-b58d-861e482d.bjb1.seetacloud.com:8443/generate
```

**重要**：
- 实例 ID：`uu769760-b58d-861e482d`（两个 `u`，不是 `u769760`）
- 内网端口：`6008`
- 外网端口：`8443`
- API 路径：`/generate`

### 完整配置

```env
# AI 服务配置
AI_SERVICE_URL=https://uu769760-b58d-861e482d.bjb1.seetacloud.com:8443/generate
AI_SERVICE_TYPE=autodl
AI_MAX_TOKENS=150
AI_TEMPERATURE=0.7
AI_TIMEOUT_SECONDS=60
```

---

## 🚀 AutoDL 部署步骤

### 1. 上传文件到 AutoDL

上传以下文件到 `/root/autodl-tmp/`：
- `start_tr.sh` - 启动脚本
- `start_inference.py` - 推理服务

### 2. 启动服务

```bash
chmod +x start_tr.sh
bash start_tr.sh
```

### 3. 配置自定义服务

在 AutoDL 控制台：
1. 进入实例详情
2. 点击"自定义服务"
3. 添加服务：内网端口 `6008`，协议 `HTTP`
4. 复制生成的公网 URL（如：`https://uu769760-b58d-861e482d.bjb1.seetacloud.com:8443`）

### 4. 测试服务

```bash
# 本地测试
curl http://localhost:6008/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "种植牙术后多久能吃饭？", "max_tokens": 150}'

# 公网测试
curl https://uu769760-b58d-861e482d.bjb1.seetacloud.com:8443/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "种植牙术后多久能吃饭？", "max_tokens": 150}'
```

### 5. 更新后端配置

编辑 `backend/.env`：
```env
AI_SERVICE_URL=https://你的实例地址:端口/generate
```

---

## 🧪 测试方法

### Swagger UI 测试

1. 启动后端：`python -m uvicorn app.main:app --reload`
2. 访问：http://localhost:8000/docs
3. 登录获取 Token
4. 调用 `POST /api/dialogues/` 接口

### 命令行测试

```bash
# 登录
curl http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "admin123"}'

# 对话
curl http://localhost:8000/api/dialogues/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -d '{"patient_id": 1, "session_id": "test_001", "user_message": "种植牙术后多久能吃饭？", "message_type": "consultation"}'
```

---

## 📊 服务架构

```
微信小程序 → FastAPI 后端 → AutoDL AI 服务
              ↓
         MySQL 数据库
```

**对话流程**：
1. 小程序发送用户问题
2. 后端接收请求，获取对话历史（最近 3 轮）
3. 检索相关知识（从知识库表）
4. 构建 System Prompt
5. 调用 AutoDL API
6. 后处理 AI 回复（截断、清理、移除追问）
7. 保存到数据库并返回

---

## ⚠️ 常见问题

### Q: 404 错误

**原因**：URL 错误或自定义服务未配置

**解决**：
1. 确认 URL 格式：`https://实例 ID.seetacloud.com:端口/generate`
2. 检查 AutoDL 自定义服务是否添加
3. 测试本地服务：`curl http://localhost:6008/generate`

### Q: 连接超时

**原因**：服务未运行或网络问题

**解决**：
1. 检查 AutoDL 服务：`ps aux | grep python`
2. 重启服务：`bash start_tr.sh`
3. 检查防火墙设置

### Q: 返回默认回复

**原因**：AI 服务调用失败

**解决**：
1. 检查 `.env` 中的 `AI_SERVICE_URL`
2. 测试连接：`curl 你的 URL/generate`
3. 查看后端日志

---

**更新时间**：2026 年 2 月 27 日
