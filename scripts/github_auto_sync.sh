#!/bin/bash
# TIER咖啡 - GitHub系统集群常态化更新脚本
# 使用方法: ./github_auto_sync.sh [push|pull|status]

ACTION=${1:-status}
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== TIER GitHub常态化更新 $DATE ==="

REPOS=(
  "CapsuleHub:知识胶囊核心服务"
  "Matrix-BNUHS-v2:附中矩阵"
  "capsule_service_v2:胶囊服务V2"
  "kai-hub:知识枢纽"
  "kai-meta-hub:元枢纽"
  "kaimetahub:MetaHub"
  "star-office-ui:StarOfficeUI"
  "SuiLight:知识沙龙"
  "emergence-engine:涌现引擎"
)

case $ACTION in
  "status")
    echo "📊 仓库状态检查"
    echo "===================="
    for repo in "${REPOS[@]}"; do
      dir="${repo%%:*}"
      desc="${repo##*:}"
      cd ~/clawd/$dir 2>/dev/null || continue
      changes=$(git status --short 2>/dev/null | wc -l | tr -d ' ')
      if [ "$changes" -gt 0 ]; then
        echo "🔴 $dir ($desc): $changes 个待提交"
      else
        echo "✅ $dir ($desc): 无变更"
      fi
    done
    ;;

  "push")
    echo "📤 推送所有仓库"
    echo "===================="
    for repo in "${REPOS[@]}"; do
      dir="${repo%%:*}"
      desc="${repo##*:}"
      cd ~/clawd/$dir 2>/dev/null || continue
      changes=$(git status --short | wc -l | tr -d ' ')
      if [ "$changes" -gt 0 ]; then
        echo "📤 推送 $dir..."
        git add -A
        git commit -m "update: $DATE" 2>/dev/null
        git push origin main 2>/dev/null && echo "  ✅ 成功" || echo "  ❌ 失败"
      else
        echo "✅ $dir: 无变更"
      fi
    done
    ;;

  "pull")
    echo "📥 拉取所有仓库"
    echo "===================="
    for repo in "${REPOS[@]}"; do
      dir="${repo%%:*}"
      desc="${repo##*:}"
      cd ~/clawd/$dir 2>/dev/null || continue
      echo "📥 拉取 $dir..."
      git pull origin main 2>/dev/null && echo "  ✅ 成功" || echo "  ⚠️ 无更新"
    done
    ;;

  *)
    echo "用法: ./github_auto_sync.sh [status|push|pull]"
    ;;
esac

echo "===================="
echo "完成 $DATE"
