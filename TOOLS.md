# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

## TTS / 语音
- **本地 TTS**: sherpa-onnx (离线，无需网络)
- **云端 TTS + 播客 + 视频 + 图片**: ListenHub (需要 API Key)
- 默认语音偏好: 待配置

## InStreet (AI Agent 社交网络)
- **Base URL**: https://instreet.coze.site
- **Username**: kai
- **API Key**: sk_inst_d2cd4c99c2b99a3b52d9f0d354a5277d
- 获取 API Key: https://listenhub.ai/dashboard
- 设置: `export LISTENHUB_API_KEY="your-key"`
- 支持: 播客、视频、TTS、图片
- 位置: ~/.openclaw/skills/listenhub/

---

Add whatever helps you do your job. This is your cheat sheet.
