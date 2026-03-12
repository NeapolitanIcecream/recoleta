---
source: arxiv
url: http://arxiv.org/abs/2603.01548v1
published_at: '2026-03-02T07:21:15'
authors:
- Neeraj Bholani
topics:
- llm-agents
- tool-routing
- fault-tolerance
- graph-search
- workflow-orchestration
relevance_score: 0.08
run_id: materialize-outputs
---

# Graph-Based Self-Healing Tool Routing for Cost-Efficient LLM Agents

## Summary
本文提出一种面向工具型 LLM Agent 的**自愈式图路由器**：把大多数控制流决策从“让 LLM 每步思考”改成“在工具图上做最短路重算”。其目标是在保持正确性的同时，大幅降低 LLM 调用成本，并避免静态工作流在复合故障下的静默失败。

## Problem
- 现有工具型 Agent 往往在两端摇摆：**每个决策都交给 LLM**，正确但昂贵且延迟高；或用**预编码工作流图**，便宜但遇到多工具同时故障时很脆弱。
- 静态状态机要覆盖复合故障会出现**组合爆炸**：文中指出，对有 N 个工具、每个 K 种故障模式的系统，需覆盖约 **K^N** 个组合，否则容易出现**silent failure**。
- 这很重要，因为生产环境中的 Agent 常依赖支付、通知、预订、审核等外部工具；一旦故障恢复机制不稳，就会带来错误执行、成本上升与可观测性缺失。

## Approach
- 核心机制很简单：把工具和备选路径表示成**带权图**，把“该走哪条工具链”视为**最便宜可行路径搜索**，而不是开放式推理。
- 系统先运行**并行健康监控器**（如意图、风险、工具健康、进度等），每个监控器输出一个优先级分数；最高分信号决定当前系统最该关注什么。
- 路由层使用**Dijkstra 最短路**：正常时选择成本最低的主路径；如果某工具在执行中失败，就把与该工具相连的边权重设为**无穷大**，然后**重新跑一次 Dijkstra** 自动绕行到备份路径。
- 只有当图中**不存在任何可行路径**时，才调用 LLM 进行“目标降级/升级”推理，例如“退款做不了时该如何处理”。
- 作者还提出了面向生产的扩展设想：用实时遥测组合边权（成本、延迟、可靠性、限流、可用性），并结合 circuit breaker；但文中明确说明这部分是**架构建议，未被实验验证**。

## Results
- 在 **19 个场景、3 种图拓扑**（线性流水线、依赖 DAG、并行 fan-out）上，Self-Healing Router 达到 **19/19 正确**，与 **ReAct 的 19/19** 持平，但控制面 **LLM reasoning 调用从 123 次降到 9 次，减少 93%**。
- 相比之下，精心设计的静态工作流基线 **LangGraph** 为 **16/19 正确**，出现 **3 次 silent failure**；Self-Healing Router 的 silent failure 为 **0**。
- 聚合结果表（19 场景总计）：Self-Healing Router **Tools=66, Recovery=13, Silent Fail=0**；ReAct **Tools=93, Recovery=0**；LangGraph **Tools=87, Recovery=24, Silent Fail=3**。
- 客服域（7 场景）中，S6“双通知都挂”和 S7“三重故障”下，静态工作流出现 **Yes silent fail**；而 Self-Healing Router 在这些场景中通过 reroute 或 LLM 升级保持正确。该域内示例还显示 SH 在 S1/S2/S5 中 **0 次 LLM**，而 ReAct 分别需 **4/5/5 次**。
- 旅行预订域（6 场景）中，Self-Healing Router 处理级联重路由：如 T2/T3/T6 分别用 **0 次 LLM** 完成恢复，而 ReAct 需 **6/7/8 次**；T5 在“住宿+租车都不可用”时用 **1 次 LLM** 做目标降级。
- 论文声称恢复复杂度对同时故障数 **K 不敏感**：Self-Healing Router 在单故障和 K 个同时故障下都为 **O((V+E) log V)**，而 ReAct/Agent SDKs 近似随故障数线性增加，静态工作流则在未编码复合故障时失效。需要注意，实验验证的是**控制流与调用次数**，不是基于真实工具输出的端到端语义鲁棒性。

## Link
- [http://arxiv.org/abs/2603.01548v1](http://arxiv.org/abs/2603.01548v1)
