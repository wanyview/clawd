/**
 * Feishu Bot 配置与集成
 * 用于 TIER 咖啡知识沙龙
 */

const fs = require('fs-extra');
const path = require('path');

// 配置文件路径
const CONFIG_DIR = path.join(process.env.APPDATA || '', '.openclaw', 'config');
const CONFIG_PATH = path.join(CONFIG_DIR, 'feishu-bots.json');

// Bot 配置结构
const defaultConfig = {
  bots: {
    primary: {
      appId: 'cli_a90d40c8af385bc6',
      appSecret: '', // 待填写
      name: 'TIER咖啡助手',
      permissions: ['contact:contact.base:readonly'],
      status: 'pending' // pending, authorized, error
    },
    kai: {
      appId: '', // 待用户提供
      appSecret: '',
      name: 'KAI数字主理人',
      permissions: [],
      status: 'pending'
    }
  },
  defaultBot: 'primary',
  features: {
    autoReply: true,
    knowledgeSearch: true,
    capsuleCreation: true
  }
};

// 加载配置
function loadConfig() {
  fs.ensureDirSync(CONFIG_DIR);
  
  if (!fs.existsSync(CONFIG_PATH)) {
    fs.writeJsonSync(CONFIG_PATH, defaultConfig);
    return defaultConfig;
  }
  
  return fs.readJsonSync(CONFIG_PATH);
}

// 保存配置
function saveConfig(config) {
  fs.writeJsonSync(CONFIG_PATH, config, { spaces: 2 });
}

// 更新 Bot 状态
function updateBotStatus(botId, status, error = null) {
  const config = loadConfig();
  
  if (config.bots[botId]) {
    config.bots[botId].status = status;
    if (error) {
      config.bots[botId].lastError = error;
    }
    saveConfig(config);
    return true;
  }
  
  return false;
}

// 添加新 Bot
function addBot(botId, appId, appSecret, name = '新Bot') {
  const config = loadConfig();
  
  config.bots[botId] = {
    appId,
    appSecret,
    name,
    permissions: [],
    status: 'pending'
  };
  
  saveConfig(config);
  return config.bots[botId];
}

// 获取授权 URL
function getAuthUrl(botId = 'primary') {
  const config = loadConfig();
  const bot = config.bots[botId];
  
  if (!bot) return null;
  
  return `https://open.feishu.cn/app/${bot.appId}/auth?q=contact:contact.base:readonly`;
}

module.exports = {
  loadConfig,
  saveConfig,
  updateBotStatus,
  addBot,
  getAuthUrl,
  defaultConfig
};
