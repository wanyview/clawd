# 知识图谱API

## 概述
提供知识胶囊之间的关联查询

## 接口

### 获取胶囊关联
GET /capsules/{id}/related?limit=5

### 获取领域图谱
GET /domains/graph

## 数据结构
```json
{
  "nodes": [{"id": "capsule_1", "domain": "AI"}],
  "links": [{"source": "capsule_1", "target": "capsule_2", "weight": 0.8}]
}
```

