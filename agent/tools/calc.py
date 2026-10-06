"""第二个工具，用来说明注册表：加它不用改主循环。只做四则运算。"""

import ast
import operator

from agent.registry import tool

_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
        return _BIN_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
        return _UNARY_OPS[type(node.op)](_eval(node.operand))
    raise ValueError("只支持数字和 + - * / 以及括号")


@tool(
    name="calculate",
    description="计算四则运算。当用户要求计算一个算式时使用。",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "只含数字和 + - * / 括号的算式，例如 12*(3+4)",
            }
        },
        "required": ["expression"],
    },
)
def calculate(expression):
    tree = ast.parse(expression, mode="eval")
    value = _eval(tree)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)
