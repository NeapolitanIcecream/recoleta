---
source: hn
url: https://maggieappleton.com/zero-alignment
published_at: '2026-04-14T23:52:32'
authors:
- facundo_olano
topics:
- multi-agent-software-engineering
- code-intelligence
- collaborative-ai
- developer-tools
- human-ai-interaction
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# One Developer, Two Dozen Agents, Zero Alignment

## Summary
## 摘要
Ace 是 GitHub Next 的一个多人编程研究原型，提供共享的智能体、聊天、规划和云工作区。该演讲认为，在由智能体驱动的软件工作中，主要瓶颈是团队对齐，而不是代码生成速度。

## 问题
- 当前的编程智能体是按单用户工具来构建的，但软件团队需要共享的规划、上下文和协作。
- 代码生成更快后，瓶颈会转向决定要构建什么、避免重复工作，以及在代码进入 pull request 之前让团队成员保持一致。
- 现有工具，如 PR、issue 和 Slack，难以很好处理重度依赖智能体的开发在速度、规模和共享上下文上的需求。

## 方法
- Ace 让人和编程智能体进入同一个实时会话，聊天、提示历史、摘要和共享上下文对该会话中的所有人都可见。
- 每个会话都运行在云端 microVM 上，拥有自己的 git branch、terminal、dev server、preview、commits 和 diffs，因此多个人和多个智能体可以在同一任务上工作，而不必承受本地配置带来的阻碍。
- 团队成员可以加入一个会话，查看完整的智能体对话，运行命令，查看相同的预览，一起编辑代码，并共同向智能体发出提示。
- 对于更大的任务，团队可以先在工作区内共同编辑计划，再让智能体实现它，把对齐提前到工作流更早的阶段。
- Ace 还加入了仪表盘摘要，如未完成工作、队友活动和最近的代码仓库变更，帮助用户在许多并行的智能体驱动任务中保持清楚的状态感知。

## 结果
- 摘录中没有提供正式的基准结果、数据集评估或受控的定量比较。
- 最明确的具体说法是产品层面的：Ace 支持一名开发者在共享的多人工作区中与“two dozen agents”协作。
- 该原型据称正进入技术预览阶段，并计划让数千人参与用户测试。
- 声称的用户可见效果包括共享云端执行、多人提示、协作式计划编辑、实时预览、自动提交、创建 GitHub PR，以及在一名用户断开连接后仍会持续的会话。

## Problem

## Approach

## Results

## Link
- [https://maggieappleton.com/zero-alignment](https://maggieappleton.com/zero-alignment)
