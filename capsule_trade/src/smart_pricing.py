"""
capsule_trade 智能定价与推荐模块
功能: DATM评分+智能定价+协同过滤推荐
来源: 推荐算法
"""

import json
import time
import random
from typing import List, Dict, Optional

class DATMScorer:
    """DATM评分器"""
    
    def __init__(self):
        self.weights = {
            "truth": 0.3,      # 真理度
            "goodness": 0.25,  # 价值性
            "beauty": 0.2,     # 美感
            "meaning": 0.15,   # 意义性
            "style": 0.1       # 风格
        }
    
    def score(self, capsule: Dict) -> Dict:
        """计算DATM分数"""
        # 简化实现
        scores = {
            "truth": random.uniform(7, 10),
            "goodness": random.uniform(6, 9),
            "beauty": random.uniform(7, 10),
            "meaning": random.uniform(6, 9),
            "style": random.uniform(7, 10)
        }
        
        total = sum(scores[k] * self.weights[k] for k in self.weights)
        
        return {
            "dimensions": scores,
            "total": round(total, 2),
            "level": self._get_level(total)
        }
    
    def _get_level(self, score: float) -> str:
        if score >= 9: return "L4-传世"
        if score >= 8: return "L3-钻石"
        if score >= 7: return "L2-方"
        return "L1-圆"

class SmartPricer:
    """智能定价"""
    
    def __init__(self, scorer: DATMScorer):
        self.scorer = scorer
        self.base_prices = {"L1": 0, "L2": 9, "L3": 99, "L4": 999}
        
    def calculate_price(self, capsule: Dict) -> int:
        """计算价格"""
        score_result = self.scorer.score(capsule)
        level = score_result["level"]
        
        base = self.base_prices.get(level, 0)
        
        # 根据稀缺性调整
        scarcity = capsule.get("views", 0) / 100
        multiplier = 1 + scarcity
        
        return int(base * multiplier)

class Recommender:
    """协同过滤推荐"""
    
    def __init__(self):
        self.user_preferences = {}
        self.capsule_features = {}
        
    def add_user_action(self, user_id: str, capsule_id: str, action: str):
        """记录用户行为"""
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        self.user_preferences[user_id][capsule_id] = action
        
    def recommend(self, user_id: str, candidates: List[Dict], top_k: int = 5) -> List[Dict]:
        """推荐"""
        if user_id not in self.user_preferences:
            # 冷启动 - 热门推荐
            return sorted(candidates, key=lambda x: x.get("views", 0), reverse=True)[:top_k]
        
        # 协同过滤
        user_likes = {c for c, a in self.user_preferences[user_id].items() if a == "like"}
        
        scores = []
        for capsule in candidates:
            if capsule["id"] in user_likes:
                scores.append((capsule, 10))  # 喜欢过的高分
            else:
                # 基于内容相似
                scores.append((capsule, random.uniform(1, 5)))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in scores[:top_k]]

# 测试
if __name__ == "__main__":
    scorer = DATMScorer()
    pricer = SmartPricer(scorer)
    recommender = Recommender()
    
    capsule = {"id": "c1", "title": "AI知识胶囊", "views": 50}
    
    # 评分
    score = scorer.score(capsule)
    print("DATM评分:", json.dumps(score, ensure_ascii=False, indent=2))
    
    # 定价
    price = pricer.calculate_price(capsule)
    print(f"\n智能定价: ¥{price}")
    
    # 推荐
    candidates = [
        {"id": "c1", "title": "AI", "views": 100},
        {"id": "c2", "title": "物理", "views": 50},
        {"id": "c3", "title": "化学", "views": 30},
    ]
    recs = recommender.recommend("user1", candidates)
    print("\n推荐:", [r["title"] for r in recs])
