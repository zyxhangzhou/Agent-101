"""可选的真实模型。练习循环时用 --mock，不必先准备 key。"""

import os


def openai_complete(messages, schemas):
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("未设置 OPENAI_API_KEY。先用 --mock 把循环跑通。")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("实时模式需要安装 openai：pip install openai") from exc

    client = OpenAI()
    response = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        messages=messages,
        tools=schemas,
    )
    return response.choices[0].message
