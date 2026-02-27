# 双平台开发工作流

## 概述
同时使用 **ChatGPT/Codex 网页端** 和 **Codespaces OpenClaw** 开发，代码通过 GitHub 同步。

```
ChatGPT/Codex 网页 ←→ GitHub ←→ Codespaces OpenClaw
        ↓                ↓              ↓
    复杂代码编写      中央仓库      日常对话/测试
```

---

## 使用方式

### 在 ChatGPT/Codex 中修改代码

1. 访问 https://chatgpt.com/codex
2. 点击 **"Connect to GitHub"**
3. 选择仓库：`SchweinQin/workspace`
4. 选择分支：`main`
5. 直接编辑文件 → 自动提交到 GitHub

### 在 Codespaces OpenClaw 中同步

**方式 A：手动同步（推荐）**
```bash
# 在终端运行
sync
# 或
bash scripts/sync_from_github.sh
```

**方式 B：自动同步（每10分钟）**
```bash
# 已配置 cron，自动拉取
# 查看日志: cat /tmp/sync.log
```

**方式 C：启动时自动同步**
```bash
# 每次启动 Codespaces 时运行
bash scripts/sync_from_github.sh
```

---

## 工作流程示例

### 场景：修改 router/strategy.py

1. **在 ChatGPT/Codex 中：**
   - 打开 `router/strategy.py`
   - 修改代码
   - ChatGPT 自动提交到 GitHub

2. **在 Codespaces 中：**
   ```bash
   sync  # 拉取最新代码
   ```

3. **测试修改：**
   ```bash
   python3 -m unittest router.test_strategy -v
   ```

4. **本地修改后推送：**
   ```bash
   git add .
   git commit -m "更新"
   git push
   # ChatGPT 中会自动显示最新代码
   ```

---

## 备份策略

| 备份类型 | 位置 | 频率 |
|---------|------|------|
| Git 提交 | GitHub | 每次修改 |
| 本地 tar | `/tmp/workspace-dual-*.tgz` | 每天 |
| Git stash | 本地 | 自动（冲突时） |

---

## 注意事项

### ⚠️ 避免冲突

**不要同时在两边修改同一个文件！**

如果冲突：
```bash
# 1. 备份本地更改
git stash

# 2. 拉取远程
sync

# 3. 恢复本地更改
git stash pop

# 4. 手动解决冲突
```

### 🔐 安全

- **不要在 ChatGPT 中提交 .env 文件**
- **Token 只保存在 Codespaces 环境变量中**
- **GitHub 仓库保持私密**

---

## 快速命令

```bash
# 同步代码
sync

# 运行测试
python3 -m unittest router.test_strategy -v

# 检查状态
git status

# 查看日志
tail -f /tmp/sync.log
```

---

## 故障排除

### 同步失败
```bash
# 强制重置到远程版本（会丢失本地未提交更改）
git fetch origin
git reset --hard origin/main
```

### ChatGPT 不显示最新代码
```bash
# 在 ChatGPT 中刷新或重新连接仓库
```

### 权限问题
```bash
# 检查 GitHub Token 是否有效
gh auth status
```
