---
source: hn
url: https://modulus.so
published_at: '2026-03-07T22:31:18'
authors:
- dasubhajit
topics:
- multi-agent-coding
- shared-memory
- git-worktrees
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: Modulus – Run multiple coding agents with shared project memory

## Summary
Modulus 是一个面向软件开发的多智能体编程工具：它让多个 AI 编码代理并行工作，同时共享项目级记忆并使用隔离工作区。核心卖点是减少上下文复制、避免代码冲突，并把多代理产出的变更集中审阅。

## Problem
- 现有 AI 编码助手通常一次只支持单代理或单任务，难以并行处理修 bug、做功能开发等多项工作。
- 多个代理同时改同一项目时，容易出现上下文不同步、代码冲突、重复拷贝 README/API 信息等低效问题。
- 这很重要，因为团队希望把 AI 从“聊天式辅助”提升为可并行协作的开发劳动力，但前提是要解决共享上下文与工程隔离。

## Approach
- 使用**多个 AI agents 并行运行**，让不同代理同时处理不同开发任务，例如一边修 bug、一边开发新功能。
- 通过**shared project memory** 让代理自动获取 API schema、依赖关系、最近改动以及跨仓库上下文，尽量减少人工复制粘贴。
- 给每个代理分配**独立隔离工作区**，基于 git worktrees 工作，从机制上降低文件冲突和相互阻塞。
- 将所有代理产生的代码变更汇总到一个地方审查，并可直接创建 pull request。

## Results
- 文本**没有提供定量实验结果**，没有给出速度、成功率、代码质量或与基线工具的数值比较。
- 最强的具体产品声明是：可让**多个 AI coding agents 并行工作**，并宣称实现“**without conflicts**”。
- 另一个具体声明是：代理可共享项目记忆，自动了解“**API schemas, dependencies, and recent changes across all repositories**”，从而实现“**Zero copy-pasting**”。
- 系统还宣称每个代理使用**git worktrees** 的独立工作区，以支持并发开发并避免等待。
- 支持在一个界面中**review all changes from all agents**，并**directly create pull requests**。

## Link
- [https://modulus.so](https://modulus.so)
