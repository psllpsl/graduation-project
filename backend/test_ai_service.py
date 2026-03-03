"""
测试 AI 服务连接
用于快速诊断 AI 服务是否正常
"""
import httpx
import warnings

# 禁用 SSL 警告
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

# AI 服务配置
# 当前地址：https://uu769760-8aa7-e51ad73a.bjb1.seetacloud.com:8443
AI_SERVICE_URL = "https://uu769760-8aa7-e51ad73a.bjb1.seetacloud.com:8443"

def test_ai_service():
    """测试 AI 服务连接"""
    print("=" * 50)
    print("AI 服务连接测试")
    print("=" * 50)
    
    # 确保 URL 以 /generate 结尾
    api_url = AI_SERVICE_URL
    if not api_url.endswith("/generate"):
        api_url = api_url.rstrip("/") + "/generate"
    
    print(f"请求地址：{api_url}")
    
    try:
        # 测试连接
        print("\n正在连接 AI 服务...")
        with httpx.Client(
            timeout=httpx.Timeout(60, connect=10.0),
            verify=False
        ) as client:
            response = client.post(
                api_url,
                json={
                    "prompt": "你好",
                    "system_prompt": "你是一名牙科修复 AI 助手",
                    "max_tokens": 50,
                    "temperature": 0.5
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            
            print(f"响应状态码：{response.status_code}")
            print(f"响应头：{dict(response.headers)}")
            print(f"\n响应内容：{response.text[:500] if response.text else 'empty'}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n解析后的 JSON: {result}")
                print("\n[OK] AI 服务连接成功！")
                return True
            else:
                print(f"\n[错误] 响应状态码：{response.status_code}")
                return False
                
    except httpx.ConnectError as e:
        print(f"\n[错误] 连接失败：{e}")
        print("可能原因：")
        print("  1. AI 服务未启动")
        print("  2. 网络问题")
        print("  3. 防火墙阻止")
        return False
    except httpx.TimeoutException as e:
        print(f"\n[错误] 连接超时：{e}")
        print("可能原因：")
        print("  1. 网络延迟")
        print("  2. AI 服务负载过高")
        return False
    except Exception as e:
        print(f"\n[错误] 发生异常：{e}")
        return False

if __name__ == "__main__":
    success = test_ai_service()
    print("\n" + "=" * 50)
    if success:
        print("测试通过！后端应该可以正常连接 AI 服务")
    else:
        print("测试失败！请检查 AI 服务状态和网络连接")
        print("\n排查步骤：")
        print("1. 登录 AutoDL 控制台，确认实例运行中")
        print("2. 检查自定义服务端口映射（6008 -> 8443）")
        print("3. 在 AutoDL 终端测试本地调用：curl http://localhost:6008/generate")
        print("4. 检查 .env 中的 AI_SERVICE_URL 配置")
