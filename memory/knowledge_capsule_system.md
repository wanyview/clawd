# 知识胶囊系统 (Knowledge Capsule System)

## 基于 wanyview DATM 评分体系

### 胶囊结构
```json
{
  "id": "capsule_uuid",
  "title": "咖啡知识标题",
  "content": "知识内容",
  "tags": ["咖啡", "品鉴", "产地"],
  "source": {
    "university": "天津大学|复旦大学",
    "author": "来源作者",
    "date": "2026-01-01",
    "url": "https://..."
  },
  "datm": {
    "truth": 0.85,      // 真理值
    "goodness": 0.90,   // 善良值
    "beauty": 0.80,     // 美丽值
    "intelligence": 0.88  // 智慧值
  },
  "created_at": "2026-02-08T23:40:00Z",
  "version": 1
}
```

### 胶囊类型
1. **咖啡品种胶囊** - 品种特性、产地、风味
2. **冲煮技术胶囊** - 萃取方法、参数、技巧
3. **品鉴知识胶囊** - 感官评价、风味轮、评分
4. **行业洞察胶囊** - 市场趋势、行业动态

### 核心功能
- [ ] 创建胶囊（支持DATM评分）
- [ ] 检索胶囊（关键词、标签、评分范围）
- [ ] 胶囊溯源（追踪知识来源）
- [ ] 胶囊分享（导出、导入）
- [ ] 胶囊对比（多维度评分对比）

### 数据存储
- SQLite 数据库：`~/.openclaw/data/knowledge_capsules.db`
- 备份目录：`~/.openclaw/data/capsules_backup/`
