/**
 * OpenClaw Skill: 知识胶囊服务
 * Skill ID: knowledge-capsule
 * 用于咖啡知识存储、检索、溯源
 */

const path = require('path');

// 导入胶囊服务
const capsuleService = require('../services/knowledge-capsule/src/index.js');

module.exports = {
  id: 'knowledge-capsule',
  name: '知识胶囊',
  description: '咖啡知识存储、检索与溯源系统，基于 DATM 评分体系',
  
  // 技能配置
  config: {
    // DATM 评分阈值
    minDatmThreshold: 0.7,
    // 默认返回数量
    defaultLimit: 10,
    // 最大返回数量
    maxLimit: 50
  },

  // 指令定义
  commands: {
    /**
     * 创建知识胶囊
     * 用法: 创建胶囊 [标题] [内容]
     */
    create: {
      description: '创建新的知识胶囊',
      parameters: {
        type: 'object',
        properties: {
          title: { type: 'string', description: '胶囊标题' },
          content: { type: 'string', description: '胶囊内容' },
          tags: { type: 'array', items: { type: 'string' }, description: '标签列表' },
          source: {
            type: 'object',
            properties: {
              university: { type: 'string' },
              author: { type: 'string' },
              date: { type: 'string' },
              url: { type: 'string' }
            }
          },
          datm: {
            type: 'object',
            properties: {
              truth: { type: 'number' },
              goodness: { type: 'number' },
              beauty: { type: 'number' },
              intelligence: { type: 'number' }
            }
          }
        },
        required: ['title', 'content']
      },
      
      async handler(args) {
        const result = capsuleService.createCapsule(args);
        return {
          success: true,
          message: `✅ 胶囊创建成功！ID: ${result.id}`,
          capsuleId: result.id
        };
      }
    },

    /**
     * 搜索知识胶囊
     * 用法: 搜索胶囊 [关键词]
     */
    search: {
      description: '搜索知识胶囊',
      parameters: {
        type: 'object',
        properties: {
          keyword: { type: 'string', description: '搜索关键词' },
          university: { type: 'string', enum: ['天津大学', '复旦大学'] },
          tags: { type: 'string', description: '标签关键词' },
          minDatm: { type: 'number', description: '最低 DATM 评分' },
          limit: { type: 'number', description: '返回数量限制' }
        }
      },
      
      async handler(args) {
        const results = capsuleService.searchCapsules(args);
        
        if (results.length === 0) {
          return {
            success: true,
            message: '未找到相关胶囊',
            results: []
          };
        }

        return {
          success: true,
          message: `找到 ${results.length} 个胶囊`,
          results: results.map(r => ({
            id: r.id,
            title: r.title,
            tags: r.tags,
            datm: r.datm,
            source: r.source_university
          }))
        };
      }
    },

    /**
     * 获取胶囊详情
     */
    get: {
      description: '获取胶囊详情',
      parameters: {
        type: 'object',
        properties: {
          id: { type: 'string', description: '胶囊 ID' }
        },
        required: ['id']
      },
      
      async handler(args) {
        const results = capsuleService.searchCapsules({ limit: 1 });
        const capsule = results.find(r => r.id === args.id);
        
        if (!capsule) {
          return { success: false, message: '胶囊不存在' };
        }

        return {
          success: true,
          capsule
        };
      }
    }
  },

  // 快捷指令（简化用法）
  shortcuts: {
    '胶囊': 'search',
    '新建胶囊': 'create'
  }
};
