"""第 02 期：工具注册表。新工具在这里登记，主循环不用改。"""

TOOLS = {}


def tool(name, description, parameters):
    """装饰器：登记一个工具的四元组（第 03 期）。

    name / description / parameters 给模型看；func 只在本地执行。
    """

    def decorator(func):
        TOOLS[name] = {
            "schema": {
                "type": "function",
                "function": {
                    "name": name,
                    "description": description,
                    "parameters": parameters,
                },
            },
            "func": func,
        }
        return func

    return decorator


def get_schemas():
    """返回给模型的工具说明书。里面没有 func。"""
    return [item["schema"] for item in TOOLS.values()]
