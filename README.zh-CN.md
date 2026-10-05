
# Agent 101

[English](./README.md) · [中文](./README.zh-CN.md)

本仓库起步时**只有文档**。Agent 代码请你自己写。

## 这是什么

一个干净的练习场，用来亲手实现系列前四期的最小 Agent：

| 焦点 | 要点 |
|------|------|
| **Agent 循环** | 任务 → 模型 →（可选）工具调用 → 把结果塞回 → 直到结束 |
| **工具注册表** | 注册一次即可扩展；主循环不必堆 `if name == …` |
| **工具四元组** | `name` · `description` · `parameters` · `func`（模型从不执行 `func`） |
| **永不抛异常的 execute / Harness** | `execute` 永远返回字符串；错误也是结果，模型才能纠错重试 |

## 系列链接

- **大纲：** [status/2105659995035722170](https://x.com/antiAIvo/status/2105659995035722170)
- **01 — Agent 循环：** [status/2106039131264758018](https://x.com/antiAIvo/status/2106039131264758018)
- **02 — 工具注册表：** [status/2106731342105125019](https://x.com/antiAIvo/status/2106731342105125019)
- **03 — 工具四元组：** [status/2107049946969161922](https://x.com/antiAIvo/status/2107049946969161922)
- **04 — 执行器 / Harness：** [status/2107101476137140532](https://x.com/antiAIvo/status/2107101476137140532)
- **博客：** [nano-ai.tech](https://nano-ai.tech)（Agent 系列正文尚未上博客；从零手写 LLM 相关内容在站内）

## 学习目标（第 01–04 期）

- **01** — 看清「智能 Agent」核心多半是一个 **while / for 循环**：调模型 → 有工具就执行 → 追加结果 → 没有 tool calls（或达到步数上限）就停。
- **02** — 用 **注册表**（schema + 函数）扩展工具，主循环尽量保持短小。
- **03** — 把每个工具当成 **四部分契约**：name（暗号）、description（何时调用——往往最重要）、parameters（JSON schema）、func（只在本地跑）。
- **04** — 在执行外套一层 **Harness**：工具不存在、参数错误、运行失败全部变成字符串。工具出错时进程不能崩；模型需要这条消息才能重试。

## 怎么练

1. 先读上面的大纲与四期推文。
2. **自己动手写代码**——敲一遍循环和注册表，才是练习的意义。
3. 建议先用离线 **mock 模型**，把循环跑通，再接真实 API。
4. 之后可按需设置 `OPENAI_API_KEY`，接带 tool calling 的 chat completions。

仓库故意不放起步包。空目录不是必须的。

## 建议目录（可选，之后再建）

仅作参考——需要时再创建：

```text
Agent-101/
├── README.md
├── README.zh-CN.md
├── agent/                 # 循环、注册表、execute
│   ├── loop.py
│   ├── registry.py
│   ├── execute.py
│   └── tools/             # 小演示工具（如天气 mock）
└── main.py                # 入口：跑一个样例任务
```

语言不限；系列演示偏 Python 形态。

## 本练习切片明确不做

留给更后面的期次（大约 **05–08** 及以后）：

- 真实的 **文件 / shell / 网页** 工具
- **持久化**（跨运行保存任务进度）
- **多 Agent**
- 完整可靠性栈（重试、人工确认 UI、RAG、评测等）

先把循环、注册表、工具形态、永不抛异常的 execute 练扎实。

## 许可 / 氛围

公开练习笔记。跟着写、保持小、先搞懂再堆功能。
