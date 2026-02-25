"""
从知识库生成训练数据集
生成 2000+ 条高质量、低重复的训练数据
"""

import json
import random

# 加载知识库数据
with open("D:/Project/毕业设计/data/knowledge/knowledge_base_v3.json", 'r', encoding='utf-8') as f:
    knowledge_base = json.load(f)

print(f"加载知识库数据：{len(knowledge_base)} 条")

# 系统提示词
SYSTEM_PROMPT = "你是一名专业的牙科修复 AI 智能客服助手。你的职责是为患者提供牙科修复术后的专业指导和咨询，回答关于复诊时间、术后护理、注意事项等问题。语气要友好、专业、易懂，体现关怀。对于紧急情况，建议立即就医。不提供诊断，只提供一般性建议。"

# 问题变化前缀（15 种）
QUESTION_PREFIXES = [
    "", "医生，", "请问，", "我想问一下，", "麻烦问一下，",
    "咨询一下，", "想请教一下，", "您好，", "问一下，", "问问，",
    "请教一下，", "询问一下，", "想了解，", "想知道，", "求助，"
]

# 问题变化后缀（10 种）
QUESTION_SUFFIXES = [
    "", "？", "吗？", "呢？", "啊？", "呀？", "的吧？", "是吗？", "对吗？", "怎么样？"
]

# 回答前缀（10 种）
ANSWER_PREFIXES = [
    "", "您好，", "感谢您的咨询，", "很高兴为您解答，", "关于您的问题，",
    "我来为您详细解答，", "感谢您提问，", "您好！很高兴为您解答，", "感谢您的信任，", "您好！关于这个问题，"
]

# 回答后缀（10 种）
ANSWER_SUFFIXES = [
    "", "\n\n如有其他疑问，欢迎继续咨询。", "\n\n祝您早日康复！", "\n\n希望以上信息对您有帮助。",
    "\n\n建议您定期复查。", "\n\n如有不适请及时联系医生。", "\n\n请严格遵照医嘱。",
    "\n\n如有问题随时联系我们。", "\n\n祝您口腔健康！", "\n\n感谢您的信任与支持。"
]

# 从标题生成问题
def generate_questions(title, category):
    questions = []
    
    # 基础问题
    base = title.rstrip("注意指南处理时间费用寿命周期")
    
    # 根据关键词生成问题
    if "注意" in title:
        questions.append(f"{base}需要注意什么？")
        questions.append(f"{base}的注意事项有哪些？")
        questions.append(f"{base}有什么禁忌？")
    elif "处理" in title or "紧急" in title:
        questions.append(f"{base}怎么处理？")
        questions.append(f"{base}怎么办？")
        questions.append(f"遇到{base}情况怎么办？")
    elif "指南" in title:
        questions.append(f"{base}怎么做？")
        questions.append(f"{base}的方法？")
        questions.append(f"如何进行{base}？")
    elif "时间" in title or "周期" in title:
        questions.append(f"{base}需要多久？")
        questions.append(f"{base}要多长时间？")
        questions.append(f"{base}什么时候？")
    elif "费用" in title or "价格" in title:
        questions.append(f"{base}多少钱？")
        questions.append(f"{base}费用是多少？")
        questions.append(f"{base}贵吗？")
    elif "寿命" in title or "使用" in title:
        questions.append(f"{base}能用多久？")
        questions.append(f"{base}可以用多少年？")
        questions.append(f"{base}耐用吗？")
    elif "疼痛" in title or "疼" in title:
        questions.append(f"{base}疼不疼？")
        questions.append(f"{base}痛吗？")
        questions.append(f"{base}会痛吗？")
    elif "感染" in title or "发炎" in title:
        questions.append(f"{base}有什么症状？")
        questions.append(f"如何判断{base}？")
        questions.append(f"{base}怎么办？")
    elif "出血" in title:
        questions.append(f"{base}正常吗？")
        questions.append(f"{base}怎么处理？")
        questions.append(f"{base}怎么办？")
    elif "清洁" in title or "刷牙" in title:
        questions.append(f"{base}？")
        questions.append(f"如何{base}？")
        questions.append(f"{base}的方法？")
    elif "饮食" in title:
        questions.append(f"{base}？")
        questions.append(f"{base}有什么禁忌？")
        questions.append(f"{base}注意事项？")
    elif "复查" in title or "复诊" in title:
        questions.append(f"{base}？")
        questions.append(f"{base}时间？")
        questions.append(f"什么时候{base}？")
    elif "品牌" in title or "材料" in title or "类型" in title:
        questions.append(f"{base}怎么选？")
        questions.append(f"{base}哪种好？")
        questions.append(f"{base}有什么区别？")
    elif "禁忌" in title or "适合" in title:
        questions.append(f"{base}？")
        questions.append(f"什么人{base}？")
        questions.append(f"{base}条件？")
    else:
        # 通用问题生成
        questions.append(f"{title}？")
        questions.append(f"关于{title}的问题")
        questions.append(f"{category}{title}？")
        questions.append(f"我想了解{title}")
        questions.append(f"{title}是怎么回事？")
    
    return questions

