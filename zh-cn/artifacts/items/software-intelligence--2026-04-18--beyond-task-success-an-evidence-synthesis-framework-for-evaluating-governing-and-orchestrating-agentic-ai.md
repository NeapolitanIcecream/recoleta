---
source: arxiv
url: http://arxiv.org/abs/2604.19818v1
published_at: '2026-04-18T20:28:26'
authors:
- Christopher Koch
- Joshua Andreas Wellbrock
topics:
- agentic-ai
- ai-governance
- runtime-assurance
- multi-agent-systems
- tool-safety
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Task Success: An Evidence-Synthesis Framework for Evaluating, Governing, and Orchestrating Agentic AI

## Summary
## 摘要
这篇论文认为，可信的 agentic AI 需要完整的控制栈，不能只看任务成功基准。论文综合了 24 个来源，提出一个把评估、治理、编排和保障连接起来的框架，用来弥合其所说的治理到行动闭合缺口。

## 问题
- Agentic AI 系统会在多步骤工作流中执行操作、使用工具、保留状态，并产生外部副作用，所以最终任务是否完成，不能说明系统在执行过程中是否表现得可接受。
- 当前研究分散在几条独立路线中：基准测试衡量结果，标准定义义务，编排研究分析控制点，保障研究分析轨迹和证明。论文指出，这些路线都没有说明策略在何处约束具体行动，也没有说明后续如何证明合规。
- 这很重要，因为智能体能力正在快速上升。论文引用 Stanford HAI 的 2026 AI Index 摘要：真实世界任务上的 Terminal-Bench 成功率从 2025 年的 20% 升至 2026 年的 77.3%，而衡量和管理仍然落后。

## 方法
- 这篇论文是对 24 个手工编码来源做的有限证据综合：包括 15 篇研究论文和 9 个标准或框架类材料，来源涵盖 arXiv、ACL Anthology、PMLR、NIST、ISO 和 Stanford HAI。
- 论文按八个维度对每个来源编码，包括分析单元、控制位置、证据类型、失败模式和可执行性类别，然后比较这些研究路线，找出反复出现的不匹配。
- 它最主要的概念产出是 **治理到行动闭合缺口**：评估说明结果是否良好，治理说明什么应当被允许，但两者都没有说明行动时的执行约束发生在何处，也没有说明之后如何加以证明。
- 论文提出一个四层框架：evaluation = 发生了什么，governance = 应该发生什么，orchestration = 执行时此刻可以发生什么，assurance = 之后如何证明这一点。
- 它还提出两个具体构件：ODTA 测试，用 observability、decidability、timeliness 和 attestability 来判断要求应放在运行时的什么位置；以及用于状态变更行动的最小行动证据包（MAEB），适用于工具调用、审批和外部交易等行为。

## 结果
- 这篇论文**没有**报告新的实验结果，也**没有**给出新的基准分数。它是一篇综合论文，并包含一个采购智能体场景的示例分析。
- 最强的实证性结论来自它整合的已有文献：
  - Stanford HAI 2026 AI Index 摘要：Terminal-Bench 成功率从 **20%（2025）** 升至 **77.3%（2026）**。
  - Agentic Benchmark Checklist：基准设计选择会让报告的性能结果在**相对意义上最多变化 100%**。
  - Agent-SafetyBench：在 **16 个智能体**、**349 个环境** 和 **2,000 个测试用例** 中，**没有一个超过 60% 的安全分数**。
  - WebGuard：前沿模型在预测网页动作结果时准确率低于 **60%**，在没有专门防护的情况下，对高风险动作的召回率也低于 **60%**。
  - ToolSafe：在提示注入条件下，步骤级干预平均将有害工具调用减少 **65%**，同时提高了正常任务完成率。
  - ShieldAgent：在其基准上报告了 **90.1% 的召回率**，同时减少了 API 查询次数和推理时间。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19818v1](http://arxiv.org/abs/2604.19818v1)
