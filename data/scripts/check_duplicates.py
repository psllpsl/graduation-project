#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查 train.json 中的重复内容
"""
import json
from collections import Counter
import sys

# 设置控制台输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取数据
with open('D:/Project/毕业设计/data/train/train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总记录数：{len(data)}")
print("=" * 60)

# 方法 1：检查 input 字段是否重复
input_values = [item['input'] for item in data]
input_counter = Counter(input_values)

duplicates_by_input = {k: v for k, v in input_counter.items() if v > 1}

if duplicates_by_input:
    print(f"\n[警告] 发现 {len(duplicates_by_input)} 个重复的 input 字段：")
    print("-" * 60)
    for inp, count in duplicates_by_input.items():
        print(f"重复 {count} 次：{inp[:50]}...")
else:
    print("\n[OK] 没有发现重复的 input 字段")

# 方法 2：检查 input + output 组合是否重复
input_output_pairs = [(item['input'], item['output']) for item in data]
pair_counter = Counter(input_output_pairs)

duplicates_by_pair = {k: v for k, v in pair_counter.items() if v > 1}

if duplicates_by_pair:
    print(f"\n[警告] 发现 {len(duplicates_by_pair)} 个重复的 (input, output) 组合：")
    print("-" * 60)
    for (inp, out), count in duplicates_by_pair.items():
        print(f"重复 {count} 次：{inp[:50]}...")
else:
    print("\n[OK] 没有发现重复的 (input, output) 组合")

# 方法 3：检查完整记录是否重复（包括 instruction）
full_records = [(item['instruction'], item['input'], item['output']) for item in data]
full_counter = Counter(full_records)

duplicates_full = {k: v for k, v in full_counter.items() if v > 1}

if duplicates_full:
    print(f"\n[警告] 发现 {len(duplicates_full)} 个完全重复的记录：")
    print("-" * 60)
    for (inst, inp, out), count in duplicates_full.items():
        print(f"重复 {count} 次：{inp[:50]}...")
else:
    print("\n[OK] 没有发现完全重复的记录")

# 方法 4：检查 output 字段相似度（简单检查完全相同的 output）
output_values = [item['output'] for item in data]
output_counter = Counter(output_values)

duplicates_by_output = {k: v for k, v in output_counter.items() if v > 1}

if duplicates_by_output:
    print(f"\n[警告] 发现 {len(duplicates_by_output)} 个重复的 output 字段：")
    print("-" * 60)
    for out, count in duplicates_by_output.items():
        print(f"重复 {count} 次：{out[:50]}...")
else:
    print("\n[OK] 没有发现重复的 output 字段")

# 统计信息
print("\n" + "=" * 60)
print("统计信息：")
print("-" * 60)
category_counter = Counter(item['category'] for item in data)
for cat, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    print(f"{cat}: {count} 条 ({count/len(data)*100:.1f}%)")

print("\n" + "=" * 60)
print("检查完成！")
