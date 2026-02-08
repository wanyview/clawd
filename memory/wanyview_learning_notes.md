# Wanyview GitHub 项目学习笔记
# 仓库地址: https://github.com/wanyview

## 核心项目清单 (31+ Repos)

### 1. CapsuleHub (胶囊中心)
**定位**: 知识胶囊存储与管理系统
**技术栈**: Node.js, SQLite, JWT Auth
**核心功能**:
- 胶囊创建/编辑/删除
- 胶囊搜索与标签
- 用户权限管理
- 胶囊分享与导出

**DATM 评分系统**:
- Truth (真理值) - 知识准确性
- Goodness (善良值) - 价值观正向性
- Beauty (美丽值) - 美学价值
- Intelligence (智慧值) - 实用性

### 2. kai-capsule-service
**定位**: 知识胶囊 API 服务
**特点**:
- RESTful API 设计
- 支持批量操作
- 缓存优化
- 日志追踪

### 3. Dreamsense- (护理系统)
**定位**: 多角色 AI 护理助手
**特点**:
- 角色切换机制
- 上下文记忆
- 情感识别
- 多模态交互

### 4. Matrix-BNUHS (北京中医药大学)
**定位**: 医疗知识图谱
**技术**:
- 知识图谱构建
- 实体关系抽取
- 智能问答

### 5. 其他重要项目
- **kai-* 系列** - 个人 AI 助手
- **dreamsense-* 系列** - 护理/陪伴机器人
- **Capsule*** 系列 - 知识管理工具

## 技术架构总结

### 后端
- Node.js / Express
- SQLite (轻量数据库)
- JWT (认证)
- WebSocket (实时通信)

### 前端
- React / Vue
- 组件化设计
- 响应式布局

### AI 集成
- 多模型支持
- Prompt 工程
- RAG 检索增强

## 可复用的设计模式

### 1. 胶囊模式
```javascript
{
  id: 'uuid',
  title: '标题',
  content: '内容',
  tags: ['标签1', '标签2'],
  source: { university, author, date },
  datm: { truth, goodness, beauty, intelligence },
  created_at: '时间戳'
}
```

### 2. 多角色路由
```javascript
const roles = {
  barista: { skills: ['brewing', 'extraction'] },
  qgrader: { skills: ['tasting', 'grading'] },
  scholar: { skills: ['history', 'research'] }
};
```

### 3. 知识溯源
- 记录来源 (university, author)
- 记录时间 (date)
- DATM 评分 (truth/goodness/beauty/intelligence)
- 版本控制 (version)

## 下一步计划

1. ✅ 已集成: 知识胶囊服务 (DATM 评分)
2. ✅ 已集成: 多角色系统设计
3. ⏳ 待集成: 胶囊 Hub UI
4. ⏳ 待集成: 知识图谱
5. ⏳ 待集成: RAG 检索增强

## 学习心得

### 核心价值
1. **知识胶囊化** - 将碎片化知识结构化
2. **DATM 评估** - 多维度知识质量评估
3. **角色专业化** - 垂直领域专家系统
4. **溯源可信** - 知识来源追踪

### 技术亮点
1. 轻量级方案 (SQLite + Node.js)
2. 标准化接口 (RESTful API)
3. 模块化设计 (Service + Skill)
4. 可扩展架构 (Plugin + Hook)

---
*最后更新: 2026-02-08*
*学习人: KAI*
