# 牙科修复领域训练数据集

## 📊 数据集概览

| 数据集 | 目标数据量 | 状态 |
|--------|----------|------|
| **知识库** | **1500 条** | ⏳ 等待《口腔修复学》PDF |
| **训练集** | **1000 条** | ⏳ 等待 PDF 后生成 |
| **验证集** | **150 条** | ⏳ 等待 PDF 后生成 |
| **测试集** | **150 条** | ⏳ 等待 PDF 后生成 |

**目标总量**：**1900 条**

---

## 📁 目录结构

```
data/
├── knowledge/               # 知识库目录 ✅
├── train/                   # 训练集目录 ✅
├── scripts/                 # 脚本目录 ✅
├── reference/               # 参考文档目录 ⏳ 等待 PDF
├── README.md                # 本文档
└── 数据集构建完成报告.md     # 构建报告（待更新）
```

---

## ⏳ 当前状态

**正在等待**：《口腔修复学》第 8 版 PDF 下载

**下载完成后**：
1. 将 PDF 保存到 `data/reference/` 文件夹
2. 读取 PDF 内容并提取专业知识
3. 生成 1500 条知识库数据
4. 生成 1000 条训练数据
5. 生成验证集和测试集
6. 更新本文档和构建报告

---

## 📝 数据格式

### 训练数据（Alpaca 格式）

```json
{
  "instruction": "你是一名专业的牙科修复 AI 智能客服助手...",
  "input": "种植牙术后多久可以刷牙？",
  "output": "种植牙术后 24 小时内不要刷牙..."
}
```

### 知识库数据

```json
{
  "category": "术后护理",
  "title": "种植牙术后 24 小时内注意事项",
  "content": "1. 不要刷牙，可用漱口水轻轻含漱\n2. 不要吐口水...",
  "keywords": "种植牙，术后 24 小时，注意事项",
  "source": "《口腔修复学》第 8 版"
}
```

---

## 📊 目标数据分布

### 知识库类别分布（目标）

| 类别 | 目标数量 | 占比 |
|------|----------|------|
| 术后护理 | 500 条 | 33.3% |
| 常见问题 | 400 条 | 26.7% |
| 修复类型 | 250 条 | 16.7% |
| 紧急情况 | 150 条 | 10.0% |
| 复诊规范 | 100 条 | 6.7% |
| 术前评估 | 50 条 | 3.3% |
| 材料选择 | 50 条 | 3.3% |

---

## 🔧 使用方法（生成后）

### 1. 导入知识库到 MySQL

```bash
cd D:\Project\毕业设计\data\scripts
python import_knowledge_to_mysql.py
```

### 2. 使用 LLaMA Factory 微调

```bash
cp data/train/dataset_info.json /path/to/LLaMA-Factory/data/
cp data/train/train_final.json /path/to/LLaMA-Factory/data/

llamafactory-cli train --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
    --dataset dental_knowledge --template qwen \
    --finetuning_type lora --lora_rank 8 \
    --num_train_epochs 3 --output_dir checkpoints/dental_qwen_lora
```

---

## 📚 数据来源

- **主要来源**：《口腔修复学》第 8 版（人民卫生出版社）
- **补充来源**：临床指南、专业文献、牙科诊所 FAQ

---

**数据版本**：v3.0（待生成）  
**创建日期**：2026 年 2 月 25 日  
**最后更新**：2026 年 2 月 25 日（等待 PDF 中）  
**适用对象**：牙科修复 AI 助手微调训练
