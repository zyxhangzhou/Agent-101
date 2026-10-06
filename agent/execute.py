"""第 04 期：Harness。execute 永远返回字符串，永远不抛异常。"""

import json

from agent.registry import TOOLS

MAX_OUTPUT = 8000


def execute(name, args):
    """执行工具。不存在、参数不对、运行失败、成功，四种情况都变成字符串。"""
    if name not in TOOLS:
        names = ", ".join(TOOLS) or "(无)"
        return f"Error: 不存在工具 '{name}', 可用工具: {names}"
    try:
        result = str(TOOLS[name]["func"](**args))
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"
    if len(result) > MAX_OUTPUT:
        result = result[:MAX_OUTPUT] + f"\n... (已截断, 共 {len(result)} 字符)"
    return result


def execute_call(name, arguments):
    """解析模型给出的 arguments JSON，再交给 execute。解析失败也返回字符串。"""
    try:
        args = json.loads(arguments or "{}")
    except json.JSONDecodeError as e:
        return f"Error: JSONDecodeError: {e}"
    if not isinstance(args, dict):
        return "Error: 工具参数必须是 JSON 对象"
    return execute(name, args)
