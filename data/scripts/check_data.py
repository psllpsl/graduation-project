#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
训练集数据校对工具
检查数据重复性和质量
"""

import json
import hashlib
import sys
from datetime import datetime
from collections import Counter

# 设置标准输出编码为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

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

def check_duplicates(data):
    """检查重复数据"""
    seen_hashes = {}
    duplicates = []
    
    for i, item in enumerate(data):
        data_hash = get_data_hash(item)
        if data_hash in seen_hashes:
            duplicates.append({
                'index': i,
                'input': item.get('input', '')[:50] + '...' if len(item.get('input', '')) > 50 else item.get('input', ''),
                'duplicate_of': seen_hashes[data_hash]
            })
        else:
            seen_hashes[data_hash] = i
    
    return duplicates

def check_quality(data):
    """检查数据质量"""
    issues = []
    
    for i, item in enumerate(data):
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
        if len(output) > 3000:
            issues.append(f"索引 {i}: output 过长 ({len(output)} 字符)")
        
        # 检查 input 长度
        input_text = item.get('input', '')
        if len(input_text) < 5:
            issues.append(f"索引 {i}: input 过短 ({len(input_text)} 字符)")
        if len(input_text) > 200:
            issues.append(f"索引 {i}: input 过长 ({len(input_text)} 字符)")
        
        # 检查 category 是否合法
        valid_categories = ['术后护理', '术前评估', '常见问题', '修复类型', '材料选择', '复诊规范', '紧急情况']
        if item.get('category') not in valid_categories:
            issues.append(f"索引 {i}: category 不合法 - {item.get('category')}")
    
    return issues

def generate_report(data, duplicates, issues):
    """生成校对报告"""
    # 统计类别分布
    category_count = Counter(item.get('category', '未知') for item in data)
    
    report = f"""# 训练集数据校对报告

## 生成时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 数据概览
- 总数据量：{len(data)} 条
- 目标数据量：500 条
- 完成进度：{len(data)/500*100:.1f}%

## 重复检查
- 重复数据：{len(duplicates)} 条
- 重复率：{len(duplicates)/len(data)*100:.2f}%
- 检查结果：{"✅ 无重复" if not duplicates else f"⚠️ 发现 {len(duplicates)} 条重复"}

{"### 重复详情" if duplicates else ""}
"""
    
    if duplicates:
        for dup in duplicates[:20]:
            report += f"- 索引 {dup['index']}: \"{dup['input']}\" (重复于索引 {dup['duplicate_of']})\n"
    
    report += f"""
## 数据质量
- 发现问题：{len(issues)} 个
- 质量状态：{"✅ 通过" if not issues else f"⚠️ 发现 {len(issues)} 个问题"}

{"### 问题详情" if issues else ""}
"""
    
    if issues:
        for issue in issues[:20]:
            report += f"- {issue}\n"
    
    report += f"""
## 类别分布

| 类别 | 数量 | 占比 |
|------|------|------|
"""
    
    for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(data) * 100
        report += f"| {category} | {count} 条 | {percentage:.1f}% |\n"
    
    total = sum(category_count.values())
    report += f"| **总计** | **{total} 条** | **100%** |\n"
    
    report += f"""
## 数据示例

### 示例 1（索引 0）
- **input**: {data[0].get('input', '')}
- **category**: {data[0].get('category', '')}
- **output 长度**: {len(data[0].get('output', ''))} 字符

### 示例 2（索引 50）
- **input**: {data[50].get('input', '') if len(data) > 50 else 'N/A'}
- **category**: {data[50].get('category', '') if len(data) > 50 else 'N/A'}
- **output 长度**: {len(data[50].get('output', '')) if len(data) > 50 else 0} 字符

### 示例 3（索引 99）
- **input**: {data[99].get('input', '') if len(data) > 99 else 'N/A'}
- **category**: {data[99].get('category', '') if len(data) > 99 else 'N/A'}
- **output 长度**: {len(data[99].get('output', '')) if len(data) > 99 else 0} 字符

## 结论

"""
    
    if not duplicates and not issues:
        report += "✅ **数据质量优秀！** 无重复数据，无质量问题。\n"
    elif not duplicates:
        report += f"⚠️ **数据质量良好。** 无重复数据，但存在 {len(issues)} 个质量问题需要修复。\n"
    else:
        report += f"❌ **数据质量需改进。** 发现 {len(duplicates)} 条重复数据和 {len(issues)} 个质量问题。\n"
    
    report += f"""
## 下一步建议

1. {"✅ 数据无重复，可以继续生成剩余数据" if not duplicates else "❌ 先修复重复数据"}
2. {"✅ 数据质量合格" if not issues else f"❌ 修复 {len(issues)} 个质量问题"}
3. 📊 继续生成剩余的 {500 - len(data)} 条数据
4. 📝 生成最终的数据集说明文档

---
*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return report

def main():
    """主函数"""
    print("=" * 70)
    print("训练集数据校对工具")
    print("=" * 70)
    
    # 加载数据
    print("\n[1/5] 加载数据...")
    data = load_json('D:/Project/毕业设计/data/train/train_200.json')
    print(f"      数据量：{len(data)} 条")
    
    # 检查重复
    print("\n[2/5] 检查重复数据...")
    duplicates = check_duplicates(data)
    if duplicates:
        print(f"      ⚠️ 发现 {len(duplicates)} 条重复数据")
    else:
        print("      ✅ 无重复数据")
    
    # 检查质量
    print("\n[3/5] 检查数据质量...")
    issues = check_quality(data)
    if issues:
        print(f"      ⚠️ 发现 {len(issues)} 个问题")
    else:
        print("      ✅ 数据质量合格")
    
    # 生成报告
    print("\n[4/5] 生成校对报告...")
    report = generate_report(data, duplicates, issues)
    report_file = 'D:/Project/毕业设计/data/train/train_200_check_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"      报告已保存：{report_file}")
    
    # 保存去重后的数据（如果有重复）
    print("\n[5/5] 保存去重后的数据...")
    if duplicates:
        seen_hashes = set()
        unique_data = []
        for item in data:
            data_hash = get_data_hash(item)
            if data_hash not in seen_hashes:
                seen_hashes.add(data_hash)
                unique_data.append(item)
        
        dedup_file = 'D:/Project/毕业设计/data/train/train_300_dedup.json'
        save_json(unique_data, dedup_file)
        print(f"      去重后数据：{len(unique_data)} 条")
        print(f"      已保存：{dedup_file}")
    else:
        print("      无需去重")
    
    # 打印统计信息
    print("\n" + "=" * 70)
    print("统计信息")
    print("=" * 70)
    
    from collections import Counter
    category_count = Counter(item.get('category', '未知') for item in data)
    print("\n类别分布:")
    for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        percentage = count / len(data) * 100
        print(f"  {category}: {count} 条 ({percentage:.1f}%)")
    
    print(f"\n总数据量：{len(data)} 条")
    print(f"目标数据量：500 条")
    print(f"完成进度：{len(data)/500*100:.1f}%")
    print(f"还需生成：{500 - len(data)} 条")
    
    print("\n" + "=" * 70)
    if not duplicates and not issues:
        print("✅ 校对完成！数据质量优秀！")
    elif not duplicates:
        print(f"⚠️ 校对完成！数据无重复，但存在 {len(issues)} 个质量问题。")
    else:
        print(f"❌ 校对完成！发现 {len(duplicates)} 条重复数据和 {len(issues)} 个质量问题。")
    print("=" * 70)

if __name__ == '__main__':
    main()
