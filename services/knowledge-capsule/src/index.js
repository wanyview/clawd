/**
 * 知识胶囊服务 - 核心模块
 * 基于 DATM 评分体系 (Truth/Goodness/Beauty/Intelligence)
 */

const path = require('path');
const fs = require('fs-extra');
const Database = require('better-sqlite3');

// 配置
const DATA_DIR = path.join(process.env.APPDATA || '', '.openclaw', 'data');
const DB_PATH = path.join(DATA_DIR, 'knowledge_capsules.db');

// 初始化数据库
function initDB() {
  fs.ensureDirSync(DATA_DIR);
  
  const db = new Database(DB_PATH);
  
  db.exec(`
    CREATE TABLE IF NOT EXISTS capsules (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      content TEXT,
      tags TEXT,
      source_university TEXT,
      source_author TEXT,
      source_date TEXT,
      source_url TEXT,
      datm_truth REAL DEFAULT 0.5,
      datm_goodness REAL DEFAULT 0.5,
      datm_beauty REAL DEFAULT 0.5,
      datm_intelligence REAL DEFAULT 0.5,
      created_at TEXT DEFAULT (datetime('now')),
      version INTEGER DEFAULT 1
    )
  `);
  
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_tags ON capsules(tags);
    CREATE INDEX IF NOT EXISTS idx_university ON capsules(source_university);
  `);
  
  return db;
}

// 创建胶囊
function createCapsule(data) {
  const db = initDB();
  
  const stmt = db.prepare(`
    INSERT INTO capsules (
      id, title, content, tags,
      source_university, source_author, source_date, source_url,
      datm_truth, datm_goodness, datm_beauty, datm_intelligence
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  
  stmt.run(
    data.id || generateUUID(),
    data.title,
    data.content,
    JSON.stringify(data.tags || []),
    data.source?.university,
    data.source?.author,
    data.source?.date,
    data.source?.url,
    data.datm?.truth || 0.5,
    data.datm?.goodness || 0.5,
    data.datm?.beauty || 0.5,
    data.datm?.intelligence || 0.5
  );
  
  return { success: true, id: data.id };
}

// 检索胶囊
function searchCapsules(query) {
  const db = initDB();
  
  let sql = 'SELECT * FROM capsules WHERE 1=1';
  const params = [];
  
  if (query.keyword) {
    sql += ' AND (title LIKE ? OR content LIKE ?)';
    params.push(`%${query.keyword}%`, `%${query.keyword}%`);
  }
  
  if (query.university) {
    sql += ' AND source_university = ?';
    params.push(query.university);
  }
  
  if (query.tags) {
    sql += ' AND tags LIKE ?';
    params.push(`%${query.tags}%`);
  }
  
  if (query.minDatm) {
    const min = query.minDatm;
    sql += ` AND datm_truth >= ? AND datm_goodness >= ? AND datm_beauty >= ? AND datm_intelligence >= ?`;
    params.push(min, min, min, min);
  }
  
  sql += ' ORDER BY created_at DESC LIMIT ?';
  params.push(query.limit || 20);
  
  const stmt = db.prepare(sql);
  const results = stmt.all(...params);
  
  return results.map(r => ({
    ...r,
    tags: JSON.parse(r.tags || '[]'),
    datm: {
      truth: r.datm_truth,
      goodness: r.datm_goodness,
      beauty: r.datm_beauty,
      intelligence: r.datm_intelligence
    }
  }));
}

// 辅助函数
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0;
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

module.exports = {
  initDB,
  createCapsule,
  searchCapsules
};
