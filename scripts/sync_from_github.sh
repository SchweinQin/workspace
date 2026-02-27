#!/bin/bash
# 自动从 GitHub 拉取最新代码（用于 ChatGPT/Codex 修改后同步）

set -e

echo "[$(date)] 开始同步..."
cd /home/codespace/.openclaw/workspace

# 检查是否有本地未提交更改
if [ -n "$(git status --porcelain)" ]; then
    echo "[$(date)] 本地有未提交更改，先备份..."
    git stash push -m "auto-backup-$(date +%Y%m%d-%H%M%S)"
fi

# 拉取远程最新代码
echo "[$(date)] 拉取远程代码..."
git pull origin main

echo "[$(date)] 同步完成"
