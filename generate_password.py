from passlib.context import CryptContext

# 配置密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成密码哈希
password = "admin123"
hashed = pwd_context.hash(password)

print(f"密码: {password}")
print(f"哈希值: {hashed}")

# 验证密码
is_valid = pwd_context.verify(password, hashed)
print(f"验证结果: {is_valid}") 