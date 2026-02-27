#!/usr/bin/env python3
"""Enhanced OpenClaw model router.

Route by content type:
- Code issues → Codex (primary) + Kimi (auxiliary)
- General chat → MiniMax (primary) + Kimi (auxiliary)
"""

from __future__ import annotations

import os
import re
from typing import Any

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cpp", ".c", ".cs", ".php", ".rb", ".swift", ".kt", ".sql", ".sh", ".yaml", ".yml", ".json"}

CODE_KEYWORDS = {"报错", "stack trace", "traceback", "review", "代码审查", "重构", "函数", "api", "sql", "bug", "exception", "debug", "测试", "fix", "代码", "编译", "运行失败", "error", "代码问题"}

FILE_PATTERN = re.compile(r"\b[\w\-./]+(\.[A-Za-z0-9]+)\b")

def looks_like_code_task(message: str) -> tuple[bool, str]:
    msg = message.lower()
    if "```" in message:
        return True, "contains_code_fence"
    for keyword in CODE_KEYWORDS:
        if keyword in msg:
            return True, f"keyword:{keyword}"
    for ext in FILE_PATTERN.findall(message):
        if ext.lower() in CODE_EXTENSIONS:
            return True, f"file_extension:{ext.lower()}"
    return False, "general_chat"

def call_model(url: str, api_key: str | None, payload: dict[str, Any]) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

@app.post("/chat")
def chat() -> Any:
    body = request.get_json(silent=True) or {}
    message = (body.get("message") or "").strip()
    
    if not message:
        return jsonify({"error": "message required"}), 400
    
    is_code, reason = looks_like_code_task(message)
    
    # Route configuration
    if is_code:
        # Code issues: Codex primary, Kimi auxiliary
        primary_model = "codex"
        auxiliary_model = "kimi"
        endpoints = [
            (os.getenv("CODEX_API_URL"), os.getenv("CODEX_API_KEY")),
            (os.getenv("KIMI_API_URL"), os.getenv("KIMI_API_KEY"))
        ]
    else:
        # General chat: MiniMax primary, Kimi auxiliary
        primary_model = "minimax"
        auxiliary_model = "kimi"
        endpoints = [
            (os.getenv("MINIMAX_API_URL"), os.getenv("MINIMAX_API_KEY")),
            (os.getenv("KIMI_API_URL"), os.getenv("KIMI_API_KEY"))
        ]
    
    # Call primary model
    results = {"primary": None, "auxiliary": None, "route_reason": reason}
    
    for idx, (url, key) in enumerate(endpoints):
        if not url:
            continue
        try:
            model_name = primary_model if idx == 0 else auxiliary_model
            response = call_model(url, key, {"message": message, "context": body.get("context")})
            if idx == 0:
                results["primary"] = {"model": model_name, "response": response}
            else:
                results["auxiliary"] = {"model": model_name, "response": response}
        except Exception as e:
            if idx == 0:
                results["primary_error"] = str(e)
            else:
                results["auxiliary_error"] = str(e)
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
