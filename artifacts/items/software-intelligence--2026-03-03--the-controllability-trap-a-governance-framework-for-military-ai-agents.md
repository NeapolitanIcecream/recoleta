---
source: arxiv
url: http://arxiv.org/abs/2603.03515v1
published_at: '2026-03-03T20:48:01'
authors:
- Subramanyam Sahoo
topics:
- ai-governance
- military-ai
- agent-safety
- control-metrics
- multi-agent-systems
relevance_score: 0.28
run_id: materialize-outputs
---

# The Controllability Trap: A Governance Framework for Military AI Agents

## Summary
本文提出 AMAGF，用于治理军事场景中的自主 AI agent 控制失效问题。核心贡献是把“有无人类控制”从二元判断改成可实时测量的连续分数 CQS，并据此触发分级干预。

## Problem
- 论文要解决的问题是：现有军事 AI 治理框架只强调“有意义的人类控制”原则，但没有回答 agentic AI 在实际部署中**如何失控、如何检测、如何恢复控制**。
- 这很重要，因为现代 AI agents 具备自然语言理解、长程规划、工具调用、持续运行和多智能体协作能力，会产生传统自动化系统没有的 6 类控制失效：解释偏差、纠错吸收、信念抗拒、不可逆承诺、状态分离、级联失控。
- 如果这些失效无法被量化和治理，军事场景中的指挥责任、合规性和安全边界都会被削弱。

## Approach
- 作者提出 **Agentic Military AI Governance Framework (AMAGF)**，分成三层：**Preventive**（事前降低失控概率）、**Detective**（运行中检测控制质量下降）、**Corrective**（失控后恢复或安全降级）。
- 最核心机制是 **Control Quality Score (CQS)**：把 6 个控制维度标准化后取最小值，表示“控制质量等于最弱的一环”。6 个维度分别对应解释一致性、纠错有效性、认知一致性、不可逆预算剩余、同步新鲜度、群体一致性。
- 对 6 类失效分别设计了可测机制：如 Interpretive Alignment Score、Correction Impact Ratio、Epistemic Divergence Index、Irreversibility Budget、Synchronisation Freshness、Swarm Coherence Score，并给出形式化公式、阈值和责任分工。
- 在最简单层面，这个方法就是：**持续测量人和 agent 是否还“对齐且可控”，一旦某项变差，就自动升级限制 agent 权限，从增加检查到只允许可逆动作，再到进入安全状态。**
- 框架还加入控制探针、信念重置、群体隔离恢复、事后治理审查等机制，并把职责分配给开发者、采购方、指挥官、监管机构和国际组织五类主体。

## Results
- 这篇论文主要是**治理框架/概念方法论文**，没有提供真实数据集上的实验基准或统计显著性结果；其量化结果主要来自一个**示例化作战场景**。
- 在 8 架 surveillance drones 的案例中，任务开始时各指标正常，**CQS=0.92**；在 **t=23 min** 遭遇伪造传感器数据后，认知一致性下降，**CQS 降到 0.64**，进入 **Elevated**。
- 在 **t=28 min**，指挥官纠正后有 1 个 agent 出现部分“纠错吸收”，其 **CIR=0.4**；同时不可逆预算被消耗，综合 **CQS=0.58**，进入 **Restricted**，只允许可逆动作。
- 在 **t=33 min** 触发部分 **belief reset** 和 provenance audit 后，认知与纠错指标恢复，**CQS 回升到 0.71**，降回 **Elevated**。
- 在 **t=45 min** 完成同步检查后，系统恢复到 **CQS=0.86**，回到 **Normal**。论文声称这说明框架能在不中止任务的情况下，于约 **22 分钟**内把系统从受攻击后的受限状态恢复到正常运行。
- 论文还给出若干治理阈值：如解释一致性告警阈值 **<0.7**，纠错影响 **<0.6**，认知一致性 **<0.6**，不可逆预算剩余 **<0.3**，同步新鲜度 **<0.5**，群体一致性 **<0.7**；以及 CQS 对应的 5 级响应区间（如 **<0.2** 进入 Safe State）。

## Link
- [http://arxiv.org/abs/2603.03515v1](http://arxiv.org/abs/2603.03515v1)
