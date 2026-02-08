/**
 * 知识胶囊 RESTful API 服务器
 * 基于 Wanyview kai-capsule-service 设计
 */

const express = require('express');
const cors = require('cors');
const { createCapsule, searchCapsules, initDB } = require('./index.js');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件
app.use(cors());
app.use(express.json());

// 初始化数据库
initDB();

// ========== 胶囊 CRUD ==========

// 创建胶囊
app.post('/api/capsules', (req, res) => {
  try {
    const result = createCapsule(req.body);
    res.status(201).json({
      success: true,
      message: '胶囊创建成功',
      ...result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// 搜索胶囊
app.get('/api/capsules', (req, res) => {
  try {
    const { keyword, university, tags, minDatm, limit } = req.query;
    const results = searchCapsules({
      keyword,
      university,
      tags,
      minDatm: minDatm ? parseFloat(minDatm) : undefined,
      limit: limit ? parseInt(limit) : 20
    });
    
    res.json({
      success: true,
      count: results.length,
      results
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// 获取单个胶囊
app.get('/api/capsules/:id', (req, res) => {
  try {
    const results = searchCapsules({ limit: 100 });
    const capsule = results.find(c => c.id === req.params.id);
    
    if (!capsule) {
      return res.status(404).json({
        success: false,
        error: '胶囊不存在'
      });
    }
    
    res.json({
      success: true,
      capsule
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ========== DATM 评分 ==========

// 计算 DATM 评分
app.post('/api/datm/calculate', (req, res) => {
  const { truth, goodness, beauty, intelligence } = req.body;
  
  const datm = {
    truth: truth || 0.5,
    goodness: goodness || 0.5,
    beauty: beauty || 0.5,
    intelligence: intelligence || 0.5
  };
  
  // 计算综合评分
  const overall = (datm.truth + datm.goodness + datm.beauty + datm.intelligence) / 4;
  
  res.json({
    success: true,
    datm,
    overall,
    grade: overall >= 0.8 ? 'A' : overall >= 0.6 ? 'B' : overall >= 0.4 ? 'C' : 'D'
  });
});

// ========== 健康检查 ==========

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════╗
║  知识胶囊 API 服务已启动                          ║
║  ------------------------------------------------ ║
║  地址: http://localhost:${PORT}                    ║
║  ------------------------------------------------ ║
║  端点:                                            ║
║  POST   /api/capsules       - 创建胶囊           ║
║  GET    /api/capsules       - 搜索胶囊           ║
║  GET    /api/capsules/:id   - 获取胶囊详情       ║
║  POST   /api/datm/calculate - 计算 DATM 评分     ║
║  GET    /health             - 健康检查           ║
╚═══════════════════════════════════════════════════╝
  `);
});

module.exports = app;