# 生成训练数据
training_data = []
unique_questions = set()

for item in knowledge_base:
    title = item["title"]
    content = item["content"]
    category = item["category"]
    
    # 生成问题
    base_questions = generate_questions(title, category)
    
    # 为每个基础问题生成变体
    for base_q in base_questions:
        for prefix in QUESTION_PREFIXES[:8]:
            for suffix in QUESTION_SUFFIXES[:3]:
                question = f"{prefix}{base_q}{suffix}".replace("？？", "？")
                
                if question not in unique_questions and len(training_data) < 2500:
                    unique_questions.add(question)
                    
                    # 生成回答
                    ans_prefix = random.choice(ANSWER_PREFIXES[:5])
                    ans_suffix = random.choice(ANSWER_SUFFIXES[:5])
                    answer = f"{ans_prefix}{content}{ans_suffix}".strip()
                    
                    training_data.append({
                        "instruction": SYSTEM_PROMPT,
                        "input": question,
                        "output": answer
                    })

print(f"初步生成训练数据：{len(training_data)} 条")
print(f"唯一问题数：{len(unique_questions)}")

# 如果数据不够，继续生成
while len(training_data) < 2000:
    item = random.choice(knowledge_base)
    content = item["content"]
    title = item["title"]
    category = item["category"]
    
    prefix = random.choice(QUESTION_PREFIXES)
    suffix = random.choice(QUESTION_SUFFIXES)
    ans_prefix = random.choice(ANSWER_PREFIXES)
    ans_suffix = random.choice(ANSWER_SUFFIXES)
    
    # 生成通用问题
    questions = [
        f"{prefix}{title}{suffix}",
        f"{prefix}{category}相关问题",
        f"{prefix}关于{category}的问题",
        f"{prefix}{category}咨询",
    ]
    
    for q in questions:
        if q not in unique_questions and len(training_data) < 2500:
            unique_questions.add(q)
            answer = f"{ans_prefix}{content}{ans_suffix}".strip()
            training_data.append({
                "instruction": SYSTEM_PROMPT,
                "input": q,
                "output": answer
            })

print(f"最终训练数据：{len(training_data)} 条")
print(f"最终唯一问题数：{len(unique_questions)}")

# 去重检查
seen = set()
deduplicated_data = []
for item in training_data:
    key = (item["input"], item["output"])
    if key not in seen:
        seen.add(key)
        deduplicated_data.append(item)

print(f"去重后数据：{len(deduplicated_data)} 条")
training_data = deduplicated_data

# 打乱数据
random.shuffle(training_data)

# 分割数据集
train_size = int(len(training_data) * 0.8)
dev_size = int(len(training_data) * 0.1)

train_data = training_data[:train_size]
dev_data = training_data[train_size:train_size + dev_size]
test_data = training_data[train_size + dev_size:]

# 保存
def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(data)} 条数据到 {filepath}")

save_json(train_data, "D:/Project/毕业设计/data/train/train_final.json")
save_json(dev_data, "D:/Project/毕业设计/data/train/dev_final.json")
save_json(test_data, "D:/Project/毕业设计/data/train/test_final.json")

# 统计信息
print("\n" + "=" * 60)
print("数据集生成完成！")
print("=" * 60)
print(f"\n知识库：{len(knowledge_base)} 条")
print(f"训练集：{len(train_data)} 条")
print(f"验证集：{len(dev_data)} 条")
print(f"测试集：{len(test_data)} 条")
print(f"总计：{len(knowledge_base) + len(train_data) + len(dev_data) + len(test_data)} 条")

# 类别分布
category_count = {}
for item in train_data:
    # 从问题中推断类别
    input_text = item["input"]
    for cat in ["种植", "固定", "活动", "术后", "复查", "材料", "紧急"]:
        if cat in input_text:
            category_count[cat] = category_count.get(cat, 0) + 1
            break

print("\n训练集类别分布（估计）：")
for cat, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count} 条 ({count/len(train_data)*100:.1f}%)")
