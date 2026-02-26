#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
补充最后 3 条数据达到 300 条
"""
import json

# 读取训练集
with open('D:/Project/毕业设计/data/train/train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"当前训练集：{len(data)} 条")

# 获取现有 input 集合
existing_inputs = set(item['input'] for item in data)

# 补充 3 条新数据
new_records = [
  {
    "instruction": "你是一名专业的牙科修复 AI 智能客服助手，请用专业、友好、易懂的语言回答患者关于牙科修复的问题。",
    "input": "医生，活动义齿戴上后可以吃杏鲍菇吗？",
    "output": "您好，活动义齿戴用后可以吃杏鲍菇，但需要注意：\n\n【吃杏鲍菇的建议】\n\n【烹饪方式】\n1. 选择炖煮方式\n2. 煮软烂一些\n3. 避免油炸\n4. 避免烧烤\n\n【食用方式】\n1. 切成小块\n2. 用后牙咀嚼\n3. 细嚼慢咽\n4. 避免大块咬\n\n【注意事项】\n1. 杏鲍菇纤维多\n2. 可能嵌入义齿\n3. 吃完漱口\n4. 清洗义齿\n\n【食用后处理】\n1. 立即漱口\n2. 取出义齿清洗\n3. 清除残留\n4. 保持清洁\n\n【特别提醒】\n- 初戴者煮软一些\n- 适应后正常食用\n- 注意清洁\n- 保护义齿\n\n建议您将杏鲍菇煮软一些，切成小块食用。请问您的义齿戴了多久了？",
    "category": "术后护理"
  },
  {
    "instruction": "你是一名专业的牙科修复 AI 智能客服助手，请用专业、友好、易懂的语言回答患者关于牙科修复的问题。",
    "input": "医生，种植牙手术后可以吃木耳吗？",
    "output": "您好，种植牙术后可以吃木耳，但需要注意：\n\n【吃木耳的建议】\n\n【烹饪方式】\n1. 选择凉拌或煮汤\n2. 煮软烂一些\n3. 避免过硬\n4. 易于咀嚼\n\n【食用方式】\n1. 切成小块\n2. 用对侧咀嚼\n3. 细嚼慢咽\n4. 避免大块咬\n\n【术后早期】\n1. 术后 2-3 天可以吃\n2. 选择软木耳\n3. 切成小块\n4. 温度适宜\n\n【注意事项】\n1. 木耳纤维多\n2. 可能嵌入伤口\n3. 吃完漱口\n4. 保持清洁\n\n【食用后处理】\n1. 立即漱口\n2. 保持口腔清洁\n3. 清除残留\n4. 保护伤口\n\n【长期建议】\n- 恢复期坚持食用\n- 补充营养\n- 促进伤口愈合\n- 增强体质\n\n建议您术后适量食用软木耳，有助于恢复。请问您术后多久了？",
    "category": "术后护理"
  },
  {
    "instruction": "你是一名专业的牙科修复 AI 智能客服助手，请用专业、友好、易懂的语言回答患者关于牙科修复的问题。",
    "input": "医生，固定义齿戴了后可以吃海带吗？",
    "output": "您好，固定义齿戴了后可以吃海带，但需要注意：\n\n【吃海带的建议】\n\n【烹饪方式】\n1. 选择炖煮方式\n2. 煮软烂一些\n3. 避免凉拌生吃\n4. 易于咀嚼\n\n【食用方式】\n1. 切成小块\n2. 用后牙咀嚼\n3. 细嚼慢咽\n4. 避免大块咬\n\n【注意事项】\n1. 海带纤维多\n2. 可能嵌入牙冠边缘\n3. 吃完漱口\n4. 使用牙线清洁\n\n【食用后处理】\n1. 立即漱口\n2. 使用牙线清洁\n3. 检查牙冠边缘\n4. 清除残留\n\n【特别提醒】\n- 戴牙初期煮软一些\n- 适应后正常食用\n- 注意清洁\n- 保护牙冠\n\n【长期建议】\n- 适量食用\n- 补充碘质\n- 保护口腔健康\n\n建议您将海带煮软一些，切成小块食用，吃完及时清洁。请问您的牙冠戴了多久了？",
    "category": "术后护理"
  }
]

# 检查是否重复
for record in new_records:
    if record['input'] not in existing_inputs:
        data.append(record)
        print(f"已添加：{record['input'][:30]}...")
    else:
        print(f"重复跳过：{record['input'][:30]}...")

# 保存
with open('D:/Project/毕业设计/data/train/train.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n最终训练集：{len(data)} 条")

# 统计
from collections import Counter
category_counter = Counter(item['category'] for item in data)
print("\n类别分布：")
for cat, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count} 条 ({count/len(data)*100:.1f}%)")
