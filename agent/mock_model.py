"""离线假模型：不推理，只按关键词发出工具调用，用来把循环跑通。"""

import json
import re


class _Function:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class _ToolCall:
    def __init__(self, call_id, name, arguments):
        self.id = call_id
        self.type = "function"
        self.function = _Function(name, arguments)


class AssistantMessage:
    """形状对齐 OpenAI 的 message：循环只依赖 content、tool_calls、model_dump。"""

    def __init__(self, content=None, tool_calls=None):
        self.role = "assistant"
        self.content = content
        self.tool_calls = tool_calls

    def model_dump(self, exclude_none=True):
        data = {
            "role": "assistant",
            "content": self.content,
            "tool_calls": None,
        }
        if self.tool_calls:
            data["tool_calls"] = [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
                for call in self.tool_calls
            ]
        if exclude_none:
            return {key: value for key, value in data.items() if value is not None}
        return data


def make_tool_call(name, args, call_id="call_test"):
    payload = json.dumps(args, ensure_ascii=False)
    return AssistantMessage(tool_calls=[_ToolCall(call_id, name, payload)])


def make_text(content):
    return AssistantMessage(content=content)


class MockModel:
    def __init__(self):
        self._n = 0

    def __call__(self, messages, schemas):
        task = next(item["content"] for item in messages if item["role"] == "user")
        tool_msgs = [item for item in messages if item["role"] == "tool"]
        if tool_msgs:
            return make_text(_final_answer(task, tool_msgs[-1]["content"]))
        self._n += 1
        if _wants_weather(task):
            return make_tool_call(
                "get_weather", {"city": _city(task)}, call_id=f"call_{self._n}"
            )
        if _wants_math(task):
            return make_tool_call(
                "calculate",
                {"expression": _expression(task)},
                call_id=f"call_{self._n}",
            )
        return make_text("我目前只会查天气和做四则运算。")


def _wants_weather(text):
    return any(word in text for word in ("天气", "气温", "下雨", "外套", "穿什么"))


def _wants_math(text):
    return bool(re.search(r"\d", text)) and any(op in text for op in "+-*/×÷")


def _city(text):
    for name in ("北京", "上海", "广州", "深圳", "杭州", "成都", "新加坡", "Singapore"):
        if name in text:
            return name
    return "北京"


def _expression(text):
    matched = re.search(r"[0-9][0-9\.\+\-\*/\(\)\s]*[0-9\)]", text)
    if not matched:
        return text
    return re.sub(r"\s+", "", matched.group(0))


def _final_answer(task, tool_result):
    if tool_result.startswith("Error:"):
        return f"工具没有成功：{tool_result}"
    if _wants_math(task):
        return f"计算结果是 {tool_result}。"
    # 假天气固定是晴、25度，示例问句因此回答不用外套。
    if "外套" in task or "穿" in task:
        return f"不用穿外套。{tool_result}。"
    return tool_result
