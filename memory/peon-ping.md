# peon-ping 安装状态

> Warcraft 风格终端语音通知

## ✅ 已安装

位置: `~/.openclaw/hooks/peon-ping/`

## 使用方法

```bash
# 播放测试音效
~/.openclaw/hooks/peon-ping/peon.sh preview session.start

# 查看帮助
~/.openclaw/hooks/peon-ping/peon.sh --help

# 暂停/恢复
~/.openclaw/hooks/peon-ping/peon.sh pause
~/.openclaw/hooks/peon-ping/peon.sh resume
```

## 音效类别

- session.start - 会话开始
- task.acknowledge - 任务确认
- task.complete - 任务完成
- task.error - 任务错误
- input.required - 需要输入
- resource.limit - 资源限制
- user.spam - 用户消息

## 状态

⚠️ 部分音效包需要下载
⚠️ 需要配置到 OpenClaw 钩子中才能自动触发
