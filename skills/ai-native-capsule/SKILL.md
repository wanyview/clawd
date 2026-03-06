# AI原生胶囊 Skill

## 概述

这是一个让AI Agent可以直接调用的知识胶囊系统设计规范。

## 胶囊结构

每个胶囊包含三层：

```json
{
  "capsule": {
    "id": "kc_xxx",
    "title": "胶囊名称",
    
    "red_layer": {
      "type": "human_readable",
      "format": "markdown",
      "content": "人类可读内容"
    },
    
    "blue_layer": {
      "type": "ai_native",
      "format": "json",
      "content": {
        "think_pattern": {...},
        "trigger": {...},
        "tools_needed": [...],
        "reasoning": {...},
        "response": {...}
      }
    },
    
    "black_layer": {
      "type": "metadata",
      "density": 85,
      "level": "core|processed|filtered",
      "tags": ["#tag1"],
      "created_at": "2026-03-06"
    }
  }
}
```

## 核心字段说明

### blue_layer (AI原生)

| 字段 | 类型 | 说明 |
|------|------|------|
| think_pattern.mode | string | 思维模式: concept_definition/extraction/retrieval/reasoning/agent |
| think_pattern.process | array | 处理步骤列表 |
| think_pattern.parallel | boolean | 是否并行处理 |
| trigger.user_asks | array | 触发问题模式 |
| trigger.confidence_threshold | float | 置信度阈值 |
| tools_needed | array | 需要调用的工具 |
| reasoning.chain | array | 推理链 |
| reasoning.logic | string | IF...THEN...逻辑 |
| response.format | string | 输出格式: text/json/structured |
| response.template | string | 响应模板 |

### 工具标记

```json
"tools_needed": {
  "browser": ["navigate", "click", "fill", "extract"],
  "search": ["web_search", "knowledge_search"],
  "llm": ["analyze", "generate", "extract"],
  "code": ["execute", "calculate"],
  "memory": ["read", "write", "search"]
}
```

## 思维模式

### 1. concept_definition
- 用途: 概念定义类问题
- 流程: 解析意图 → 匹配知识库 → 直接回答

### 2. structure_extraction
- 用途: 信息提取类任务
- 流程: 接收文本 → LLM分析 → 结构化输出

### 3. hybrid_retrieval
- 用途: 知识检索
- 流程: query → 并发搜索 → 融合 → 重排 → 返回

### 4. data_driven_decision
- 用途: 数据驱动的决策
- 流程: 解析数据 → 对比分析 → 计算提升 → 给出建议

### 5. multi_step_pipeline
- 用途: 多步骤处理
- 流程: Stage1 → Stage2 → Stage3 → Stage4

### 6. agent_workflow
- 用途: Agent自主任务
- 流程: 理解 → 规划 → 工具 → 执行 → 验证 → 反思

## 使用示例

### 当用户问"什么是知识胶囊"时

```json
{
  "capsule_id": "kc_001",
  "think_pattern": {
    "mode": "concept_definition"
  },
  "trigger": {
    "user_asks": ["什么是知识胶囊", "knowledge capsule"]
  },
  "reasoning": {
    "chain": [
      "premise: 知识管理面临信息过载",
      "solution: AI自动生成元数据",
      "result: knowledge_capsule"
    ]
  },
  "response": {
    "template": "【定义】{概念}是{核心特征}，主要应用于{场景}。"
  }
}
```

### 当需要检索知识时

```json
{
  "capsule_id": "kc_005",
  "think_pattern": {
    "mode": "hybrid_retrieval",
    "parallel": true
  },
  "tools_needed": [
    {"tool": "semantic_search", "weight": 0.5},
    {"tool": "keyword_search", "weight": 0.2},
    {"tool": "graph_db", "weight": 0.2}
  ]
}
```

## 密度分级

| 等级 | 分数 | 处理 |
|------|------|------|
| 🌿 核心A | ≥90 | 直接入库，定价¥99 |
| 🌿 核心B | 80-89 | 标准库，定价¥59 |
| 🍂 加工 | 60-79 | AI浓缩后入库 |
| 🗑 过滤 | <60 | 不入库 |

## 调用函数

```python
# 创建胶囊
def create_capsule(text, source="manual"):
    # 1. 人类理解层
    human_content = generate_human_readable(text)
    
    # 2. AI理解层  
    ai_native = generate_ai_native(text)
    
    # 3. 计算密度
    density = calculate_density(text)
    
    return {
        "red_layer": human_content,
        "blue_layer": ai_native,
        "black_layer": {"density": density}
    }

# 检索胶囊
def retrieve_capsules(query, top_k=5):
    # 混合检索
    results = hybrid_search(query)
    return results[:top_k]
```

## 适用场景

- 个人知识管理
- AI Agent知识调用
- RAG系统构建
- 知识库索引
- 智能问答系统

---

*此Skill定义用于AI Agent调用知识胶囊的标准格式*
