"""第 01 step：Agent 的本质是这个while循环。模型决定调不调工具，代码负责执行并塞回结果。"""

from agent.execute import execute_call
from agent.registry import get_schemas

SYSTEM = "你是一个会使用工具的助手。需要事实或计算时调用工具，不要编造工具结果。拿到结果后用简短中文回答。"
MAX_STEPS = 8


def run(task, complete, max_steps=MAX_STEPS):
    """把任务交给 complete（假模型或真实模型），直到它不再要工具。

    complete(messages, schemas) 需返回带 content / tool_calls / model_dump 的消息。
    """
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
            result = execute_call(name, arguments)
            preview = arguments[:80]
            print(f"[第 {step} 步] {name}({preview})")
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )

    print(f"\n[达到 {max_steps} 步上限，已停止]")
    return ""
