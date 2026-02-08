"""
$CAPSULE 知识胶囊交易系统
支持胶囊发行、交易、钱包、转账
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import os
from datetime import datetime
import hashlib
import secrets

# ===================== 配置 =====================
DB_PATH = "/Users/wanyview/clawd/capsule_trade/capsule_trade.db"
app = FastAPI(title="Kai Capsule Trade System", version="1.0.0")

# ===================== 数据库 =====================
_db_conn = None

def get_db():
    """获取数据库连接"""
    global _db_conn
    if _db_conn is None:
        _db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _db_conn.row_factory = sqlite3.Row
    return _db_conn

def init_db():
    """初始化数据库"""
    conn = get_db()
    cursor = conn.cursor()
    
    # 钱包表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            id TEXT PRIMARY KEY,
            user_id TEXT UNIQUE NOT NULL,
            balance REAL DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # 交易记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            from_user TEXT,
            to_user TEXT,
            amount REAL,
            tx_type TEXT,
            capsule_id TEXT,
            created_at TEXT
        )
    ''')
    
    # 胶囊发行表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capsule_issuance (
            id TEXT PRIMARY KEY,
            capsule_id TEXT NOT NULL,
            issuer TEXT NOT NULL,
            price REAL NOT NULL,
            total_supply INTEGER DEFAULT 1,
            sold_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            created_at TEXT
        )
    ''')
    
    conn.commit()

init_db()

# ===================== 数据模型 =====================
class WalletCreate(BaseModel):
    user_id: str

class WalletResponse(BaseModel):
    user_id: str
    balance: float
    created_at: str

class TransferRequest(BaseModel):
    from_user: str
    to_user: str
    amount: float
    memo: Optional[str] = None

class CapsuleIssueRequest(BaseModel):
    capsule_id: str
    issuer: str
    price: float
    total_supply: int = 1

class CapsuleBuyRequest(BaseModel):
    capsule_id: str
    buyer: str
    amount: int = 1

# ===================== 工具函数 =====================
def generate_id():
    return secrets.token_hex(8)

def get_or_create_wallet(user_id: str) -> dict:
    """获取或创建钱包"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    cursor.execute("SELECT * FROM wallets WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row is None:
        wallet_id = generate_id()
        cursor.execute('''
            INSERT INTO wallets (id, user_id, balance, created_at, updated_at)
            VALUES (?, ?, 0, ?, ?)
        ''', (wallet_id, user_id, now, now))
        conn.commit()
        return {"user_id": user_id, "balance": 0, "created_at": now}
    
    return dict(row)

# ===================== API路由 =====================

