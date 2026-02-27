"""Minimal routing strategy for Discord multi-model orchestration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RouteDecision:
    target: str
    reason: str


def route_request(text: str) -> RouteDecision:
    normalized = text.lower().strip()

    code_words = ["code", "bug", "stacktrace", "refactor", "python", "typescript"]
    cn_words = ["润色", "总结", "中文", "翻译", "改写"]
    creative_words = ["创意", "营销", "脑暴", "slogan", "campaign"]

    if any(word in normalized for word in code_words):
        return RouteDecision(target="codex", reason="matched code/debug keywords")

    if any(word in normalized for word in cn_words):
        return RouteDecision(target="kimi", reason="matched chinese polishing/summarization keywords")

    if any(word in normalized for word in creative_words):
        return RouteDecision(target="minimax", reason="matched creative/marketing keywords")

    return RouteDecision(target="ensemble", reason="no strong intent; use multi-model aggregation")


if __name__ == "__main__":
    examples = [
        "please refactor this python code",
        "帮我把这段话润色成更自然中文",
        "给我一个活动slogan",
        "这个问题你怎么看",
    ]
    for text in examples:
        decision = route_request(text)
        print(f"{text} -> {decision.target} ({decision.reason})")
