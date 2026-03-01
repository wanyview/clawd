"""
api_gateway 限流与熔断模块
功能: 令牌桶限流 + 熔断降级
来源: 高可用架构
"""

import time
from typing import Dict, Optional
from collections import defaultdict
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # 正常
    OPEN = "open"          # 熔断
    HALF_OPEN = "half_open"  # 半开

class TokenBucket:
    """令牌桶限流器"""
    
    def __init__(self, rate: int, capacity: int):
        self.rate = rate        # 每秒生成令牌数
        self.capacity = capacity  # 桶容量
        self.tokens = capacity
        self.last_time = time.time()
        
    def allow_request(self) -> bool:
        """是否允许请求"""
        now = time.time()
        elapsed = now - self.last_time
        
        # 补充令牌
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.rate
        )
        self.last_time = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class CircuitBreaker:
    """熔断器"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        
    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(f"⚠️ 熔断器打开 (失败{self.failure_count}次)")
    
    def record_success(self):
        """记录成功"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        
    def allow_request(self) -> bool:
        """是否允许请求"""
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            # 检查超时
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                print("🔄 熔断器进入半开状态")
                return True
            return False
            
        # 半开状态
        return True

class RateLimiter:
    """限流管理器"""
    
    def __init__(self):
        self.limiters: Dict[str, TokenBucket] = {}
        self.circuits: Dict[str, CircuitBreaker] = {}
        
        # 默认配置
        self.default_limits = {
            "default": {"rate": 100, "capacity": 100},
            "premium": {"rate": 1000, "capacity": 1000},
            "enterprise": {"rate": 10000, "capacity": 10000},
        }
    
    def add_limiter(self, tier: str, rate: int, capacity: int):
        """添加限流器"""
        self.limiters[tier] = TokenBucket(rate, capacity)
        self.circuits[tier] = CircuitBreaker()
        print(f"✅ 添加限流器: {tier} (rate={rate}/s, cap={capacity})")
    
    def check_request(self, tier: str = "default") -> tuple[bool, str]:
        """检查请求"""
        # 检查限流
        limiter = self.limiters.get(tier)
        if limiter and not limiter.allow_request():
            return False, "rate_limit_exceeded"
        
        # 检查熔断
        circuit = self.circuits.get(tier)
        if circuit and not circuit.allow_request():
            return False, "circuit_breaker_open"
        
        return True, "ok"
    
    def record_success(self, tier: str = "default"):
        """记录成功"""
        if tier in self.circuits:
            self.circuits[tier].record_success()
    
    def record_failure(self, tier: str = "default"):
        """记录失败"""
        if tier in self.circuits:
            self.circuits[tier].record_failure()

# 测试
if __name__ == "__main__":
    limiter = RateLimiter()
    
    # 添加限流器
    limiter.add_limiter("default", rate=10, capacity=20)
    limiter.add_limiter("premium", rate=100, capacity=200)
    
    # 测试请求
    for i in range(25):
        allowed, msg = limiter.check_request("default")
        status = "✅" if allowed else "❌"
        if not allowed:
            print(f"{status} 请求{i+1}: {msg}")
    
    print("\n测试熔断:")
    circuit = limiter.circuits["default"]
    for i in range(6):
        circuit.record_failure()
        print(f"失败{i+1}次: 状态={circuit.state.value}")
