import unittest

from router.strategy import route_request


class TestRouteStrategy(unittest.TestCase):
    def test_code_route(self):
        decision = route_request("Need help debugging this stacktrace")
        self.assertEqual(decision.target, "codex")

    def test_kimi_route(self):
        decision = route_request("请帮我润色这个中文段落")
        self.assertEqual(decision.target, "kimi")

    def test_minimax_route(self):
        decision = route_request("想做一次营销脑暴")
        self.assertEqual(decision.target, "minimax")

    def test_ensemble_route(self):
        decision = route_request("what do you think")
        self.assertEqual(decision.target, "ensemble")


if __name__ == "__main__":
    unittest.main()
