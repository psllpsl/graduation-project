#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
合并训练集数据
"""

import json

# 加载两个文件
with open('D:/Project/毕业设计/data/train/train_100.json', 'r', encoding='utf-8') as f:
    data1 = json.load(f)

with open('D:/Project/毕业设计/data/train/train_300.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

print(f"train_100.json: {len(data1)} 条")
print(f"train_300.json: {len(data2)} 条")

# 合并数据
merged = data1 + data2
print(f"合并后：{len(merged)} 条")

# 保存合并后的数据
with open('D:/Project/毕业设计/data/train/train_200.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print("已保存到 train_200.json")
