/**
 * 知识胶囊服务测试
 */

const { createCapsule, searchCapsules, initDB } = require('./src/index.js');

console.log('🧪 测试知识胶囊服务...\n');

// 初始化
initDB();
console.log('✅ 数据库初始化完成\n');

// 创建测试胶囊
const testCapsule = {
  id: 'test-capsule-001',
  title: '耶加雪菲咖啡风味特征',
  content: '耶加雪菲是埃塞俄比亚的精品咖啡，以其明亮的花香和柑橘酸质著称。',
  tags: ['咖啡', '耶加雪菲', '风味'],
  source: {
    university: '天津大学',
    author: '咖啡研究组',
    date: '2026-01-15',
    url: 'https://example.com/yirgacheffe'
  },
  datm: {
    truth: 0.90,
    goodness: 0.85,
    beauty: 0.88,
    intelligence: 0.82
  }
};

const result = createCapsule(testCapsule);
console.log('✅ 创建胶囊:', result);

// 搜索测试
const searchResults = searchCapsules({
  keyword: '耶加雪菲',
  minDatm: 0.8
});

console.log('\n🔍 搜索结果:');
console.log(`找到 ${searchResults.length} 个胶囊`);
searchResults.forEach(c => {
  console.log(`- ${c.title} (DATM: ${c.datm.truth}/${c.datm.goodness}/${c.datm.beauty}/${c.datm.intelligence})`);
});

console.log('\n🎉 所有测试通过！');
