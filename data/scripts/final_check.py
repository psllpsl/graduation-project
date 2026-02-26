#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最终检查并补充到 200 条
"""
import json

# 读取训练集
with open('D:/Project/毕业设计/data/train/train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"当前训练集：{len(data)} 条")

# 检查是否有重复
inputs = [item['input'] for item in data]
unique_inputs = set(inputs)

if len(inputs) != len(unique_inputs):
    print(f"[警告] 发现 {len(inputs) - len(unique_inputs)} 条重复数据")
    # 删除重复
    seen = set()
    unique_data = []
    for item in data:
        if item['input'] not in seen:
            seen.add(item['input'])
            unique_data.append(item)
    data = unique_data
    print(f"去重后：{len(data)} 条")
else:
    print("[OK] 无重复数据")

# 计算需要补充的数量
target = 200
need_to_add = target - len(data)
print(f"需要补充：{need_to_add} 条")

# 补充数据
if need_to_add > 0:
    new_records = [
      {
        "instruction": "你是一名专业的牙科修复 AI 智能客服助手，请用专业、友好、易懂的语言回答患者关于牙科修复的问题。",
        "input": "医生，活动义齿的基托是什么材料？安全吗？",
        "output": "您好，活动义齿的基托材料主要有以下几种：\n\n【塑料基托（树脂基托）】\n\n【材料特性】\n- 丙烯酸树脂制成\n- 颜色接近牙龈\n- 质轻\n- 价格经济\n\n【优点】\n1. 价格便宜\n2. 制作简单\n3. 修理方便\n4. 颜色美观\n\n【缺点】\n1. 较厚，异物感大\n2. 导热性差\n3. 易老化变色\n4. 强度较低\n\n【价格】2000-5000 元\n\n【金属基托】\n\n【材料特性】\n- 钴铬合金或纯钛\n- 薄而坚固\n- 导热性好\n\n【优点】\n1. 薄而舒适\n2. 导热性好\n3. 强度高耐用\n4. 异物感小\n\n【缺点】\n1. 价格较高\n2. 制作复杂\n3. 修理较难\n\n【价格】5000-15000 元\n\n【安全性】\n\n【塑料基托】\n- 医用级树脂\n- 生物相容性好\n- 安全无毒\n- 通过国家认证\n\n【金属基托】\n- 医用级合金\n- 生物相容性好\n- 无毒性\n- 少数人可能过敏\n\n【选择建议】\n1. 经济条件有限：塑料基托\n2. 追求舒适：金属基托\n3. 金属过敏：塑料基托\n4. 前牙区：塑料基托美观\n\n两种材料都是安全的，建议您根据经济条件和舒适度要求选择。请问您目前戴的是什么基托的义齿？",
        "category": "材料选择"
      }
    ]
    
    # 检查是否重复
    existing_inputs = set(item['input'] for item in data)
    for record in new_records[:need_to_add]:
        if record['input'] not in existing_inputs:
            data.append(record)
            print(f"已添加：{record['input'][:30]}...")

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
