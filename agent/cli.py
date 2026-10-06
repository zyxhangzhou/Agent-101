"""命令行入口。"""

import argparse

from agent.live import openai_complete
from agent.loop import MAX_STEPS, run
from agent.mock_model import MockModel


def main(argv=None):
    parser = argparse.ArgumentParser(description="最小 Agent：循环 + 注册表 + execute")
    parser.add_argument("task", help="交给 Agent 的一句话任务")
    parser.add_argument("--mock", action="store_true", help="用离线假模型，不访问网络")
    parser.add_argument("--max-steps", type=int, default=MAX_STEPS, help="循环步数上限")
    args = parser.parse_args(argv)
    complete = MockModel() if args.mock else openai_complete
    run(args.task, complete, max_steps=args.max_steps)


if __name__ == "__main__":
    main()
