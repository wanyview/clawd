"""
统一API网关 - 整合所有服务
整合认证、胶囊存储、胶囊交易三个系统
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
from typing import Dict, Any

# ===================== 配置 =====================
app = FastAPI(title="Kai API Gateway", version="2.0.0")

# 启用CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 后端服务地址
AUTH_SERVICE = "http://localhost:8004"
CAPSULE_SERVICE = "http://localhost:8005"
TRADE_SERVICE = "http://localhost:8010"

# ===================== 工具函数 =====================
async def proxy_request(url: str, method: str, data: Dict = None, headers: Dict = None):
    """代理请求到后端服务"""
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                resp = await client.get(url, headers=headers)
            elif method == "POST":
                resp = await client.post(url, json=data, headers=headers)
            elif method == "PUT":
                resp = await client.put(url, json=data, headers=headers)
            elif method == "DELETE":
                resp = await client.delete(url, headers=headers)
            else:
                raise HTTPException(status_code=405, detail="不支持的方法")
            
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"服务不可用: {str(e)}")

# ===================== 根路由 =====================

@app.get("/")
async def root():
    """网关状态"""
    return {
        "service": "Kai API Gateway",
        "version": "2.0.0",
        "status": "running",
        "services": {
            "auth": AUTH_SERVICE,
            "capsule": CAPSULE_SERVICE,
            "trade": TRADE_SERVICE
        }
    }

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}

# ===================== 认证服务路由 =====================

@app.post("/api/auth/register")
async def auth_register(request: Request):
    """用户注册"""
    data = await request.json()
    return await proxy_request(f"{AUTH_SERVICE}/register", "POST", data)

@app.post("/api/auth/login")
async def auth_login(request: Request):
    """用户登录"""
    data = await request.json()
    return await proxy_request(f"{AUTH_SERVICE}/login", "POST", data)

@app.get("/api/auth/me")
async def auth_me(authorization: str = None):
    """获取当前用户"""
    headers = {"Authorization": authorization} if authorization else {}
    return await proxy_request(f"{AUTH_SERVICE}/me", "GET", headers=headers)

@app.post("/api/auth/regenerate-key")
async def auth_regenerate_key(authorization: str = None):
    """重新生成API Key"""
    headers = {"Authorization": authorization} if authorization else {}
    return await proxy_request(f"{AUTH_SERVICE}/regenerate-api-key", "POST", headers=headers)

# ===================== 胶囊服务路由 =====================

@app.post("/api/capsules")
async def create_capsule(request: Request):
    """创建胶囊"""
    data = await request.json()
    return await proxy_request(f"{CAPSULE_SERVICE}/capsules", "POST", data)

@app.get("/api/capsules")
async def list_capsules(domain: str = None, min_score: float = None, limit: int = 20):
    """查询胶囊列表"""
    params = {"limit": limit}
    if domain: params["domain"] = domain
    if min_score: params["min_score"] = min_score
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CAPSULE_SERVICE}/capsules", params=params)
        return JSONResponse(content=resp.json(), status_code=resp.status_code)

@app.get("/api/capsules/{capsule_id}")
async def get_capsule(capsule_id: str):
    """获取单个胶囊"""
    return await proxy_request(f"{CAPSULE_SERVICE}/capsules/{capsule_id}", "GET")

@app.delete("/api/capsules/{capsule_id}")
async def delete_capsule(capsule_id: str):
    """删除胶囊"""
    return await proxy_request(f"{CAPSULE_SERVICE}/capsules/{capsule_id}", "DELETE")

@app.post("/api/capsules/collisions")
async def detect_collisions(request: Request):
    """碰撞检测"""
    data = await request.json()
    return await proxy_request(f"{CAPSULE_SERVICE}/collisions", "POST", data)

@app.get("/api/capsules/stats")
async def capsule_stats():
    """胶囊统计"""
    return await proxy_request(f"{CAPSULE_SERVICE}/stats", "GET")

# ===================== 交易服务路由 =====================

@app.post("/api/wallets")
async def create_wallet(request: Request):
    """创建钱包"""
    data = await request.json()
    return await proxy_request(f"{TRADE_SERVICE}/wallets", "POST", data)

@app.get("/api/wallets/{user_id}")
async def get_wallet(user_id: str):
    """查询钱包"""
    return await proxy_request(f"{TRADE_SERVICE}/wallets/{user_id}", "GET")

@app.post("/api/transfer")
async def transfer(request: Request):
    """转账"""
    data = await request.json()
    return await proxy_request(f"{TRADE_SERVICE}/transfer", "POST", data)

@app.post("/api/capsules/issue")
async def issue_capsule(request: Request):
    """发行胶囊"""
    data = await request.json()
    return await proxy_request(f"{TRADE_SERVICE}/issue", "POST", data)

@app.post("/api/capsules/buy")
async def buy_capsule(request: Request):
    """购买胶囊"""
    data = await request.json()
    return await proxy_request(f"{TRADE_SERVICE}/buy", "POST", data)

@app.get("/api/market")
async def get_market():
    """市场概览"""
    return await proxy_request(f"{TRADE_SERVICE}/market", "GET")

@app.get("/api/transactions/{user_id}")
async def get_transactions(user_id: str, limit: int = 20):
    """交易记录"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TRADE_SERVICE}/transactions/{user_id}", params={"limit": limit})
        return JSONResponse(content=resp.json(), status_code=resp.status_code)

# ===================== 聚合查询 =====================

@app.get("/api/dashboard/{user_id}")
async def dashboard(user_id: str):
    """用户仪表板 - 聚合查询"""
    async with httpx.AsyncClient() as client:
        # 并行查询
        wallet, capsules, transactions = await asyncio.gather(
            client.get(f"{TRADE_SERVICE}/wallets/{user_id}"),
            client.get(f"{CAPSULE_SERVICE}/capsules", params={"limit": 10}),
            client.get(f"{TRADE_SERVICE}/transactions/{user_id}", params={"limit": 10}),
            client.get(f"{TRADE_SERVICE}/market"),
        )
        
        return {
            "wallet": wallet.json() if wallet.status_code == 200 else None,
            "recent_capsules": capsules.json() if capsules.status_code == 200 else [],
            "recent_transactions": transactions.json() if transactions.status_code == 200 else [],
            "market": market.json() if market.status_code == 200 else {}
        }

# ===================== 启动 =====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
