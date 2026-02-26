#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对 train.json 进行去重处理
"""
import json
from collections import Counter

# 读取数据
with open('D:/Project/毕业设计/data/train/train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"去重前记录数：{len(data)}")

# 方法：基于 input + output 组合去重（保留第一条）
seen = set()
unique_data = []
duplicate_count = 0

for item in data:
    # 使用 input + output 作为唯一键
    key = (item['input'], item['output'])
    
    if key not in seen:
        seen.add(key)
        unique_data.append(item)
    else:
        duplicate_count += 1

print(f"去重后记录数：{len(unique_data)}")
print(f"删除重复记录数：{duplicate_count}")

# 保存去重后的数据
with open('D:/Project/毕业设计/data/train/train.json', 'w', encoding='utf-8') as f:
    json.dump(unique_data, f, ensure_ascii=False, indent=2)

print("\n去重完成！数据已保存到 train.json")

# 统计信息
print("\n" + "=" * 60)
print("去重后统计信息：")
print("-" * 60)
category_counter = Counter(item['category'] for item in unique_data)
for cat, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"{cat}: {count} 条 ({count/len(unique_data)*100:.1f}%)")

print("\n" + "=" * 60)
