---
source: hn
url: https://github.com/bkawa-bot/planet-maiko
published_at: '2026-05-22T23:40:14'
authors:
- bkawa-bot
topics:
- developer-tools
- agent-orchestration
- local-rag
- code-review
- human-ai-interaction
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# I was bored so I turned my dev tools into an alien planet ruled by my dog

## Summary
## 总结
Planet Maiko 是一个本地开发者工作台，把任务、代码审查、代理会话和工具通知汇总到一个桌面工作流里。它针对的是频繁切换上下文和照看代理的负担，不是研究基准。

## 问题
- 开发者在 GitHub、Slack、日历、问题跟踪器、PagerDuty 和 AI 代理分别在不同工具里催办时，很难保持专注。
- 这个项目之所以重要，是因为多代理软件工作会带来协调开销：代理会卡住，成本会升高，人还是要决定下一步做什么。
- 作者想要一个本地工具，能总结工作、建议下一步动作，并把私有工作数据留在笔记本上。

## 方法
- Planet Maiko 在本地运行，需要 Python 3.10+ 和 Node.js 18+，安装通过 `python3 bootstrap.py`，日常使用通过 `maiko up`。
- 它连接 PagerDuty、Linear、Calendar 和 GitHub 等开发者系统，然后把它们的状态合并到一个工作仪表盘里。
- 它包含代理编排、代理聊天界面、应用内 diff 审查、自定义自动化、按成本感知的模型路由、本地 RAG 嵌入和实验性的模型微调。
- 插件模型要求用户只写 1 个 Python 类就能添加新的数据源。
- 它的记忆层会构建本地 RAG 存储，包括从以往 GitHub 历史中提取的指南，这样工具就能在不把数据发送到托管服务的情况下给出与工作相关的建议。

## 结果
- 摘要没有给出任何基准指标、用户研究结果，也没有和 Cursor、GitHub Copilot、Devin 风格代理或问题跟踪器助手做对比。
- 它声称支持 4 个命名集成：PagerDuty、Linear、Calendar 和 GitHub。
- 它声称本地运行，没有遥测、没有托管账户、没有云依赖，也没有付费档位。
- 它声称可以覆盖一天里的工作流，包括早晨规划、PR 审查、代理会话管理、问题更新、任务更新、自动化和通知。
- 最具体的贡献是产品集成：一个免费的开源本地工具，把 RAG 记忆、代理控制、代码审查和开发者系统插件放在一个应用里。

## Problem

## Approach

## Results

## Link
- [https://github.com/bkawa-bot/planet-maiko](https://github.com/bkawa-bot/planet-maiko)
