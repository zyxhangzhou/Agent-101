"""第 01 step：Agent 的本质是这个while循环。模型决定调不调工具，代码负责执行并塞回结果。"""

import json

from agent.execute import execute, parse_arguments
from agent.permissions import check, confirm_in_terminal
from agent.registry import get_schemas

SYSTEM = "你是一个会使用工具的助手。需要事实或计算时调用工具，不要编造工具结果。拿到结果后用简短中文回答。"
MAX_STEPS = 8


def run(task, complete, max_steps=MAX_STEPS, confirm=None):
    """把任务交给 complete（假模型或真实模型），直到它不再要工具。

    complete(messages, schemas) 需返回带 content / tool_calls / model_dump 的消息。
    confirm(name, args) 在需要人工确认时调用；不传就在终端问 y/n。
    """
    ask = confirm_in_terminal if confirm is None else confirm
    import agent.tools  # noqa: F401  导入时完成工具注册

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": task},
    ]
    for step in range(1, max_steps + 1):
        msg = complete(messages, get_schemas())
        messages.append(msg.model_dump(exclude_none=True))

        tool_calls = getattr(msg, "tool_calls", None)
        if not tool_calls:
            text = msg.content or ""
            print(f"\n[完成，共 {step} 步]\n{text}")
            return text

        for call in tool_calls:
            name = call.function.name
            arguments = call.function.arguments or ""
            result = _run_tool(name, arguments, ask)
            preview = arguments[:80]
            print(f"[第 {step} 步] {name}({preview})")
            if result.startswith("[权限拒绝]"):
                print(result)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )

    print(f"\n[达到 {max_steps} 步上限，已停止]")
    return ""


def _run_tool(name, arguments, ask):
    """先检查权限，通过了才执行。拒绝也是一段文字，循环继续。"""
    args, error = parse_arguments(arguments)
    if error:
        return error
    decision, reason = check(name, args)
    if decision == "deny":
        return f"[权限拒绝] {reason}"
    if decision == "confirm" and not ask(name, args):
        shown = json.dumps(args, ensure_ascii=False)
        return f"[权限拒绝] 未获允许执行 {name}({shown})"
    return execute(name, args)
