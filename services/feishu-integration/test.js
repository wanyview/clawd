/**
 * Feishu 集成测试
 */

const { loadConfig, getAuthUrl, updateBotStatus } = require('./src/config.js');

console.log('📱 Feishu 集成测试\n');

const config = loadConfig();
console.log('✅ 配置加载成功');
console.log('\n🤖 Bot 列表:');

Object.entries(config.bots).forEach(([id, bot]) => {
  console.log(`\n  [${id}] ${bot.name}`);
  console.log(`     AppID: ${bot.appId ? bot.appId.substring(0, 10) + '...' : '未配置'}`);
  console.log(`     状态: ${bot.status}`);
});

console.log('\n🔗 授权 URL:');
console.log(getAuthUrl('primary'));

console.log('\n🎉 配置完成！');
