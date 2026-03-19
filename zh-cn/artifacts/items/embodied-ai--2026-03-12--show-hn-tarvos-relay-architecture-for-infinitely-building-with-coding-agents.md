---
source: hn
url: https://github.com/Photon48/tarvos/tree/main
published_at: '2026-03-12T23:55:30'
authors:
- Photon48
topics:
- ai-coding-agents
- multi-agent-orchestration
- context-management
- developer-tools
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Tarvos – Relay Architecture for infinitely building with coding agents

## Summary
Tarvos 提出一种面向 AI 编码代理的“接力式”编排架构，用多个上下文干净的代理接续完成长周期软件开发任务，以减轻长上下文导致的性能退化。它当前以 Claude Code 的参考实现形式提供，核心卖点是把单次会话执行改为分阶段、可恢复、可监控的多代理流水线。

## Problem
- 现有 AI 编码工具通常让单个代理从头执行到尾，随着上下文不断累积，模型准确率会下降，后期大量上下文被用于“记住已完成内容”而不是继续开发。
- 这会限制长任务、分阶段任务和更接近“自主开发”的工作流，尤其在多阶段 PRD 执行时更明显。
- 对用户而言，缺少可靠的交接、恢复、隔离执行与上下文预算控制，会让长时编码代理难以稳定扩展。

## Approach
- 用 **Relay Architecture** 替代单代理长会话：每个新代理都从磁盘重新读取完整主计划（Master Plan），只接收一个极简交接笔记（Baton），然后继续下一段工作。
- 交接笔记是 `progress.md`，被限制在 40 行内，目的是强制最小信息传递，避免把旧上下文膨胀带入下一个代理，重现“上下文腐化”。
- 系统通过三类显式信号 `PHASE_COMPLETE`、`PHASE_IN_PROGRESS`、`ALL_PHASES_COMPLETE` 来驱动编排器；编排器无需理解代码语义，只需监听状态信号并调度下一步。
- 引入 **Context Budget**：实时跟踪 token 使用量，到达预算阈值后自动停止当前代理并生成新的干净代理接力；代理也可在中途自我判断并主动交接。
- Tarvos 作为参考实现，还提供 git worktree 隔离、后台执行、TUI 监控、异常恢复（可由恢复代理从 git 历史重建交接）、以及 accept/reject/forget 生命周期管理。

## Results
- 文中给出的演示案例：一个约 **4 个阶段、约 2400 行工作量** 的支付功能开发计划，由 **5 个代理** 在 **29 分钟** 内完成，并最终达到 `ALL_PHASES_COMPLETE`。
- 各代理示例耗时与 token 使用：Phase 1 **3 分钟 / 42k tokens**；Phase 2 第一次 **8 分钟 / 87k tokens** 后因上下文预算触发干净交接；Phase 2 续跑 **6 分钟 / 61k tokens**；Phase 3 **7 分钟 / 79k tokens**；Phase 4 **5 分钟 / 53k tokens**。
- 关键主张是：每个代理都能在“满容量”下运行，而不是在长上下文后期性能退化；系统将长任务拆为多次新鲜上下文执行，从而覆盖“单个代理无法持续完成的距离”。
- 文中**没有提供正式基准实验**、公开数据集评测、对照方法统计显著性，或与其他 AI 编码代理框架的系统化量化比较。
- 最强的具体证据是工程级产品特性与一次端到端示例运行，而非学术论文式实验结果。

## Link
- [https://github.com/Photon48/tarvos/tree/main](https://github.com/Photon48/tarvos/tree/main)
