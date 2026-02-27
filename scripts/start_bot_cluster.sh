#!/usr/bin/env bash
# 多 Bot 启动脚本 - 小秦的 Discord Bot 集群
# 用法: source .env && bash scripts/start_bot_cluster.sh

set -euo pipefail

echo "🤖 启动 Discord Bot 集群..."

# 检查环境变量
if [ -z "${DISCORD_TOKEN_OPENBOT:-}" ]; then
    echo "❌ 错误: DISCORD_TOKEN_OPENBOT 未设置"
    echo "请先运行: source .env"
    exit 1
fi

if [ -z "${DISCORD_TOKEN_BOT2:-}" ]; then
    echo "❌ 错误: DISCORD_TOKEN_BOT2 未设置"
    exit 1
fi

if [ -z "${DISCORD_TOKEN_BOT3:-}" ]; then
    echo "❌ 错误: DISCORD_TOKEN_BOT3 未设置"
    exit 1
fi

echo ""
echo "📋 Bot 配置:"
echo "  Bot1 (openbot) → Codex"
echo "  Bot2           → MiniMax"
echo "  Bot3           → Kimi"
echo ""

# 启动 Bot1 - openbot (Codex)
echo "🚀 启动 Bot1 (openbot - Codex)..."
OPENCLAW_CONFIG_PATH="$HOME/.openclaw/profiles/openbot/openclaw.json" \
DISCORD_TOKEN="$DISCORD_TOKEN_OPENBOT" \
openclaw agent --model openai-codex/gpt-5.2-codex &
BOT1_PID=$!
echo "   PID: $BOT1_PID"

# 启动 Bot2 - MiniMax
echo "🚀 启动 Bot2 (MiniMax)..."
OPENCLAW_CONFIG_PATH="$HOME/.openclaw/profiles/bot2/openclaw.json" \
DISCORD_TOKEN="$DISCORD_TOKEN_BOT2" \
openclaw agent --model minimax-portal/MiniMax-M2.5 &
BOT2_PID=$!
echo "   PID: $BOT2_PID"

# 启动 Bot3 - Kimi
echo "🚀 启动 Bot3 (Kimi)..."
OPENCLAW_CONFIG_PATH="$HOME/.openclaw/profiles/bot3/openclaw.json" \
DISCORD_TOKEN="$DISCORD_TOKEN_BOT3" \
openclaw agent --model kimi-coding/k2p5 &
BOT3_PID=$!
echo "   PID: $BOT3_PID"

echo ""
echo "✅ 所有 Bot 已启动!"
echo ""
echo "📊 状态查看:"
echo "  ps aux | grep openclaw"
echo ""
echo "🛑 停止所有 Bot:"
echo "  kill $BOT1_PID $BOT2_PID $BOT3_PID"
echo ""
echo "💡 提示: 在 Discord 中 @对应的 Bot 即可对话"
