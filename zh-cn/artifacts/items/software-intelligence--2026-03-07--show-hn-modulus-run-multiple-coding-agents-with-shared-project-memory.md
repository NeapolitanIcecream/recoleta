---
source: hn
url: https://modulus.so
published_at: '2026-03-07T22:31:18'
authors:
- dasubhajit
topics:
- multi-agent
- coding-agents
- shared-memory
- git-worktrees
- developer-tools
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Modulus – Run multiple coding agents with shared project memory

## Summary
Modulus 是一个面向编程场景的多智能体协作工具，主张让多个 AI 编码代理在并行且隔离的工作区中共享项目记忆完成开发任务。其核心价值在于减少上下文复制、避免代码冲突，并把多代理产出的变更集中审查。

## Problem
- 传统单代理或多窗口式 AI 编程流程难以并行处理多个任务，如同时修 bug 和开发新功能。
- 多个代理若直接操作同一代码库，容易产生冲突、上下文不一致和等待成本。
- 现有工具常需要手动复制 README、API schema 或近期改动给代理，造成高摩擦和信息遗漏。

## Approach
- 使用**多个 AI coding agents 并行运行**，让不同代理同时处理不同开发任务。
- 通过**shared project memory** 让代理自动获取 API schemas、依赖关系以及跨仓库的近期改动，无需手动粘贴上下文。
- 为每个代理分配**独立隔离工作区**，底层使用 git worktrees 来避免相互覆盖和代码冲突。
- 提供**统一审查界面**，汇总所有代理的修改，并支持直接创建 pull request。

## Results
- 文本声称可实现**并行执行多个编码任务**，例如“修复 bug 的同时开发功能”，但**未提供定量基准或实验指标**。
- 文本明确宣称每个代理拥有**独立 workspace**，基于 **git worktrees** 实现“no conflicts, no waiting”，但**没有给出冲突率、吞吐量或耗时下降数据**。
- 文本声称代理可自动共享**API schemas、dependencies、recent changes across all repositories**，并实现“**Zero copy-pasting**”，但**没有给出人工操作减少比例等数字**。
- 文本声称可在**一个地方审查所有代理改动并直接创建 PR**，但**没有提供用户研究、采用率或开发效率提升数据**。

## Link
- [https://modulus.so](https://modulus.so)
