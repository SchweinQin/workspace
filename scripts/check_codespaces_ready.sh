#!/usr/bin/env bash
set -euo pipefail

echo "[check] python3 version"
python3 --version

echo "[check] git version"
git --version

echo "[check] router self-check"
python3 -m router.strategy >/tmp/router_strategy.out
cat /tmp/router_strategy.out

echo "[ok] basic environment and local router checks passed"
