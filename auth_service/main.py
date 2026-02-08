"""
用户认证服务 - FastAPI + SQLite + JWT
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import sqlite3
import jwt
import hashlib
import os
from datetime import datetime, timedelta

# ===================== 配置 =====================
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "kai-huangzhong-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时

app = FastAPI(title="Kai Auth Service", version="1.0.0")
security = HTTPBearer()

# ===================== 数据库 =====================
DB_PATH = "/Users/wanyview/clawd/auth_service/users.db"
_db_conn = None

def init_db():
    """初始化数据库"""
    global _db_conn
    _db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = _db_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            api_key TEXT UNIQUE,
            role TEXT DEFAULT 'user',
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    _db_conn.commit()

init_db()

def get_db():
    """获取数据库连接（线程安全）"""
    global _db_conn
    if _db_conn is None:
        _db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return _db_conn

# ===================== 数据模型 =====================
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    api_key: Optional[str]
    role: str

# ===================== 工具函数 =====================
def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_api_key() -> str:
    """生成API密钥"""
    import secrets
    return "kai_" + secrets.token_hex(16)

def create_access_token(data: dict) -> str:
    """创建JWT令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ===================== 认证依赖 =====================
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户"""
    token = credentials.credentials
    payload = verify_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="无效的令牌")
    return username

async def get_admin_user(current_user: str = Depends(get_current_user)):
    """管理员权限检查"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ?", (current_user,))
    row = cursor.fetchone()
    conn.close()
    if row is None or row[0] != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user

# ===================== API路由 =====================

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, conn = Depends(get_db)):
    """用户注册"""
    cursor = conn.cursor()
    
    # 检查用户名
    cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建用户
    now = datetime.utcnow().isoformat()
    password_hash = hash_password(user.password)
    api_key = generate_api_key()
    
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, api_key, role, created_at, updated_at)
        VALUES (?, ?, ?, ?, 'user', ?, ?)
    ''', (user.username, user.email, password_hash, api_key, now, now))
    
    conn.commit()
    user_id = cursor.lastrowid
    
    return {
        "id": user_id,
        "username": user.username,
        "email": user.email,
        "api_key": api_key,
        "role": "user"
    }

@app.post("/login", response_model=Token)
async def login(user: UserLogin, conn = Depends(get_db)):
    """用户登录"""
    cursor = conn.cursor()
    password_hash = hash_password(user.password)
    
    cursor.execute('''
        SELECT id, username, role FROM users 
        WHERE username = ? AND password_hash = ?
    ''', (user.username, password_hash))
    
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    access_token = create_access_token(data={"sub": row[1], "role": row[2]})
    return {"access_token": access_token}

@app.get("/me", response_model=UserResponse)
async def get_me(current_user: str = Depends(get_current_user), conn = Depends(get_db)):
    """获取当前用户信息"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, email, api_key, role FROM users WHERE username = ?
    ''', (current_user,))
    
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "api_key": row[3],
        "role": row[4]
    }

@app.post("/regenerate-api-key")
async def regenerate_api_key(current_user: str = Depends(get_current_user), conn = Depends(get_db)):
    """重新生成API密钥"""
    cursor = conn.cursor()
    new_api_key = generate_api_key()
    now = datetime.utcnow().isoformat()
    
    cursor.execute('''
        UPDATE users SET api_key = ?, updated_at = ? WHERE username = ?
    ''', (new_api_key, now, current_user))
    
    conn.commit()
    return {"api_key": new_api_key}

@app.get("/users")
async def list_users(_admin = Depends(get_admin_user), conn = Depends(get_db)):
    """列出所有用户（仅管理员）"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, created_at FROM users")
    rows = cursor.fetchall()
    return {"users": [dict(row) for row in rows]}

# ===================== 启动 =====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
