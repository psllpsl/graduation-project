"""
敏感信息脱敏脚本
用于在上传 GitHub 前替换文档中的敏感信息
"""

import os
import re

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 需要脱敏的模式和替换
REPLACEMENTS = {
    # AutoDL 实例地址
    r'uu769760-[\w-]+\.bjb[\d]\.seetacloud\.com:\d+': '你的实例 ID.seetacloud.com:端口',
    r'uu769760-[\w-]+': '你的实例 ID',
    
    # 微信小程序 AppID
    r'your-appid-here': 'your-appid-here',
    r'your-appid-here': 'your-appid-here',
    
    # 数据库密码（示例）
    r'DATABASE_PASSWORD=你的密码': 'DATABASE_PASSWORD=你的密码',
    
    # 具体的 IP 地址（局域网）
    r'10\.14\.168\.\d+': '你的电脑 IP',
    r'192\.168\.\d+\.\d+': '你的电脑 IP',
}

# 需要处理的文件扩展名
FILE_EXTENSIONS = ['.md', '.txt', '.json', '.py', '.env.example']

def sanitize_file(file_path):
    """脱敏单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changed = False
        
        # 应用所有替换
        for pattern, replacement in REPLACEMENTS.items():
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changed = True
                content = new_content
        
        # 如果有变化，写回文件
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] 已脱敏：{file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"[错误] {file_path}: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("敏感信息脱敏脚本")
    print("=" * 60)
    print()
    
    sanitized_count = 0
    total_count = 0
    
    # 遍历项目目录
    for root, dirs, files in os.walk(BASE_DIR):
        # 跳过某些目录
        if any(skip in root for skip in ['.git', 'venv', '__pycache__', 'node_modules']):
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1]
            
            if ext in FILE_EXTENSIONS:
                total_count += 1
                if sanitize_file(file_path):
                    sanitized_count += 1
    
    print()
    print("=" * 60)
    print(f"检查文件数：{total_count}")
    print(f"脱敏文件数：{sanitized_count}")
    print("=" * 60)
    print()
    print("脱敏完成！")
    print()
    print("注意：")
    print("1. .env 文件不会被处理（已在 .gitignore 中）")
    print("2. 请手动检查敏感信息是否完全脱敏")
    print("3. 查看 敏感信息说明.md 了解如何配置")

if __name__ == "__main__":
    main()
