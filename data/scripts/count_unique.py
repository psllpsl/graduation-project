#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计三个 train 文件的不重复数据总量
"""

import json
import hashlib
import sys

# 设置标准输出编码为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def load_json(filepath):
    """加载 JSON 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_input_hash(input_text):
    """生成 input 的哈希值"""
    return hashlib.md5(input_text.encode('utf-8')).hexdigest()

def analyze_file(filepath, name):
    """分析单个文件"""
    data = load_json(filepath)
    inputs = set()
    for item in data:
        input_text = item.get('input', '')
        inputs.add(get_input_hash(input_text))
    
    print(f"\n{name}")
    print(f"  文件路径：{filepath}")
    print(f"  数据总量：{len(data)} 条")
    print(f"  不重复 input: {len(inputs)} 条")
    
    return data, inputs

def main():
    print("=" * 70)
    print("三个 train 文件不重复数据统计")
    print("=" * 70)
    
    # 分析每个文件
    data1, inputs1 = analyze_file(
        'D:/Project/毕业设计/data/train/train_100.json',
        'train_100.json'
    )
    
    data2, inputs2 = analyze_file(
        'D:/Project/毕业设计/data/train/train_300.json',
        'train_300.json (新生成的 100 条)'
    )
    
    data3, inputs3 = analyze_file(
        'D:/Project/毕业设计/data/train/train_200.json',
        'train_200.json (合并文件)'
    )
    
    # 统计 train_100 和 train_300 的并集
    all_inputs = inputs1 | inputs2
    
    print("\n" + "=" * 70)
    print("不重复数据统计")
    print("=" * 70)
    
    # 计算独有数据
    only_in_100 = inputs1 - inputs2
    only_in_300 = inputs2 - inputs1
    in_both = inputs1 & inputs2
    
    print(f"""
train_100.json 独有数据：{len(only_in_100)} 条
train_300.json 独有数据：{len(only_in_300)} 条
两个文件重复数据：{len(in_both)} 条

合并后不重复数据总量：{len(all_inputs)} 条
""")
    
    # 验证 train_200.json
    print(f"train_200.json 数据量：{len(data3)} 条")
    print(f"train_200.json 不重复量：{len(inputs3)} 条")
    
    # 检查 train_200 是否等于 train_100 + train_300 的合并
    if inputs3 == all_inputs:
        print("\n✅ train_200.json = train_100.json ∪ train_300.json (完全一致)")
    else:
        print("\n⚠️ train_200.json 与合并结果不一致")
        diff1 = inputs3 - all_inputs
        diff2 = all_inputs - inputs3
        if diff1:
            print(f"   train_200 独有：{len(diff1)} 条")
        if diff2:
            print(f"   合并集独有：{len(diff2)} 条")
    
    # 详细重复数据列表
    if in_both:
        print("\n" + "=" * 70)
        print("重复数据详情")
        print("=" * 70)
        
        # 找出重复的 input 文本
        input_map_100 = {get_input_hash(item.get('input', '')): item.get('input', '') for item in data1}
        input_map_300 = {get_input_hash(item.get('input', '')): item.get('input', '') for item in data2}
        
        print(f"\n发现 {len(in_both)} 条重复数据：\n")
        for i, hash_val in enumerate(list(in_both)[:20], 1):
            input_text = input_map_100.get(hash_val, input_map_300.get(hash_val, 'Unknown'))
            if len(input_text) > 50:
                input_text = input_text[:50] + '...'
            print(f"  {i}. {input_text}")
        
        if len(in_both) > 20:
            print(f"\n  ... 还有 {len(in_both) - 20} 条重复数据")
    
    print("\n" + "=" * 70)
    print("最终统计结果")
    print("=" * 70)
    print(f"""
  train_100.json: {len(data1)} 条 ({len(only_in_100)} 条独有)
  train_300.json: {len(data2)} 条 ({len(only_in_300)} 条独有)
  
  合并后不重复总量：{len(all_inputs)} 条
  
  重复率：{len(in_both)/len(all_inputs)*100:.1f}%
""")
    print("=" * 70)

if __name__ == '__main__':
    main()
