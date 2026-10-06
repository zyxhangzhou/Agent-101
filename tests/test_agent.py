import unittest

import agent.tools  # noqa: F401  注册 get_weather / calculate
from agent.execute import MAX_OUTPUT, execute
from agent.loop import run
from agent.mock_model import MockModel, make_text, make_tool_call
from agent.registry import tool


class ExecuteTests(unittest.TestCase):
    def test_unknown_tool_is_a_string(self):
        result = execute("missing_tool", {})
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("missing_tool", result)

    def test_bad_args_are_a_string(self):
        result = execute("get_weather", {})
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("TypeError", result)

    def test_weather_and_calc(self):
        self.assertEqual(execute("get_weather", {"city": "北京"}), "北京今天晴，25度")
        self.assertEqual(execute("calculate", {"expression": "12*(3+4)"}), "84")

    def test_long_output_is_truncated(self):
        @tool(
            name="blob",
            description="返回很长的文本",
            parameters={
                "type": "object",
                "properties": {},
            },
        )
        def blob():
            return "x" * (MAX_OUTPUT + 50)

        result = execute("blob", {})
        self.assertLess(len(result), MAX_OUTPUT + 80)
        self.assertIn("已截断", result)
        self.assertIn(str(MAX_OUTPUT + 50), result)


class LoopTests(unittest.TestCase):
    def test_weather_task(self):
        text = run("北京今天要穿外套吗？", MockModel())
        self.assertIn("不用穿外套", text)
        self.assertIn("北京今天晴，25度", text)

    def test_math_task(self):
        text = run("计算 12*(3+4)", MockModel())
        self.assertIn("84", text)

    def test_tool_error_does_not_crash_the_loop(self):
        def complete(messages, schemas):
            if any(item["role"] == "tool" for item in messages):
                return make_text("工具不存在，改用文字回答。")
            return make_tool_call("no_such_tool", {}, call_id="call_bad")

        text = run("随便问一句", complete, max_steps=3)
        self.assertEqual(text, "工具不存在，改用文字回答。")

    def test_step_cap(self):
        def complete(messages, schemas):
            return make_tool_call("get_weather", {"city": "上海"}, call_id="call_loop")

        text = run("一直查", complete, max_steps=2)
        self.assertEqual(text, "")


if __name__ == "__main__":
    unittest.main()
