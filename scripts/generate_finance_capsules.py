"""
金融知识胶囊生成器
特点: 高逻辑性 + 明确结论 + 投资指导
"""

import requests
import json

OLLAMA_URL = "http://localhost:11434"
CAPSULE_API = "http://localhost:8005"

# 金融领域10个主题
TOPICS = [
    "A股2026年牛市能持续吗",
    "如何判断一只股票被低估",
    "散户投资常见的致命错误",
    "基金定投最佳策略",
    "A股科技板块投资逻辑",
    "如何阅读财务报表关键指标",
    "2026年最有潜力的行业",
    "股票止损还是补仓",
    "价值投资 vs 趋势投资",
    "散户如何建立自己的投资体系",
]

def call_llm(prompt: str) -> str:
    """调用本地大模型"""
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "qwen2.5:7b", "prompt": prompt, "stream": False},
            timeout=90
        )
        return resp.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"

def generate_finance_capsule(topic: str) -> str:
    """生成有逻辑性、有结论、有指导的金融胶囊"""
    
    prompt = f"""你是一位资深金融分析师和投资顾问。请针对以下主题，写一篇有深度、有逻辑、有明确结论的知识胶囊。

主题: {topic}

要求:
1. 【现状分析】当前市场/投资标的的实际情况
2. 【核心逻辑】背后的投资逻辑和原理
3. 【明确结论】你的核心观点和判断（必须明确说清楚看多还是看空）
4. 【操作建议】具体可执行的投资建议
5. 【风险提示】需要注意的风险

格式要求:
- 每个部分都要有深度分析，不能只是列举
- 结论要明确，不能含糊
- 建议要具体可执行
- 必须从投资价值角度分析

请用中文，逻辑清晰，观点鲜明:"""
    
    return call_llm(prompt)

def save_capsule(title: str, content: str) -> dict:
    """保存胶囊"""
    try:
        resp = requests.post(
            f"{CAPSULE_API}/capsules",
            json={
                "title": title, 
                "content": content, 
                "domain": "金融",
                "tags": ["金融", "投资", "股票"]
            },
            timeout=30
        )
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print(f"开始生成10个金融胶囊...\n")
    
    for i, topic in enumerate(TOPICS):
        print(f"[{i+1}/10] {topic}")
        
        # 生成内容
        content = generate_finance_capsule(topic)
        
        if "Error" in content:
            print(f"  ❌ 生成失败")
            continue
            
        # 保存胶囊
        result = save_capsule(topic, content)
        
        if "error" in result:
            print(f"  ❌ 保存失败")
        else:
            print(f"  ✅ 已创建")
            
    print("\n完成!")

if __name__ == "__main__":
    main()
