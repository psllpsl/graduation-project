#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
合并 100 条新数据到训练集
"""
import json
from collections import Counter

# 读取原有训练集
with open('D:/Project/毕业设计/data/train/train.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

print(f"原有训练集：{len(original_data)} 条")

# 获取原有数据的 input 集合
original_inputs = set(item['input'] for item in original_data)

# 读取新数据
with open('D:/Project/毕业设计/data/train/batch_new_100.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

print(f"新增数据文件：{len(new_data)} 条")

# 检查重复
unique_new = []
duplicates = 0

for item in new_data:
    if item['input'] not in original_inputs:
        unique_new.append(item)
        original_inputs.add(item['input'])
    else:
        duplicates += 1
        print(f"重复跳过：{item['input'][:50]}...")

print(f"\n实际新增：{len(unique_new)} 条")
print(f"重复数据：{duplicates} 条")

# 合并数据
merged_data = original_data + unique_new

# 保存合并后的数据
with open('D:/Project/毕业设计/data/train/train.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"\n合并完成！")
print(f"合并后总数：{len(merged_data)} 条")

# 统计类别分布
category_counter = Counter(item['category'] for item in merged_data)
print("\n类别分布：")
for cat, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count} 条 ({count/len(merged_data)*100:.1f}%)")
