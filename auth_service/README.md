# Kai Auth Service - 用户认证服务

## 概述
基于 FastAPI + SQLite + JWT 的用户认证服务

## 功能
- ✅ 用户注册/登录
- ✅ JWT Token 认证
- ✅ API Key 管理
- ✅ 角色权限控制
- ✅ 管理员功能

## 快速开始

### 1. 安装依赖
```bash
cd /Users/wanyview/clawd/auth_service
pip install -r requirements.txt
```

### 2. 启动服务
```bash
python main.py
# 或
uvicorn main:app --host 0.0.0.0 --port 8001
```

### 3. 测试
```bash
# 注册用户
curl -X POST "http://localhost:8001/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "123456"}'

# 登录获取Token
curl -X POST "http://localhost:8001/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "123456"}'

# 获取用户信息
curl -X GET "http://localhost:8001/me" \
  -H "Authorization: Bearer <token>"
```

## API 文档
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 数据库
- 位置: `/Users/wanyview/clawd/auth_service/users.db`
- 类型: SQLite

## 环境变量
- `AUTH_SECRET_KEY`: JWT密钥（默认: kai-huangzhong-2026）
