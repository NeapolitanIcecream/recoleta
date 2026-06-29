---
source: arxiv
url: https://arxiv.org/abs/2606.10106v1
published_at: '2026-06-08T19:35:37'
authors:
- Sanderson Oliveira de Macedo
topics:
- agent-harnesses
- coding-agents
- software-engineering-ai
- agent-control
- context-management
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# What makes a harness a harness: necessary and sufficient conditions for an agent harness

## Summary
## 摘要
这篇论文把 agent harness 定义为运行时层，它包裹一个或多个语言模型，并通过循环、工具、上下文管理和控制，让它们在外部环境中工作。它给出的是编码代理系统的归类测试，而不是新的代理或基准。

## 问题
- agent harness 这个词被用来指产品、评测脚手架、SDK、IDE 插件和编排器，这让系统比较变得不清楚。
- 这种区分很重要，因为编码代理会修改代码仓库并运行命令；只看提示词，无法验证代理声称的成功是否和仓库状态一致。
- 这篇论文要找的是一个可作为参照的定义，能够稳定地把具体系统纳入或排除。

## 方法
- 论文采用对研究论文、官方文档、术语表和工程报告的概念分析。
- 它追溯这个术语的来源，从马具到软件测试脚手架、机器学习评测脚手架，再到运行时 agent harness。
- 它定义了 4 个必须满足的运行时条件：agent 循环、能够改变环境的工具接口、面向任务的上下文管理，以及不依赖模型服从性的控制机制。
- 它把这些条件转成 T1-T4 测试，然后用它们检查 agent framework、agent SDK、IDE 插件、eval harness 和 orchestrator 之间的边界。
- 它把这个测试应用到 6 个系统：Claude Code、Codex CLI、Aider、Cline、OpenHands 和 SWE-agent。

## 结果
- 论文提出了一个包含 4 个条件的必要且充分定义：循环、工具、上下文管理和控制。
- 它把这个纳入测试应用到 6 个真实的编码代理 harness，并报告分类一致。
- 它把这个概念与 5 类相邻类别区分开来：agent framework、agent SDK、IDE 插件、eval harness 和 orchestrator。
- 它给出 3 个条件的具体门槛：T2 要求能够改变环境，T3 要求选择面向任务的上下文，T4 要求控制不依赖模型配合。
- 论文没有报告基准准确率、通过率、成本或延迟结果；贡献是一个共享定义和判定测试，而不是测得的代理性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10106v1](https://arxiv.org/abs/2606.10106v1)
