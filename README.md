
# Agent 101

[English](./README.md) · [中文](./README.zh-CN.md)

This repository starts **docs-only**. You write the Agent yourself.

## What this is

A clean place to hand-build a minimal Agent after the series’ first four posts:

| Focus | Idea |
|-------|------|
| **Agent loop** | Task → model → optional tool calls → feed results back → repeat until done |
| **Tool registry** | Register tools once; the loop does not grow an `if name == …` forest |
| **Tool 4-tuple** | `name` · `description` · `parameters` · `func` (the model never runs `func`) |
| **Never-raise execute / Harness** | `execute` always returns a string; errors are results the model can recover from |

## Series links

- **Outline:** [status/2105659995035722170](https://x.com/antiAIvo/status/2105659995035722170)
- **01 — Agent loop:** [status/2106039131264758018](https://x.com/antiAIvo/status/2106039131264758018)
- **02 — Tool registry:** [status/2106731342105125019](https://x.com/antiAIvo/status/2106731342105125019)
- **03 — Tool 4-tuple:** [status/2107049946969161922](https://x.com/antiAIvo/status/2107049946969161922)
- **04 — Execute / Harness:** [status/2107101476137140532](https://x.com/antiAIvo/status/2107101476137140532)
- **Blog:** [nano-ai.tech](https://nano-ai.tech) (Agent series not on the blog yet; LLM-from-scratch is there)

## Learning goals (eps 01–04)

- **01** — See that a “smart Agent” is mostly a **while / for loop**: call the model, run tools if requested, append results, stop when there are no more tool calls (or you hit a step cap).
- **02** — Grow tools through a **registry** (schema + function), so the main loop stays small when you add capabilities.
- **03** — Treat each tool as a **four-part contract**: name (handshake), description (when to call — often the most important), parameters (JSON schema), func (local code only).
- **04** — Put a **Harness** around execution: missing tool, bad args, and runtime failures all become strings. The process must not crash on a tool error; the model needs the message to retry.

## How to work here

1. Read the four episode posts (and the outline) above.
2. **Write the code yourself** in this repo — typing the loop and registry is the point.
3. Prefer a tiny offline **mock model** first so you can debug the loop without an API key.
4. Optionally set `OPENAI_API_KEY` later for a live chat-completions model with tool calling.

No starter package is checked in on purpose. Empty folders are not required.

## Suggested layout (optional, later)

Guidance only — create what you need when you need it:

```text
Agent-101/
├── README.md
├── README.zh-CN.md
├── agent/                 # your loop, registry, execute
│   ├── loop.py
│   ├── registry.py
│   ├── execute.py
│   └── tools/             # small demo tools (e.g. weather mock)
└── main.py                # one entry that runs a sample task
```

Use any language you like; the series demos are Python-shaped.

## Out of scope (this practice slice)

Leave these for later episodes (roughly **05–08** and beyond):

- Real **file / shell / web** tools
- **Persistence** (saving task progress across runs)
- **Multi-agent** setups
- Full reliability stack (retries, human confirmation UIs, RAG, eval harnesses)

Master the loop, registry, tool shape, and never-raise execute first.

## License / vibe

Public practice notes. Follow along, keep it small, and ship understanding before features.
