#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
合并训练集数据并进行去重校对
"""

import json
import hashlib
from datetime import datetime

def load_json(filepath):
    """加载 JSON 文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_data_hash(item):
    """生成数据的唯一哈希值（基于 input 字段）"""
    input_text = item.get('input', '')
    return hashlib.md5(input_text.encode('utf-8')).hexdigest()

def merge_and_dedup():
    """合并并去重"""
    print("=" * 60)
    print("训练集数据合并与校对工具")
    print("=" * 60)
    
    # 加载两个文件
    print("\n[1] 加载 train_100.json...")
    data1 = load_json('D:/Project/毕业设计/data/train/train_100.json')
    print(f"    数据量：{len(data1)} 条")
    
    print("\n[2] 加载 train_new_100.json...")
    data2 = load_json('D:/Project/毕业设计/data/train/train_new_100.json')
    print(f"    数据量：{len(data2)} 条")
    
    # 合并数据
    print("\n[3] 合并数据...")
    all_data = data1 + data2
    print(f"    合并后总数：{len(all_data)} 条")
    
    # 去重检查
    print("\n[4] 进行去重检查...")
    seen_hashes = {}
    duplicates = []
    unique_data = []
    
    for i, item in enumerate(all_data):
        data_hash = get_data_hash(item)
        if data_hash in seen_hashes:
            duplicates.append({
                'index': i,
                'input': item.get('input', ''),
                'duplicate_of': seen_hashes[data_hash]
            })
        else:
            seen_hashes[data_hash] = i
            unique_data.append(item)
    
    print(f"    唯一数据：{len(unique_data)} 条")
    print(f"    重复数据：{len(duplicates)} 条")
    
    if duplicates:
        print("\n    重复详情:")
        for dup in duplicates[:10]:  # 只显示前 10 条
            print(f"    - 索引 {dup['index']}: \"{dup['input'][:50]}...\" (重复于索引 {dup['duplicate_of']})")
    
    # 保存合并后的数据
    print("\n[5] 保存合并后的数据...")
    output_file = 'D:/Project/毕业设计/data/train/train_300.json'
    save_json(unique_data, output_file)
    print(f"    已保存到：{output_file}")
    
    # 统计类别分布
    print("\n[6] 统计类别分布...")
    category_count = {}
    for item in unique_data:
        category = item.get('category', '未知')
        category_count[category] = category_count.get(category, 0) + 1
    
    print("\n    类别分布:")
    for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(unique_data) * 100
        print(f"    - {category}: {count} 条 ({percentage:.1f}%)")
    
    # 数据质量检查
    print("\n[7] 数据质量检查...")
    issues = []
    
    for i, item in enumerate(unique_data):
        # 检查必需字段
        if not item.get('instruction'):
            issues.append(f"索引 {i}: 缺少 instruction 字段")
        if not item.get('input'):
            issues.append(f"索引 {i}: 缺少 input 字段")
        if not item.get('output'):
            issues.append(f"索引 {i}: 缺少 output 字段")
        if not item.get('category'):
            issues.append(f"索引 {i}: 缺少 category 字段")
        
        # 检查 output 长度
        output = item.get('output', '')
        if len(output) < 50:
            issues.append(f"索引 {i}: output 过短 ({len(output)} 字符)")
        if len(output) > 2000:
            issues.append(f"索引 {i}: output 过长 ({len(output)} 字符)")
    
    if issues:
        print(f"    发现问题：{len(issues)} 个")
        for issue in issues[:10]:
            print(f"    - {issue}")
    else:
        print("    ✅ 所有数据通过质量检查")
    
    # 生成报告
    print("\n[8] 生成校对报告...")
    report = f"""# 训练集数据合并校对报告

## 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 数据来源
- train_100.json: {len(data1)} 条
- train_new_100.json: {len(data2)} 条

## 合并结果
- 合并前总数：{len(all_data)} 条
- 去重后总数：{len(unique_data)} 条
- 重复数据：{len(duplicates)} 条

## 类别分布
"""
    for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(unique_data) * 100
        report += f"- {category}: {count} 条 ({percentage:.1f}%)\n"
    
    report += f"""
## 数据质量
- 发现问题：{len(issues)} 个
- 质量状态：{"✅ 通过" if not issues else "⚠️ 需修复"}

## 输出文件
- train_300.json: {len(unique_data)} 条

## 下一步
1. 检查并修复发现的问题（如有）
2. 继续生成剩余的 200 条数据（目标 500 条）
"""
    
    report_file = 'D:/Project/毕业设计/data/train/merge_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"    报告已保存到：{report_file}")
    
    print("\n" + "=" * 60)
    print("合并与校对完成!")
    print("=" * 60)
    
    return unique_data, duplicates, issues

if __name__ == '__main__':
    merge_and_dedup()
