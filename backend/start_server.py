#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牙科修复 AI 系统 - FastAPI 后端服务启动脚本
"""

import os
import sys
import subprocess

def get_autodl_url():
    """获取 AutoDL AI 服务地址"""
    default_url = "https://u769760-522r-e89d6ec1.bjb2.seetacloud.com:8443"
    
    print("=" * 60)
    print("  配置 AutoDL AI 服务地址")
    print("=" * 60)
    print()
    print(f"默认地址：{default_url}")
    print()
    print("格式要求:")
    print("  1. 以 https:// 开头")
    print("  2. 包含 seetacloud.com")
    print("  3. 包含端口号 (如 :8443)")
    print()
    print("=" * 60)
    print()
    
    while True:
        user_input = input("请输入 AutoDL AI 服务地址 (直接回车使用默认值): ").strip()
        
        if not user_input:
            url = default_url
            print(f"\n[使用默认值] {url}")
        else:
            url = user_input
            print(f"\n[自定义地址] {url}")
        
        # 验证格式
        if not (url.startswith("https://") and "seetacloud.com" in url and ":" in url.split("seetacloud.com")[1][:10]):
            print("\n[错误] 地址格式不正确！请确保:")
            print("  1. 以 https:// 开头")
            print("  2. 包含 seetacloud.com")
            print("  3. 包含端口号 (如 :8443)")
            print()
            continue
        
        print("\n[成功] 地址格式验证通过")
        return url

def main():
    print("=" * 40)
    print(" 牙科修复 AI 系统 - FastAPI 后端服务")
    print("=" * 40)
    print()
    
    # 获取 AutoDL 地址
    autodl_url = get_autodl_url()
    
    # 设置环境变量
    os.environ["AI_SERVICE_URL"] = autodl_url
    
    print()
    print("=" * 60)
    print("  服务启动成功！")
    print("=" * 60)
    print()
    print("  API 文档地址：http://localhost:8000/docs")
    print("  ReDoc 文档：http://localhost:8000/redoc")
    print(f"  AI 服务地址：{autodl_url}")
    print()
    print("  按 Ctrl+C 停止服务")
    print()
    print("=" * 60)
    print()
    
    # 启动 uvicorn
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "app.main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

if __name__ == "__main__":
    main()
