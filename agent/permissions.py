"""第 05 期：执行前的权限检查。判断写在代码里，不写在提示词里。"""

import json
import re
from pathlib import Path

# 练习里这两个工具没有副作用，直接放行。没列入这里的工具默认要人确认。
SAFE_TOOLS = {"get_weather", "calculate"}

# 兜底用的，不是完整清单。对应笔记里的误删、读私钥、把命令输出塞给 shell。
_DANGEROUS_COMMAND = re.compile(
    r"\brm\s+-"
    r"|\b(curl|wget)\b[^|\n]*\|\s*(sh|bash|zsh)\b",
    re.IGNORECASE,
)
_SENSITIVE_PATH = re.compile(
    r"(^|[/\\])\.ssh([/\\]|$)"
    r"|id_rsa|id_ed25519"
    r"|(^|[/\\])\.aws[/\\]credentials"
    r"|[/\\]etc[/\\]shadow",
    re.IGNORECASE,
)


def check(name, args):
    """返回 (allow|deny|confirm, 原因)。deny 时调用方不得再问人。"""
    for text in _strings(args):
        if _SENSITIVE_PATH.search(text):
            return "deny", f"敏感路径，直接拒绝：{text}"
        if _DANGEROUS_COMMAND.search(text):
            return "deny", f"危险命令，直接拒绝：{text}"
        if _escapes_workspace(text):
            return "deny", f"路径越界，直接拒绝：{text}"
    if name in SAFE_TOOLS:
        return "allow", ""
    return "confirm", "未列为安全工具，需要确认"


def confirm_in_terminal(name, args):
    """给人看的是这次调用的真实参数。"""
    shown = json.dumps(args, ensure_ascii=False)
    print(f"\n需要确认: {name}({shown})")
    answer = input("允许执行? [y/N] ")
    return answer.strip().lower() == "y"


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def _escapes_workspace(text):
    if not re.search(r"[/\\~]|[A-Za-z]:[/\\]", text):
        return False
    raw = Path(text).expanduser()
    if not raw.is_absolute():
        raw = Path.cwd() / raw
    try:
        resolved = raw.resolve()
        cwd = Path.cwd().resolve()
    except OSError:
        return True
    return resolved != cwd and cwd not in resolved.parents
