"""
根据知识库生成微调训练数据集
生成训练集、验证集、测试集（Alpaca 格式）
"""

import json
import random

# 设置随机种子，确保可重复性
random.seed(42)

# 读取知识库
print("正在读取知识库...")
with open('knowledge/knowledge_base_v3.json', 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

print(f"知识库总量：{len(knowledge_base)} 条")

# 系统提示词
SYSTEM_PROMPT = "你是一名专业的牙科修复 AI 智能客服助手。你的职责是为患者提供牙科修复术后的专业指导和咨询，回答关于复诊时间、术后护理、注意事项等问题。语气要友好、专业、易懂，体现关怀。对于紧急情况，建议立即就医。不提供诊断，只提供一般性建议。"

# 问题前缀（增加多样性）
QUESTION_PREFIXES = [
    "",
    "医生，",
    "请问，",
    "我想问一下，",
    "麻烦问一下，",
    "咨询一下，",
    "想请教一下，",
    "您好，",
]

# 回答前缀（增加多样性）
ANSWER_PREFIXES = [
    "",
    "您好，",
    "感谢您的咨询，",
    "很高兴为您解答，",
    "关于您的问题，",
]

# 回答后缀（增加多样性）
ANSWER_SUFFIXES = [
    "",
    "\n\n如有其他疑问，欢迎继续咨询。",
    "\n\n祝您早日康复！",
    "\n\n希望以上信息对您有帮助。",
    "\n\n建议您定期复查。",
]

# 从知识库生成问答对
def generate_qa_pairs(knowledge_item):
    """从单条知识库生成多个问答对"""
    qa_pairs = []
    
    category = knowledge_item['category']
    title = knowledge_item['title']
    content = knowledge_item['content']
    keywords = knowledge_item['keywords']
    
    # 从标题生成问题
    questions = []
    
    # 根据标题类型生成不同问法
    if "注意" in title or "事项" in title:
        questions.append(f"{title.replace('注意', '').replace('事项', '').strip()}需要注意什么？")
        questions.append(f"{title.replace('注意', '').replace('事项', '').strip()}的注意事项有哪些？")
    elif "处理" in title or "怎么办" in title:
        questions.append(f"{title.replace('处理', '').replace('怎么办', '').strip()}怎么处理？")
        questions.append(f"{title.replace('处理', '').replace('怎么办', '').strip()}怎么办？")
    elif "多久" in title or "时间" in title:
        questions.append(f"{title.replace('多久', '').replace('时间', '').strip()}需要多久？")
        questions.append(f"{title.replace('多久', '').replace('时间', '').strip()}要多长时间？")
    elif "价格" in title or "费用" in title:
        questions.append(f"{title.replace('价格', '').replace('费用', '').strip()}多少钱？")
        questions.append(f"{title.replace('价格', '').replace('费用', '').strip()}费用是多少？")
    elif "寿命" in title or "能用多久" in title:
        questions.append(f"{title.replace('寿命', '').replace('能用多久', '').strip()}能用多久？")
        questions.append(f"{title.replace('寿命', '').replace('能用多久', '').strip()}可以使用多少年？")
    elif "适合" in title or "什么人" in title:
        questions.append(f"{title.replace('适合', '').replace('什么人', '').strip()}适合什么人？")
        questions.append(f"{title.replace('适合', '').replace('什么人', '').strip()}的适应症有哪些？")
    elif "检查" in title or "项目" in title:
        questions.append(f"{title.replace('检查', '').replace('项目', '').strip()}需要做什么检查？")
        questions.append(f"{title.replace('检查', '').replace('项目', '').strip()}的检查项目有哪些？")
    elif "品牌" in title or "选择" in title:
        questions.append(f"{title.replace('品牌', '').replace('选择', '').strip()}有哪些品牌？")
        questions.append(f"{title.replace('品牌', '').replace('选择', '').strip()}应该怎么选择？")
    else:
        # 通用问法
        questions.append(f"{title}？")
        questions.append(f"关于{title}的问题")
        questions.append(f"{category}{title}？")
    
    # 为每个问题生成多个变体
    for base_q in questions[:2]:  # 每个知识库条目最多生成 2 个基础问题
        for prefix in QUESTION_PREFIXES[:3]:  # 3 种问题前缀
            question = f"{prefix}{base_q}".replace("？？", "？")
            
            # 生成回答变体
            for ans_prefix in ANSWER_PREFIXES[:2]:  # 2 种回答前缀
                for ans_suffix in ANSWER_SUFFIXES[:2]:  # 2 种回答后缀
                    answer = f"{ans_prefix}{content}{ans_suffix}".strip()
                    
                    qa_pairs.append({
                        "instruction": SYSTEM_PROMPT,
                        "input": question,
                        "output": answer,
                        "category": category
                    })
    
    return qa_pairs

# 生成所有问答对
print("正在生成问答对...")
all_qa_pairs = []
for item in knowledge_base:
    qa_pairs = generate_qa_pairs(item)
    all_qa_pairs.extend(qa_pairs)

print(f"生成问答对总数：{len(all_qa_pairs)} 条")

# 去重（基于 input）
seen_inputs = set()
unique_qa_pairs = []
for qa in all_qa_pairs:
    if qa['input'] not in seen_inputs:
        seen_inputs.add(qa['input'])
        unique_qa_pairs.append(qa)

print(f"去重后问答对总数：{len(unique_qa_pairs)} 条")

# 打乱数据
random.shuffle(unique_qa_pairs)

# 划分训练集、验证集、测试集（8:1:1）
total = len(unique_qa_pairs)
train_size = int(total * 0.8)
dev_size = int(total * 0.1)
test_size = total - train_size - dev_size

train_data = unique_qa_pairs[:train_size]
dev_data = unique_qa_pairs[train_size:train_size + dev_size]
test_data = unique_qa_pairs[train_size + dev_size:]

print(f"\n数据集划分:")
print(f"  训练集：{len(train_data)} 条 ({len(train_data)/total*100:.1f}%)")
print(f"  验证集：{len(dev_data)} 条 ({len(dev_data)/total*100:.1f}%)")
print(f"  测试集：{len(test_data)} 条 ({len(test_data)/total*100:.1f}%)")

# 保存数据集
print("\n正在保存数据集...")

# 保存训练集
with open('train/train_final.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, ensure_ascii=False, indent=2)
print(f"  [OK] 训练集已保存：train/train_final.json ({len(train_data)} 条)")

# 保存验证集
with open('train/dev_final.json', 'w', encoding='utf-8') as f:
    json.dump(dev_data, f, ensure_ascii=False, indent=2)
print(f"  [OK] 验证集已保存：train/dev_final.json ({len(dev_data)} 条)")

# 保存测试集
with open('train/test_final.json', 'w', encoding='utf-8') as f:
    json.dump(test_data, f, ensure_ascii=False, indent=2)
print(f"  [OK] 测试集已保存：train/test_final.json ({len(test_data)} 条)")

# 统计类别分布
print("\n各类别数据分布:")
category_count = {}
for qa in train_data:
    cat = qa['category']
    category_count[cat] = category_count.get(cat, 0) + 1

for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
    pct = count / len(train_data) * 100
    print(f"  {cat}: {count}条 ({pct:.1f}%)")

# 生成统计报告
stats = {
    "知识库总量": len(knowledge_base),
    "生成问答对总数": len(all_qa_pairs),
    "去重后问答对总数": len(unique_qa_pairs),
    "训练集": len(train_data),
    "验证集": len(dev_data),
    "测试集": len(test_data),
    "训练集类别分布": category_count
}

with open('train/dataset_stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)
print(f"\n  [OK] 统计报告已保存：train/dataset_stats.json")

print("\n" + "="*60)
print("数据集生成完成！")
print("="*60)
