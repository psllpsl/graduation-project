# 测试本地后端连接 AutoDL AI 服务
# 使用方法：在 backend 目录下执行 python test_autodl_connection.py

import httpx
import json

# AutoDL 服务地址
AUTODL_URL = "https://uu769760-8e18-d25f4791.bjb1.seetacloud.com:8443"

print("=" * 60)
print("测试本地后端连接 AutoDL AI 服务")
print("=" * 60)

# 测试 1：健康检查
print("\n测试 1：健康检查...")
try:
    response = httpx.get(f"{AUTODL_URL}/health", verify=False, timeout=10)
    print(f"状态码：{response.status_code}")
    print(f"响应：{response.json()}")
except Exception as e:
    print(f"失败：{e}")

# 测试 2：推理接口
print("\n测试 2：推理接口测试...")
test_questions = [
    "种植牙术后多久能吃饭？",
    "活动义齿刚戴上很不舒服，正常吗？",
    "烤瓷牙能用多久？"
]

for i, question in enumerate(test_questions, 1):
    print(f"\n问题 {i}: {question}")
    try:
        response = httpx.post(
            f"{AUTODL_URL}/generate",
            json={
                "prompt": question,
                "max_tokens": 100
            },
            verify=False,
            timeout=30
        )
        result = response.json()
        answer = result.get("text", "无回答")
        print(f"回答：{answer[:100]}...")
    except Exception as e:
        print(f"失败：{e}")

# 测试 3：带 System Prompt 的推理
print("\n测试 3：带 System Prompt 的推理测试...")
try:
    response = httpx.post(
        f"{AUTODL_URL}/generate",
        json={
            "prompt": "我种植牙术后第 3 天，可以吃坚果吗？",
            "system_prompt": "你是一名专业的牙科修复 AI 助手，请提供专业、安全的术后指导。",
            "max_tokens": 150
        },
        verify=False,
        timeout=30
    )
    result = response.json()
    answer = result.get("text", "无回答")
    print(f"回答：{answer}")
except Exception as e:
    print(f"失败：{e}")

print("\n" + "=" * 60)
print("测试完成！")
print("=" * 60)
