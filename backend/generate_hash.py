"""
使用 bcrypt 库直接生成密码哈希
"""
import bcrypt

# 生成 admin123 的密码哈希
password = b"admin123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

print(f"密码：admin123")
print(f"哈希：{hashed.decode('utf-8')}")

# 验证
verify_result = bcrypt.checkpw(password, hashed)
print(f"验证结果：{verify_result}")
