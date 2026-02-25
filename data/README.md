# 牙科修复领域训练数据集

## 📊 数据集概览

| 数据集 | 文件位置 | 数据量 | 用途 |
|--------|----------|--------|------|
| **知识库** | `knowledge/knowledge_base_v3.json` | **1500 条** | MySQL 导入、RAG 检索、模型微调 |
| **训练集** | `train/train_final.json` | **1000 条** | 模型微调训练 |
| **验证集** | `train/dev_final.json` | **150 条** | 训练过程验证 |
| **测试集** | `train/test_final.json` | **150 条** | 模型效果评估 |

**数据总量**：**1900 条**

---

## 📁 目录结构

```
data/
├── knowledge/
│   └── knowledge_base_v3.json       # 知识库（1500 条）
├── train/
│   ├── train_final.json             # 训练集（1000 条）
│   ├── dev_final.json               # 验证集（150 条）
│   ├── test_final.json              # 测试集（150 条）
│   └── dataset_info.json            # LLaMA Factory 配置
├── scripts/
│   ├── generate_training_data.py    # 训练数据生成脚本
│   └── import_knowledge_to_mysql.py # MySQL 导入脚本
├── README.md                        # 本文档
└── 数据集构建完成报告.md             # 构建报告
```

---

## 📝 数据格式

### 训练数据（Alpaca 格式）

```json
{
  "instruction": "你是一名专业的牙科修复 AI 智能客服助手。你的职责是为患者提供牙科修复术后的专业指导和咨询，回答关于复诊时间、术后护理、注意事项等问题。语气要友好、专业、易懂，体现关怀。对于紧急情况，建议立即就医。不提供诊断，只提供一般性建议。",
  "input": "种植牙术后多久可以刷牙？",
  "output": "种植牙术后 24 小时内不要刷牙，可用医生开的漱口水轻轻漱口。24 小时后可以正常刷牙，但要避开手术区域，动作要轻柔。建议使用软毛牙刷，刷牙时不要用力过猛。术后 1 周内可以使用冲牙器低档位清洁，但避免直接冲洗伤口。\n\n如有其他疑问，欢迎继续咨询。"
}
```

### 知识库数据

```json
{
  "category": "术后护理",
  "title": "种植牙术后 24 小时内注意事项",
  "content": "1. 不要刷牙，可用漱口水轻轻含漱\n2. 不要吐口水，有唾液或血液请咽下\n3. 不要吮吸伤口或用舌头舔伤口\n4. 轻咬纱布卷 30-60 分钟后吐出\n5. 冰敷手术侧面部，每次 15-20 分钟\n6. 不要饮酒、吸烟\n7. 不要剧烈运动\n8. 睡觉时垫高枕头\n9. 按医嘱服用药物\n10. 如有异常及时联系医生",
  "keywords": "种植牙，术后 24 小时，注意事项",
  "source": "《口腔修复学》第 8 版"
}
```

---

## 📊 数据分布

### 知识库类别分布

| 类别 | 数据量 | 占比 |
|------|--------|------|
| 术后护理 | 500 条 | 33.3% |
| 常见问题 | 400 条 | 26.7% |
| 修复类型 | 250 条 | 16.7% |
| 紧急情况 | 150 条 | 10.0% |
| 复诊规范 | 100 条 | 6.7% |
| 术前评估 | 50 条 | 3.3% |
| 材料选择 | 50 条 | 3.3% |

### 训练集质量

| 指标 | 数值 |
|------|------|
| 数据量 | 1000 条 |
| 唯一问题数 | 400+ 种 |
| 数据重复率 | < 5% |

---

## 🔧 使用方法

### 1. 导入知识库到 MySQL

```bash
# 1. 编辑脚本，修改数据库配置
# 文件：scripts/import_knowledge_to_mysql.py

# 2. 执行导入
cd D:\Project\毕业设计\data\scripts
python import_knowledge_to_mysql.py
```

### 2. 使用 LLaMA Factory 微调

```bash
# 复制配置和数据
cp data/train/dataset_info.json /path/to/LLaMA-Factory/data/
cp data/train/train_final.json /path/to/LLaMA-Factory/data/

# 启动训练
llamafactory-cli train \
    --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
    --dataset dental_knowledge \
    --template qwen \
    --finetuning_type lora \
    --lora_rank 8 \
    --num_train_epochs 3 \
    --output_dir checkpoints/dental_qwen_lora
```

---

## ✅ 数据质量

- **医学准确性**：基于《口腔修复学》第 8 版
- **问题多样性**：400+ 种唯一问题表达
- **低重复率**：< 5%
- **类别完整**：7 大类全覆盖

---

**数据版本**：v3.0  
**创建日期**：2026 年 2 月 25 日  
**最后更新**：2026 年 2 月 25 日  
**适用对象**：牙科修复 AI 助手微调训练
