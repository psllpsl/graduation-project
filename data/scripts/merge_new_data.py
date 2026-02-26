#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
合并 46 条新数据到训练集，并检查重复
"""
import json

# 读取原有训练集
with open('D:/Project/毕业设计/data/train/train.json', 'r', encoding='utf-8') as f:
    original_data = json.load(f)

# 读取新增的 46 条数据
with open('D:/Project/毕业设计/data/train/new_46_records.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

print(f"原有训练集：{len(original_data)} 条")
print(f"新增数据：{len(new_data)} 条")

# 获取原有数据的 input 集合
original_inputs = set(item['input'] for item in original_data)

# 检查新数据是否有重复
duplicates = []
for item in new_data:
    if item['input'] in original_inputs:
        duplicates.append(item['input'])

if duplicates:
    print(f"\n[警告] 发现 {len(duplicates)} 条重复数据：")
    for dup in duplicates:
        print(f"  - {dup[:50]}...")
else:
    print("\n[OK] 新数据与原有数据无重复")

# 合并数据
merged_data = original_data + new_data

# 再次检查合并后是否有重复
all_inputs = [item['input'] for item in merged_data]
unique_inputs = set(all_inputs)

if len(all_inputs) != len(unique_inputs):
    print(f"\n[警告] 合并后有重复！总数：{len(all_inputs)}, 唯一：{len(unique_inputs)}")
else:
    print(f"\n[OK] 合并后无重复")

# 保存合并后的数据
with open('D:/Project/毕业设计/data/train/train.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"\n合并完成！")
print(f"合并后总数：{len(merged_data)} 条")
print(f"数据已保存到 train.json")

# 统计类别分布
from collections import Counter
category_counter = Counter(item['category'] for item in merged_data)
print("\n合并后类别分布：")
for cat, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"  {cat}: {count} 条 ({count/len(merged_data)*100:.1f}%)")
