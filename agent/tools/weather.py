"""第 03 期示例：查天气。模型只提出调用，函数在本地跑。"""

from agent.registry import tool


@tool(
    name="get_weather",
    description="查询指定城市的当前天气。当用户问天气、气温、下雨、穿什么衣服时使用。",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称，例如：北京、上海、Singapore",
            }
        },
        "required": ["city"],
    },
)
def get_weather(city):
    # 练习用的固定天气，不访问网络。
    return f"{city}今天晴，25度"
