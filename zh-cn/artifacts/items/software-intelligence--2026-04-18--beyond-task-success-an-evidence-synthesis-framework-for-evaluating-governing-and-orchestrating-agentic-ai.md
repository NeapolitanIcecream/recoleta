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
本文主张，具身式 AI 的信任不能只靠任务成功率基准，而需要一整套控制栈。它综合了 24 篇来源，提出一个把评估、治理、编排和保障连接起来的框架，用来弥合它所说的“治理到行动闭合缺口”。

## 问题
- 具身式 AI 系统会跨多个步骤工作流采取行动、调用工具、保留状态，并产生外部副作用，所以最终任务是否完成，不能说明系统在执行过程中是否行为得当。
- 现有研究分散在不同方向：基准测试衡量结果，标准定义义务，编排研究关注控制点，保障研究关注轨迹和证明。本文认为，这些方向没有说明政策在何处约束具体行动，也没有说明之后如何证明合规。
- 这一点很重要，因为模型能力增长很快。本文引用了 Stanford HAI 的 2026 AI Index 摘要：Terminal-Bench 在真实世界任务上的成功率从 2025 年的 20% 升至 2026 年的 77.3%，而测量和管理仍然落后。

## 方法
- 这篇论文是在 24 篇手工编码来源上的有限证据综合：其中 15 篇是研究论文，9 篇是标准或框架材料，来源包括 arXiv、ACL Anthology、PMLR、NIST、ISO 和 Stanford HAI。
- 它沿着 8 个维度对每个来源编码，包括分析单位、控制位置、证据类型、失败模式和可执行类别，然后比较这些方向，找出反复出现的不匹配。
- 它的主要概念产出是 **治理到行动闭合缺口**：评估说明结果是否良好，治理说明哪些行为应被允许，但两者都没有说明行动时的强制执行发生在哪里，也没有说明之后如何证明。
- 它提出一个四层框架：评估 = 发生了什么，治理 = 应该发生什么，编排 = 在执行时现在可能发生什么，保障 = 之后如何证明这一主张。
- 它还给出两个具体产物：用于判断运行时要求放置位置的 ODTA 测试，依据是可观测性、可判定性、及时性和可证明性；以及用于状态改变动作的最小动作证据包（MAEB），例如工具调用、审批和外部交易。

## 结果
- 这篇论文**没有**报告新的实验结果或新的基准分数。它是一篇综合论文，附带一个采购代理的实例。
- 最强的实证主张来自它整合的文献：
  - Stanford HAI 2026 AI Index 摘要：Terminal-Bench 成功率从 **20%（2025）** 升至 **77.3%（2026）**。
  - Agentic Benchmark Checklist：基准设计选择会让报告性能在相对意义上最多相差 **100%**。
  - Agent-SafetyBench：在 **16 个代理**、**349 个环境** 和 **2,000 个测试用例** 中，没有一个超过 **60%** 的安全分数。
  - WebGuard：前沿模型在预测网页动作结果时准确率低于 **60%**，在没有专门防护时，对高风险动作的召回率也低于 **60%**。
  - ToolSafe：在提示注入条件下，逐步干预平均将有害工具调用减少 **65%**，同时提高了良性任务完成率。
  - ShieldAgent：在其基准上报告 **90.1%** 的召回率，同时减少了 API 查询和推理时间。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19818v1](http://arxiv.org/abs/2604.19818v1)
