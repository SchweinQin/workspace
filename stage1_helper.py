#!/usr/bin/env python3
"""Stage-1 helper for OpenClaw manual model switching.

No server or API key required.
It only decides whether a message looks code-related and returns a ready-to-send guidance snippet.
"""

from __future__ import annotations

import json
import re
import sys

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
    "代码",
    "编译",
    "运行失败",
}

FILE_PATTERN = re.compile(r"\b[\w\-./]+(\.[A-Za-z0-9]+)\b")


def detect_code_intent(message: str) -> tuple[bool, str]:
    lower = message.lower()
    
    if "```" in message:
        return True, "contains_code_fence"
    
    for keyword in CODE_KEYWORDS:
        if keyword in lower:
            return True, f"keyword:{keyword}"
    
    for ext in FILE_PATTERN.findall(message):
        if ext.lower() in CODE_EXTENSIONS:
            return True, f"file_extension:{ext.lower()}"
    
    return False, "default_chat"


def build_result(message: str) -> dict[str, str | bool]:
    is_code, reason = detect_code_intent(message)
    
    if is_code:
        return {
            "should_switch_model": True,
            "route_reason": reason,
            "recommended_command": "/model Codex",
            "assistant_prefix": "检测到代码任务，建议先切换到 Codex 再继续。",
        }
    
    return {
        "should_switch_model": False,
        "route_reason": reason,
        "recommended_command": "",
        "assistant_prefix": "当前是普通对话，可继续使用 MiniMax-M2.5。",
    }


def main() -> int:
    message = " ".join(sys.argv[1:]).strip()
    
    if not message:
        print(json.dumps({"error": "usage: python stage1_helper.py <message>"}, ensure_ascii=False))
        return 1
    
    print(json.dumps(build_result(message), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
