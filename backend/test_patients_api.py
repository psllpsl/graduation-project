# 测试患者 API
import requests

# 测试 URL
BASE_URL = "http://localhost:8000/api"

print("测试患者 API 路由...")
print("=" * 50)

# 测试 GET /patients/check-complete
print("\n1. 测试 GET /patients/check-complete")
try:
    response = requests.get(f"{BASE_URL}/patients/check-complete")
    print(f"   状态码：{response.status_code}")
    print(f"   响应：{response.json()}")
except Exception as e:
    print(f"   错误：{e}")

# 测试 PATCH /patients/complete
print("\n2. 测试 PATCH /patients/complete")
try:
    response = requests.patch(
        f"{BASE_URL}/patients/complete",
        json={"name": "测试", "phone": "13900139000"}
    )
    print(f"   状态码：{response.status_code}")
    print(f"   响应：{response.json()}")
except Exception as e:
    print(f"   错误：{e}")

# 测试 GET /patients/by-openid/xxx
print("\n3. 测试 GET /patients/by-openid/test")
try:
    response = requests.get(f"{BASE_URL}/patients/by-openid/test")
    print(f"   状态码：{response.status_code}")
    print(f"   响应：{response.json()}")
except Exception as e:
    print(f"   错误：{e}")

print("\n" + "=" * 50)
print("测试完成！")
