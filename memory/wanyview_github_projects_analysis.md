# wanyview GitHub 项目能力分析报告

## 生成时间: 2026-02-08

---

## 📋 项目总览

### AI 助手核心系统
| 项目 | 语言 | 描述 |
|------|------|------|
| kai-api-gateway | Python | Kai 统一 API 网关 - FastAPI/httpx |
| kai-auth-service | Python | Kai 用户认证服务 - JWT/SQLite |
| kai-capsule-service | Python | Kai 知识胶囊服务 - SQLite/DATM/碰撞算法 |

### 知识管理平台
| 项目 | 语言 | 描述 |
|------|------|------|
| CapsuleHub | Python | AI 时代的知识资产交易所 |
| Dreamsense- | - | 学习主理人学习方法系统 |

### AI 应用
| 项目 | 语言 | 描述 |
|------|------|------|
| Matrix-BNUHS | TypeScript | 附中矩阵 - Google AI Studio + Gemini |
| AIdison | TypeScript | BCI 脑机接口助手 |
| GeminiCast | TypeScript | Gemini AI 播客生成 |

### 其他项目
| 项目 | 描述 |
|------|------|
| BNU-MATRIX | BNU-MATRIX MAS |
| Know_Salon_ByMAS | TIER 咖啡知识沙龙知识库 |
| SuiLight | 知识胶囊 |
| SuiGuang-Nexus | 随光知识中枢 |
| TIER_Suiguang_Android | 随光沙龙 Android |

---

## 🎯 核心技术能力

### 1. 知识胶囊系统 (DATM)
- **Truth (真)** - 科学性: 咖啡的化学成分、提取原理、来源追溯
- **Goodness (善)** - 实用性: 怎么做咖啡、什么适合什么场景
- **Beauty (美)** - 美学性: 咖啡的品鉴、风味描述、艺术表达
- **Intelligence (智)** - 智慧性: 咖啡的历史、文化、社会意义

### 2. 溯源系统
- 版本历史管理
- 演进关系追踪
- 引用计数系统
- 知识图谱接口
- 验证记录管理

### 3. AI 角色系统
- 100+ 预设思维教练角色
- 心理学家、咖啡师、历史学家、植物学家
- 多角色辩论/讨论功能

### 4. 用户认证
- JWT Token 认证
- SQLite 本地存储
- 用户权限管理

---

## 🔧 API 能力

### 知识胶囊 API
- 创建/更新/删除胶囊
- 获取胶囊列表
- 精选胶囊功能
- 胶囊溯源查询
- 知识图谱遍历

### 用户系统 API
- 用户注册/登录
- Token 刷新
- 权限验证

---

## 📊 数据模型

### Capsule (胶囊)
```python
{
    "id": str,
    "title": str,
    "content": str,
    "datm_score": {
        "truth": float,      # 真
        "goodness": float,   # 善
        "beauty": float,     # 美
        "intelligence": float # 智
    },
    "author_id": str,
    "tags": List[str],
    "created_at": datetime,
    "updated_at": datetime,
    "version": int,
    "parent_id": Optional[str],  # 演进关系
    "citations": int,            # 引用计数
    "featured": bool             # 精选
}
```

---

## 🎓 教育/知识场景

### TIER 咖啡知识沙龙
- 知识来源: 天津大学、复旦大学
- 核心方法: DATM 知识评估
- 目标: 培养"知识主理人"

### 知识问答
- 多角度回答问题
- 不同角色视角
- 辩论式讨论

---

## 💡 建议集成到 OpenClaw 的能力

### 优先级 1 (核心)
1. ✅ 飞书通道 - 已配置
2. 📝 知识胶囊存储 - 需要开发
3. 📝 DATM 评分系统 - 需要开发
4. 📝 多角色 AI 对话 - 需要开发

### 优先级 2 (增强)
5. 📝 知识溯源功能
6. 📝 用户认证系统
7. 📝 精选推荐算法

### 优先级 3 (高级)
8. 📝 知识图谱可视化
9. 📝 引用计数系统
10. 📝 版本演进追踪

---

## 🔗 相关链接

- 知识库: CapsuleHub
- 认证服务: kai-auth-service
- API 网关: kai-api-gateway
- 知识胶囊: kai-capsule-service
- 学习系统: Dreamsense-

---

*报告生成时间: 2026-02-08*
