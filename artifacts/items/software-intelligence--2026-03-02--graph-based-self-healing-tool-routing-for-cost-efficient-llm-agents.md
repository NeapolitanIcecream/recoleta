---
source: arxiv
url: http://arxiv.org/abs/2603.01548v1
published_at: '2026-03-02T07:21:15'
authors:
- Neeraj Bholani
topics:
- llm-agents
- tool-routing
- graph-orchestration
- fault-tolerance
- cost-efficiency
relevance_score: 0.92
run_id: materialize-outputs
---

# Graph-Based Self-Healing Tool Routing for Cost-Efficient LLM Agents

## Summary
本文提出 Self-Healing Router，用图路由替代大多数 LLM 控制流决策，在工具故障时自动重算路径，从而降低成本并提升可观测性。核心主张是：常见代理决策更像“找可用且便宜的路径”，而不是每一步都需要语言推理。

## Problem
- 现有工具型 LLM 代理在**可靠性与成本**之间两难：像 ReAct 这类方法把每次决策都交给 LLM，正确但昂贵且延迟高。
- 纯工作流/状态机方案虽然便宜，但对**复合型工具故障**很脆弱；为所有同时故障组合预编码分支会出现组合爆炸，实际系统会遗漏并产生**静默失败**。
- 这很重要，因为生产代理会频繁遇到 API 超时、限流、服务宕机与风险中断；若控制平面既贵又不稳定，就难以支撑大规模自动化软件执行。

## Approach
- 用**并行健康监控器**替代 LLM 做常规“注意力分配”：意图分类、风险检测、工具健康检查等模块并行运行，各自产生优先级分数，最高分信号决定当前系统该关注什么。
- 用**带成本权重的工具图**表示可执行路径：工具是节点、依赖/切换关系是边，Dijkstra 算法寻找当前最便宜且可用的路径。
- 当某工具执行中失败时，将其相关边权重设为**无穷大**，然后从当前位置重新运行 Dijkstra；如果存在备选路径，就自动绕行，**无需调用 LLM**。
- 只有当图中**不存在任何可行路径**时，才调用 LLM 做“目标降级或升级处理”，例如从“退款”降级为“升级人工处理”。
- 论文还提出了生产化扩展思路：将实时延迟、可靠性、限流、可用性组合成动态边权，并结合 circuit breaker；但作者明确说明这些是**架构建议，未在实验中验证**。

## Results
- 在 **19 个场景、3 种图拓扑**（线性流水线、依赖 DAG、并行 fan-out）上，Self-Healing Router 达到 **19/19 正确性**，与 **ReAct 的 19/19** 持平，高于静态工作流基线 **16/19**。
- 控制平面 LLM 调用数从 **ReAct 的 123 次**降到 **9 次**，论文声称是 **93% 减少**；同时工具调用总数为 **66**，低于 ReAct 的 **93**，也低于 LangGraph 基线的 **87**。
- 共发生 **13 次恢复事件**由图重路由直接处理，**0 次需要 LLM 参与恢复**；作者称恢复复杂度对同时失败数量 **K 不敏感**，仍是一次 Dijkstra 重算。
- 相比“well-engineered” LangGraph 基线，Self-Healing Router 将**静默失败从 3 次降为 0 次**；基线在 19 个场景中有 **3/19** 个复合故障场景出现静默失败。
- 客服域中，Self-Healing Router 在 **S6/S7** 这类双/三重故障场景需要 **2 次 LLM 调用**用于无路可走后的升级处理，而 ReAct 分别需要 **8/9 次**；旅行域中 **T2/T3/T6** 的级联故障可用 **0 次 LLM** 完成图式恢复。
- 论文也明确限制：这些数字验证的是**控制流属性**（重路由、升级、调用数、可观测性），**不是**真实工具输出语义正确性或 malformed response 条件下的端到端鲁棒性。

## Link
- [http://arxiv.org/abs/2603.01548v1](http://arxiv.org/abs/2603.01548v1)
