# openclaw-schwein

OpenClaw workspace focused on **Discord multi-model routing** that can run in GitHub Codespaces.

## What's included
- A practical routing strategy doc for Codex + Kimi + MiniMax in one Discord group.
- A minimal Python router implementation you can run locally/Codespaces.
- Messages containing `优化到kimi` are treated as code-related and routed by the router keyword rules.
- 测试关键词：`codespaces-sync-test`（用于验证 Codespaces 是否同步到最新修改）。
- A Codespaces readiness check script.

## Quick start
```bash
python3 -m router.strategy
python3 -m unittest router.test_strategy -v
bash scripts/check_codespaces_ready.sh
```

## Reference skills source
You can clone external skill references (for study and adaptation) with:
```bash
git clone https://github.com/hesamsheikh/awesome-openclaw-usecases.git /tmp/awesome-openclaw-usecases
```
Then adapt prompt/skill ideas into your own local skill folders.
