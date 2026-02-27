# AI 模型文件说明

## ⚠️ 重要提示

**本目录包含的 AI 模型文件过大，无法上传到 GitHub。**

- **基座模型**（Qwen2.5-7B-Instruct）：约 14GB
- **LoRA 权重**：约 330MB
- **合并后模型**：约 14GB

---

## 📥 如何获取模型文件

### 方式一：从 ModelScope 下载（推荐）

```bash
# 安装 ModelScope
pip install modelscope

# 下载 Qwen2.5-7B-Instruct 基座模型
python -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen2.5-7B-Instruct', cache_dir='./data/models')"
```

**ModelScope 页面**：https://modelscope.cn/models/Qwen/Qwen2.5-7B-Instruct

---

### 方式二：从 HuggingFace 下载

```bash
# 使用 git clone
git lfs install
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct ./data/models/Qwen/Qwen2.5-7B-Instruct
```

**HuggingFace 页面**：https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

---

### 方式三：使用自己的微调权重

如果你已经进行了 LoRA 微调：

1. **从 AutoDL 下载**：
   ```bash
   # 在 AutoDL 上压缩模型
   tar -czf dental_qwen_merged.tar.gz ./checkpoints/dental_qwen_lora/
   
   # 下载到本地
   # 使用 AutoDL 文件传输工具或 SCP
   ```

2. **放置位置**：
   ```
   data/
   └── models/
       └── dental_qwen_merged/    # 你的微调后模型
   ```

---

## 📁 推荐的目录结构

```
data/
├── models/
│   ├── Qwen/
│   │   └── Qwen2.5-7B-Instruct/    # 基座模型（自行下载）
│   │       ├── config.json
│   │       ├── model.safetensors
│   │       └── ...
│   └── dental_qwen_merged/          # 微调后模型（可选）
├── checkpoints/
│   └── dental_qwen_lora/            # LoRA 权重（可选）
├── knowledge/
│   └── knowledge_base_v3.json       # ✅ 已上传（知识库）
└── train/
    └── train.json                   # ✅ 已上传（训练集）
```

---

## ✅ 已上传到 GitHub 的文件

以下文件**已经上传**到 GitHub，可以直接使用：

| 文件 | 大小 | 说明 |
|------|------|------|
| `data/knowledge/knowledge_base_v3.json` | ~500KB | 804 条知识库 |
| `data/train/train.json` | ~300KB | 500 条训练集 |
| `data/scripts/*.py` | ~50KB | 数据处理脚本 |
| `backend/app/services/ai_service.py` | ~15KB | AI 服务代码 |

---

## ❌ 未上传到 GitHub 的文件

以下文件**没有上传**（太大），需要自行准备：

| 文件/目录 | 大小 | 说明 |
|-----------|------|------|
| `data/models/Qwen/` | ~14GB | 基座模型 |
| `data/models/dental_qwen_merged/` | ~14GB | 微调后模型 |
| `data/checkpoints/` | ~330MB | LoRA 权重 |
| `data/*.tar.gz` | ~14GB | 模型压缩包 |

---

## 🔧 使用模型前的准备

### 1. 确认模型文件到位

```bash
# 检查基座模型
ls data/models/Qwen/Qwen2.5-7B-Instruct/config.json

# 检查微调模型（如果有）
ls data/models/dental_qwen_merged/config.json
```

### 2. 配置 AutoDL 部署

如果使用 AutoDL 部署：

1. 上传模型到 AutoDL
2. 启动推理服务
3. 配置后端 `.env` 文件：
   ```env
   AI_SERVICE_URL=https://你的 autodl 地址/generate
   ```

### 3. 本地测试（可选）

如果要在本地运行模型（需要大显存 GPU）：

```bash
cd backend
python test_autodl_connection.py
```

---

## 💡 常见情况

### 情况 1：只做毕业设计，不需要微调

**只需下载基座模型**：
```bash
python -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen2.5-7B-Instruct', cache_dir='./data/models')"
```

然后部署到 AutoDL 即可。

---

### 情况 2：已经微调完成

**下载你的微调权重**：
1. 从 AutoDL 下载 `checkpoints/dental_qwen_lora/`
2. 合并 LoRA 权重到基座模型
3. 部署合并后的模型

---

### 情况 3：只想测试后端功能

**不需要本地模型**！只需要：
1. 配置 AutoDL 部署（模型在 AutoDL 上）
2. 配置后端 `.env` 文件的 `AI_SERVICE_URL`
3. 直接测试 API

---

## 📊 GitHub 存储限制

| 限制类型 | 数值 | 说明 |
|----------|------|------|
| 单文件大小限制 | 100MB | 超过无法上传 |
| 仓库建议大小 | <1GB | 超过会被警告 |
| Git LFS 免费额度 | 1GB | 超过需付费 |

**结论**：AI 模型文件（14GB）绝对不能上传到 GitHub！

---

## 📝 文档引用

在毕业论文中引用模型：

```bibtex
@misc{qwen2.5,
  title={Qwen2.5-7B-Instruct},
  author={Alibaba Cloud},
  year={2024},
  url={https://huggingface.co/Qwen/Qwen2.5-7B-Instruct}
}
```

---

**最后更新**: 2026 年 2 月 27 日
**适用对象**：需要使用本项目的开发者、答辩评委
