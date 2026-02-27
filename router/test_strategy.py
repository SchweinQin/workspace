"""Unit tests for router.strategy module."""

import unittest
from router.strategy import route_request, RouteDecision


class TestRouteStrategy(unittest.TestCase):
    """Test cases for route_request function."""

    def test_code_keywords_route_to_codex(self):
        """Test that code-related keywords route to codex."""
        test_cases = [
            "please refactor this python code",
            "debug this stacktrace",
            "help me fix this bug",
            "write a typescript function",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                decision = route_request(text)
                self.assertEqual(decision.target, "codex")
                self.assertIn("code", decision.reason)

    def test_chinese_keywords_route_to_kimi(self):
        """Test that Chinese processing keywords route to kimi."""
        test_cases = [
            "帮我把这段话润色成更自然中文",
            "总结一下这篇文章",
            "把这段话翻译成中文",
            "帮我改写这个段落",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                decision = route_request(text)
                self.assertEqual(decision.target, "kimi")
                self.assertIn("chinese", decision.reason)

    def test_creative_keywords_route_to_minimax(self):
        """Test that creative/marketing keywords route to minimax."""
        test_cases = [
            "给我一个活动slogan",
            "帮我想个创意方案",
            "脑暴一些营销点子",
            "设计一个campaign",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                decision = route_request(text)
                self.assertEqual(decision.target, "minimax")
                self.assertIn("creative", decision.reason)

    def test_unclear_intent_routes_to_ensemble(self):
        """Test that unclear intent routes to ensemble."""
        test_cases = [
            "这个问题你怎么看",
            "hello there",
            "what's up",
            "帮我看看这个",
        ]
        for text in test_cases:
            with self.subTest(text=text):
                decision = route_request(text)
                self.assertEqual(decision.target, "ensemble")
                # reason contains "multi-model" not "ensemble"
                self.assertIn("multi-model", decision.reason)


if __name__ == "__main__":
    unittest.main()
