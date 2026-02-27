#!/usr/bin/env python3
"""Minimal OpenClaw model router.

Route code-related requests to Codex and general chat to MiniMax.
"""

from __future__ import annotations

import os
import re
from typing import Any

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".cs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".sql",
    ".sh",
    ".yaml",
    ".yml",
    ".json",
}

CODE_KEYWORDS = {
    "报错",
    "stack trace",
    "traceback",
    "review",
    "代码审查",
    "重构",
    "函数",
    "api",
    "sql",
    "bug",
    "exception",
    "debug",
    "测试",
    "fix",
}

FILE_PATTERN = re.compile(r"\b[\w\-./]+(\.[A-Za-z0-9]+)\b")


def looks_like_code_task(message: str) -> tuple[bool, str]:
    msg = message.lower()

    if "```" in message:
        return True, "contains_code_fence"

    for keyword in CODE_KEYWORDS:
        if keyword in msg:
            return True, f"keyword:{keyword}"

    for match in FILE_PATTERN.findall(message):
        ext = match.lower()
        if ext in CODE_EXTENSIONS:
            return True, f"file_extension:{ext}"

    return False, "default_general_chat"


def build_headers(api_key: str | None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def call_model(url: str, api_key: str | None, payload: dict[str, Any], timeout_s: int = 30) -> dict[str, Any]:
    resp = requests.post(url, json=payload, headers=build_headers(api_key), timeout=timeout_s)
    resp.raise_for_status()
    data = resp.json()
    return data if isinstance(data, dict) else {"raw": data}


@app.post("/chat")
def chat() -> Any:
    body = request.get_json(silent=True) or {}
    message = (body.get("message") or "").strip()
    history = body.get("history") or []

    if not message:
        return jsonify({"error": "message is required"}), 400

    minimax_url = os.getenv("MINIMAX_API_URL", "")
    codex_url = os.getenv("CODEX_API_URL", "")
    minimax_key = os.getenv("MINIMAX_API_KEY")
    codex_key = os.getenv("CODEX_API_KEY")

    if not minimax_url or not codex_url:
        return jsonify({"error": "MINIMAX_API_URL and CODEX_API_URL are required"}), 500

    is_code, reason = looks_like_code_task(message)
    primary_model = "codex" if is_code else "minimax"

    payload = {
        "message": message,
        "history": history,
        "metadata": {
            "route_reason": reason,
            "primary_model": primary_model,
        },
    }

    fallback_used = False

    try:
        if primary_model == "codex":
            model_response = call_model(codex_url, codex_key, payload)
            selected_model = "codex"
        else:
            model_response = call_model(minimax_url, minimax_key, payload)
            selected_model = "minimax"
    except Exception as exc:
        if primary_model == "codex":
            fallback_used = True
            fallback_reason = f"codex_failed:{type(exc).__name__}"
            payload["metadata"]["fallback_reason"] = fallback_reason
            model_response = call_model(minimax_url, minimax_key, payload)
            selected_model = "minimax"
            reason = f"{reason}|{fallback_reason}"
        else:
            return jsonify({"error": f"minimax_request_failed:{type(exc).__name__}"}), 502

    return jsonify(
        {
            "model": selected_model,
            "route_reason": reason,
            "fallback_used": fallback_used,
            "response": model_response,
        }
    )


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    app.run(host=host, port=port)
