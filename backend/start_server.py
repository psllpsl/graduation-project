"""
牙科修复复诊系统 - 后端启动脚本
功能：
1. 交互式输入 AI 服务地址
2. 自动更新 .env 配置文件
3. 启动 FastAPI 后端服务

使用方法：
    python start_server.py
"""

import os
import re
import sys

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, '.env')


def read_env_file():
    """读取 .env 文件内容"""
    if not os.path.exists(ENV_FILE):
        print(f"警告：{ENV_FILE} 不存在，将创建新文件")
        return {}
    
    config = {}
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def write_env_file(config):
    """更新 .env 文件"""
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新 AI_SERVICE_URL
    old_url_pattern = r'(AI_SERVICE_URL\s*=\s*).+'
    new_content = re.sub(
        old_url_pattern,
        f'\\1{config["AI_SERVICE_URL"]}',
        content
    )
    
    with open(ENV_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] 已更新 .env 文件")


def get_ai_service_url():
    """获取 AI 服务地址（交互式输入）"""
    print("=" * 60)
    print("牙科修复复诊系统 - 后端启动")
    print("=" * 60)
    print()
    
    # 读取当前配置
    config = read_env_file()
    current_url = config.get('AI_SERVICE_URL', '')
    
    print(f"当前 AI 服务地址：{current_url}")
    print()
    print("请输入新的 AI 服务地址（来自 AutoDL 控制台）")
    print("格式：https://你的实例 ID.seetacloud.com:端口")
    print("（如果地址未变化，直接按回车使用当前地址）")
    print()
    
    # 获取用户输入
    new_url = input("AI 服务地址：").strip()
    
    if not new_url:
        # 使用当前地址
        if current_url:
            print(f"使用当前地址：{current_url}")
            return current_url
        else:
            print("错误：未配置 AI 服务地址")
            sys.exit(1)
    
    # 验证 URL 格式
    if not new_url.startswith('https://'):
        print("警告：URL 应该以 https:// 开头")
        confirm = input("是否继续使用？(y/n): ").strip().lower()
        if confirm != 'y':
            return get_ai_service_url()
    
    if ':8443' not in new_url:
        print("警告：URL 应该包含端口 :8443")
        confirm = input("是否继续使用？(y/n): ").strip().lower()
        if confirm != 'y':
            return get_ai_service_url()
    
    # 更新配置
    config['AI_SERVICE_URL'] = new_url.rstrip('/')
    write_env_file(config)
    
    print()
    print(f"[OK] AI 服务地址已更新：{config['AI_SERVICE_URL']}")
    return config['AI_SERVICE_URL']


def test_ai_connection(url):
    """测试 AI 服务连接"""
    print()
    print("正在测试 AI 服务连接...")
    
    try:
        import httpx
        import warnings
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        
        api_url = url.rstrip('/') + '/generate'
        
        with httpx.Client(
            timeout=httpx.Timeout(30, connect=10.0),
            verify=False
        ) as client:
            response = client.post(
                api_url,
                json={
                    "prompt": "测试连接",
                    "max_tokens": 10
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print("[OK] AI 服务连接成功！")
                return True
            else:
                print(f"[警告] AI 服务响应异常：{response.status_code}")
                print("继续启动后端服务...")
                return True
                
    except Exception as e:
        print(f"[警告] AI 服务连接失败：{e}")
        print("后端服务仍会启动，但 AI 对话功能可能不可用")
        return True


def start_server():
    """启动 FastAPI 后端服务"""
    print()
    print("=" * 60)
    print("正在启动 FastAPI 后端服务...")
    print("=" * 60)
    print()
    print("访问 API 文档：http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务")
    print()
    
    # 启动服务
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


def main():
    """主函数"""
    try:
        # 1. 获取 AI 服务地址
        ai_url = get_ai_service_url()
        
        # 2. 测试连接（可选）
        test_ai_connection(ai_url)
        
        # 3. 启动服务
        start_server()
        
    except KeyboardInterrupt:
        print("\n")
        print("服务已停止")
    except Exception as e:
        print(f"\n[错误] 启动失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
