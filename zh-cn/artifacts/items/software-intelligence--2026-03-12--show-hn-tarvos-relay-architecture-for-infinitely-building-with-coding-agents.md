---
source: hn
url: https://github.com/Photon48/tarvos/tree/main
published_at: '2026-03-12T23:55:30'
authors:
- Photon48
topics:
- coding-agents
- multi-agent-orchestration
- context-management
- software-automation
- developer-tools
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Tarvos – Relay Architecture for infinitely building with coding agents

## Summary
Tarvos 提出一种面向 AI 编程代理的“接力式”执行架构，通过不断切换到全新代理来避免长上下文导致的性能退化。它将软件开发拆成阶段，并用最小交接信息与外部编排器维持连续性，从而支持更长程的自动化编码流程。

## Problem
- 现有 AI 编程工具通常依赖单个代理从头执行到尾，但随着上下文窗口被历史内容占满，模型准确率会显著下降。
- 在多阶段软件开发中，后期大量 token 都花在“记住之前做了什么”上，而不是继续高质量实现新任务，这限制了真正的自主开发。
- 这很重要，因为复杂软件任务往往跨多个阶段、持续较长时间，单会话代理难以稳定完成端到端交付。

## Approach
- 核心方法是“Relay Architecture”：不用一个代理做完整个任务，而是让多个全新代理按阶段接力，每次都从磁盘读取完整主计划，再基于极简交接继续工作。
- 它把共享状态拆成 4 个部件：**Master Plan**（持久化阶段计划）、**Baton**（最多 40 行的 `progress.md` 交接）、**Signals**（`PHASE_COMPLETE`/`PHASE_IN_PROGRESS`/`ALL_PHASES_COMPLETE`）、**Context Budget**（实时 token 预算与阈值切换）。
- 编排器不理解代码语义，只监听信号、监控 token 消耗，并在超预算时停止当前代理、生成新代理继续执行。
- Tarvos 作为该架构的参考实现，提供 git worktree 隔离、后台运行、TUI 监控、自动恢复、以及 accept/reject/forget 生命周期管理。

## Results
- 文中给出的示例任务“payments”被拆成 **4 个阶段**，估计约 **2400 行工作量**，最终由 **5 个代理** 接力完成，总耗时 **29 分钟**。
- 各代理 token 使用示例为：Phase 1 **42k tokens / 3m**，Phase 2 **87k / 8m** 后因预算触发交接，Phase 2 延续 **61k / 6m**，Phase 3 **79k / 7m**，Phase 4 **53k / 5m**。
- 文章的核心定性主张是：每个代理都能在“干净上下文”下以“full capacity”运行，避免单代理在长上下文中的退化。
- 文中引用了外部现象依据（Chroma Research 指出输入变长会降低模型准确率），但**没有提供正式基准实验、对照组、成功率统计或与其他 coding agent 系统的量化比较**。
- 因此，当前结果更像是一个有说服力的系统演示与工程实现，而非经过严格论文评测验证的性能突破。

## Link
- [https://github.com/Photon48/tarvos/tree/main](https://github.com/Photon48/tarvos/tree/main)
