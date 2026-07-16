---
kind: trend
trend_doc_id: 1345
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
topics:
- coding agents
- agent evaluation
- harness repair
- agent memory
- repository context
- software engineering
run_id: materialize-outputs
aliases:
- recoleta-trend-1345
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/harness-repair
- topic/agent-memory
- topic/repository-context
- topic/software-engineering
language_code: zh-CN
---

# 完整运行循环定义代理式代码评估

## 概览
当天最强的信号是面向代码代理的操作性评估。论文测试反馈轮次、harness 修复、有状态记忆，以及在接近部署条件下的仓库知识。实际问题是：当轨迹、UI 测试、提交记录或重复任务里出现证据后，代理是否会变得更好。

## 研究发现

### 闭环代码代理评估
Asuka-Bench 在初始请求含糊、且有多轮用户反馈的条件下评估网页应用代理。这个基准隐藏完整产品需求，测试浏览器渲染后的行为，并把直接的失败反馈带入后续轮次。报告中的差异很大：三轮之后，按权重计算的任务通过率在 13 种模型-运行时配置之间介于 51.8% 到 90.1%。

ADK Arena 把 Agent Development Kits（ADKs）当作可测量的工程选择。一个编码代理在隔离的 Docker 环境里为 51 个 Python kit 构建基准代理。生成在 57% 的运行中成功，成本在不同 kit 之间相差 5.6 倍。单项基准中最好的代理达到 80% 的任务解决率，中位 kit 达到 32%。

#### 资料来源
- [Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement](../Inbox/2026-06-04--asuka-bench-benchmarking-code-agents-on-underspecified-user-intent-and-multi-round-refinement.md): Summary covers Asuka-Bench task design, feedback loop, dataset size, and reported pass-rate spread.
- [ADK Arena: Evaluating Agent Development Kits via LLM-as-a-Developer](../Inbox/2026-06-04--adk-arena-evaluating-agent-development-kits-via-llm-as-a-developer.md): Summary covers ADK Arena methodology, 51 kits, generation success, cost range, and task-resolution results.

### 从失败轨迹修复 harness
两篇论文把代理 harness 变成了可测量修复的目标。Retrospective Harness Optimization 会选择过去的高难任务，重新运行这些任务，让代理诊断自己的 rollouts，并通过自我偏好选择一个 harness 更新。在 SWE-Bench Pro 上，它把保留集通过率从 0.59 提高到 0.78，且不需要外部评分。

HarnessFix 给修复过程更细的依据。它把失败轨迹和 harness 代码转成步骤级记录，把失败关联到执行、工具、上下文、生命周期、可观测性、验证或治理层，并应用范围受限的补丁。论文报告，在 SWE-Bench Verified、Terminal-Bench 2.0 Verified、GAIA 和 AppWorld 上，相比初始 harness，保留集性能提升了 15.2% 到 50.0%。

#### 资料来源
- [Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts](../Inbox/2026-06-04--retrospective-harness-optimization-improving-llm-agents-via-self-preference-over-trajectory-rollouts.md): Summary describes RHO's trajectory selection, self-validation, self-preference, and benchmark gains.
- [From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws](../Inbox/2026-06-04--from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws.md): Summary describes HarnessFix trace representation, harness-layer diagnosis, scoped repairs, and reported gains.

### 记忆与仓库上下文
记忆工作的评价标准已经转向下游任务效果，而不是一条笔记看起来是否有用。MemOp 只有在记忆让所有测量指标不变或更好，并且至少改善一项时才接受该记忆。它报告单轮任务中最高 5.25 个百分点的成功率提升，以及至少 9.79% 的计算成本下降。

CL-Bench 给出一个提醒：专门的记忆系统并不会自动超过全上下文的 in-context learning。覆盖六个领域时，使用 Claude Sonnet 4.6 的全上下文 in-context learning 在总体结果上领先，而 Mem0 和 ACE 在归一化奖励和增益上落后。

另一条路线是仓库适配。Code2LoRA 根据代码库嵌入生成仓库特定的低秩适配器，并用提交差异更新演化模式。在 RepoPeftBench 上，静态版本的跨仓库 exact match 达到 63.8%，演化版本在持续演化的仓库上达到 60.3% 的跨仓库 exact match。

#### 资料来源
- [Enhancing Software Engineering Through Closed-Loop Memory Optimization](../Inbox/2026-06-04--enhancing-software-engineering-through-closed-loop-memory-optimization.md): Summary covers MemOp's utility test, training data, downstream metrics, success gains, and cost reduction.
- [Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments](../Inbox/2026-06-04--continual-learning-bench-evaluating-frontier-ai-systems-in-real-world-stateful-environments.md): Summary covers CL-Bench design and the finding that full-context in-context learning beats dedicated memory systems on average.
- [Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution](../Inbox/2026-06-04--code2lora-hypernetwork-generated-adapters-for-code-language-models-under-software-evolution.md): Summary covers Code2LoRA's repository-specific adapters, evolution mode, RepoPeftBench, and exact-match results.