@app.get("/")
async def root():
    return {
        "service": "Kai Capsule Trade System",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/wallets", response_model=WalletResponse)
async def create_wallet(request: WalletCreate):
    """创建钱包"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    cursor.execute("SELECT * FROM wallets WHERE user_id = ?", (request.user_id,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="钱包已存在")
    
    wallet_id = generate_id()
    cursor.execute('''
        INSERT INTO wallets (id, user_id, balance, created_at, updated_at)
        VALUES (?, ?, 0, ?, ?)
    ''', (wallet_id, request.user_id, now, now))
    conn.commit()
    
    return {"user_id": request.user_id, "balance": 0, "created_at": now}

@app.get("/wallets/{user_id}", response_model=WalletResponse)
async def get_wallet(user_id: str):
    """查询钱包"""
    wallet = get_or_create_wallet(user_id)
    return {
        "user_id": wallet["user_id"],
        "balance": wallet["balance"],
        "created_at": wallet.get("created_at", datetime.utcnow().isoformat())
    }

@app.post("/transfer")
async def transfer(request: TransferRequest):
    """转账"""
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="金额必须大于0")
    
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    # 检查发送方余额
    cursor.execute("SELECT balance FROM wallets WHERE user_id = ?", (request.from_user,))
    row = cursor.fetchone()
    if row is None or row[0] < request.amount:
        raise HTTPException(status_code=400, detail="余额不足")
    
    # 扣款
    cursor.execute('''
        UPDATE wallets SET balance = balance - ?, updated_at = ? 
        WHERE user_id = ?
    ''', (request.amount, now, request.from_user))
    
    # 收款
    cursor.execute('''
        UPDATE wallets SET balance = balance + ?, updated_at = ?
        WHERE user_id = ?
    ''', (request.amount, now, request.to_user))
    
    # 记录交易
    tx_id = generate_id()
    cursor.execute('''
        INSERT INTO transactions (id, from_user, to_user, amount, tx_type, created_at)
        VALUES (?, ?, ?, ?, 'transfer', ?)
    ''', (tx_id, request.from_user, request.to_user, request.amount, now))
    
    conn.commit()
    
    return {
        "status": "success",
        "tx_id": tx_id,
        "from": request.from_user,
        "to": request.to_user,
        "amount": request.amount,
        "created_at": now
    }

@app.post("/issue")
async def issue_capsule(request: CapsuleIssueRequest):
    """发行胶囊"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    # 检查是否已发行
    cursor.execute("SELECT * FROM capsule_issuance WHERE capsule_id = ?", (request.capsule_id,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="胶囊已发行")
    
    issuance_id = generate_id()
    cursor.execute('''
        INSERT INTO capsule_issuance (id, capsule_id, issuer, price, total_supply, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'active', ?)
    ''', (issuance_id, request.capsule_id, request.issuer, request.price, request.total_supply, now))
    
    conn.commit()
    
    return {
        "status": "success",
        "issuance_id": issuance_id,
        "capsule_id": request.capsule_id,
        "price": request.price,
        "total_supply": request.total_supply,
        "created_at": now
    }

@app.post("/buy")
async def buy_capsule(request: CapsuleBuyRequest):
    """购买胶囊"""
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    # 检查发行
    cursor.execute("SELECT * FROM capsule_issuance WHERE capsule_id = ? AND status = 'active'", 
                   (request.capsule_id,))
    issuance = cursor.fetchone()
    if issuance is None:
        raise HTTPException(status_code=404, detail="胶囊未发行或已售罄")
    
    if issuance['sold_count'] + request.amount > issuance['total_supply']:
        raise HTTPException(status_code=400, detail="超出可购买数量")
    
    total_price = issuance['price'] * request.amount
    
    # 检查买家余额
    cursor.execute("SELECT balance FROM wallets WHERE user_id = ?", (request.buyer,))
    wallet = cursor.fetchone()
    if wallet is None or wallet[0] < total_price:
        raise HTTPException(status_code=400, detail="余额不足")
    
    # 扣款
    cursor.execute('''
        UPDATE wallets SET balance = balance - ?, updated_at = ?
        WHERE user_id = ?
    ''', (total_price, now, request.buyer))
    
    # 增加销量
    cursor.execute('''
        UPDATE capsule_issuance SET sold_count = sold_count + ?
        WHERE id = ?
    ''', (request.amount, issuance['id']))
    
    # 记录交易
    tx_id = generate_id()
    cursor.execute('''
        INSERT INTO transactions (id, from_user, to_user, amount, tx_type, capsule_id, created_at)
        VALUES (?, ?, ?, ?, 'buy', ?, ?)
    ''', (tx_id, request.buyer, issuance['issuer'], total_price, request.capsule_id, now))
    
    conn.commit()
    
    return {
        "status": "success",
        "tx_id": tx_id,
        "capsule_id": request.capsule_id,
        "buyer": request.buyer,
        "amount": request.amount,
        "total_price": total_price,
        "created_at": now
    }

@app.get("/transactions/{user_id}")
async def get_transactions(user_id: str, limit: int = 20):
    """查询交易记录"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions 
        WHERE from_user = ? OR to_user = ?
        ORDER BY created_at DESC LIMIT ?
    ''', (user_id, user_id, limit))
    
    return {
        "user_id": user_id,
        "transactions": [dict(row) for row in cursor.fetchall()]
    }

@app.get("/market")
async def get_market():
    """市场概览"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM capsule_issuance WHERE status = 'active'")
    active_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(sold_count) FROM capsule_issuance")
    total_sold = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM wallets")
    wallet_count = cursor.fetchone()[0]
    
    return {
        "active_listings": active_count,
        "total_sold": total_sold,
        "total_wallets": wallet_count
    }

# ===================== 启动 =====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
