#!/usr/bin/env python3
"""
100个知识胶囊批量生成脚本
用法: python generate_100_capsules.py
"""

import requests
import json
import time
import random

# 配置
OLLAMA_URL = "http://localhost:11434"
CAPSULE_API = "http://localhost:8005"

# 100个主题
TOPICS = [
    # 科技前沿 (20)
    "GPT-5技术原理与应用",
    "Claude AI助手的独特优势", 
    "本地大模型部署完全指南",
    "AI Agent工作原理解析",
    "RAG技术深度解读",
    "多模态AI发展趋势",
    "AI代码生成器使用指南",
    "自动驾驶技术现状",
    "人形机器人发展",
    "AI医疗应用前景",
    "量子计算入门",
    "区块链与AI结合",
    "边缘计算与AI",
    "6G通信技术展望",
    "AI芯片发展趋势",
    "神经形态计算",
    "脑机接口技术",
    "AI安全与对齐",
    "通用人工智能路径",
    "AI伦理框架",
    
    # 商业洞察 (15)
    "商业模式创新法则",
    "精益创业方法论",
    "平台战略精髓",
    "增长黑客实践",
    "颠覆式创新案例",
    "蓝海战略解析",
    "精益运营体系",
    "品牌建设之道",
    "定价策略艺术",
    "用户增长模型",
    "商业画布使用",
    "融资路演技巧",
    "股权分配原则",
    "并购整合要点",
    "全球化扩张策略",
    
    # 投资理财 (15)
    "价值投资哲学",
    "分散投资原则",
    "指数基金指南",
    "债券投资基础",
    "不动产投资",
    "另类投资品种",
    "风险管理体系",
    "资产配置策略",
    "复利的力量",
    "行为金融学",
    "财务自由路径",
    "退休规划指南",
    "税务优化策略",
    "保险配置原则",
    "家族财富传承",
    
    # 知识管理 (15)
    "第二大脑构建",
    "知识管理体系",
    "卡片盒方法论",
    "费曼学习技巧",
    "刻意练习方法",
    "快速阅读技巧",
    "思维导图应用",
    "番茄工作法",
    "深度工作实践",
    "笔记系统设计",
    "信息筛选原则",
    "知识输出策略",
    "跨学科学习法",
    "元认知培养",
    "学习迁移技巧",
    
    # 教育创新 (15)
    "项目式学习",
    "翻转课堂实践",
    "自适应学习系统",
    "游戏化教育",
    "慕课发展趋势",
    "职业教育创新",
    "早期教育科学",
    "批判性思维培养",
    "创造力训练方法",
    "情商教育重要性",
    "STEM教育整合",
    "人工智能教育应用",
    "产教融合模式",
    "终身学习体系",
    "学习动力激发",
    
    # 哲学思辨 (10)
    "存在主义入门",
    "实用主义哲学",
    "辩证思维方法",
    "第一性原理",
    "奥卡姆剃刀",
    "躺平与奋斗",
    "人生意义探寻",
    "自由意志问题",
    "缸中大脑实验",
    "科技与人文",
    
    # 心理学 (10)
    "行为经济学",
    "认知偏差大全",
    "动机心理学",
    "情绪管理技巧",
    "压力应对策略",
    "人际关系心理学",
    "销售心理学",
    "领导力心理学",
    "决策心理学",
    "幸福心理学",
]

# AI科学家角色
ROLES = {
    "munger": "查理·芒格 - 多学科思维模型",
    "yang": "杨振宁 - 科学大家",
    "musk": "埃隆·马斯克 - 第一性原理",
    "tao": "陶哲轩 - 数学直觉",
}

def call_llm(prompt: str) -> str:
    """调用本地大模型"""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "qwen2.5:7b", "prompt": prompt, "stream": False},
            timeout=60
        )
        return resp.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"

def generate_capsule_content(topic: str) -> str:
    """生成胶囊内容"""
    prompt = f"""请用深刻、简洁、有洞察力的方式介绍以下主题:

{topic}

要求:
1. 核心概念解释
2. 关键洞见 (3-5点)
3. 实践建议
4. 独特视角

请用中文回答:"""
    
    content = call_llm(prompt)
    return content

def save_capsule(title: str, content: str, domain: str) -> dict:
    """保存胶囊"""
    try:
        resp = requests.post(
            f"{CAPSULE_API}/capsules",
            json={"title": title, "content": content, "domain": domain},
            timeout=30
        )
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print(f"开始生成 {len(TOPICS)} 个知识胶囊...")
    
    success = 0
    failed = 0
    
    for i, topic in enumerate(TOPICS):
        print(f"[{i+1}/100] 生成: {topic}")
        
        # 生成内容
        content = generate_capsule_content(topic)
        
        if "Error" in content:
            print(f"  ❌ LLM调用失败: {content}")
            failed += 1
            continue
            
        # 保存胶囊
        domain = get_domain(topic)
        result = save_capsule(topic, content, domain)
        
        if "error" in result:
            print(f"  ❌ 保存失败: {result['error']}")
            failed += 1
        else:
            print(f"  ✅ 已创建: {result.get('id', 'unknown')}")
            success += 1
            
        # 避免过快
        time.sleep(1)
        
    print(f"\n完成! 成功: {success}, 失败: {failed}")

def get_domain(topic: str) -> str:
    """确定领域"""
    if topic in TOPICS[0:20]:
        return "科技"
    elif topic in TOPICS[20:35]:
        return "商业"
    elif topic in TOPICS[35:50]:
        return "投资"
    elif topic in TOPICS[50:65]:
        return "知识管理"
    elif topic in TOPICS[65:80]:
        return "教育"
    elif topic in TOPICS[80:90]:
        return "哲学"
    else:
        return "心理学"

if __name__ == "__main__":
    main()
