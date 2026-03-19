---
source: arxiv
url: http://arxiv.org/abs/2603.11890v1
published_at: '2026-03-12T13:03:01'
authors:
- Haowei Cheng
- Milhan Kim
- Foutse Khomh
- Teeradaj Racharak
- Nobukazu Yoshioka
- Naoyasu Ubayashi
- Hironori Washizaki
topics:
- requirements-engineering
- multi-agent-negotiation
- llm-agents
- kaos-modeling
- compliance-verification
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# QUARE: Multi-Agent Negotiation for Balancing Quality Attributes in Requirements Engineering

## Summary
QUARE 是一个把需求工程拆成多个“质量立场代理”来协商的多智能体框架，目标是在安全、效率、可持续性、可信性和责任性之间做可追踪的权衡。论文主张，相比单体式或隐式聚合的 LLM 方法，显式谈判与自动验证更能产出完整、合规且语义保持良好的需求模型。

## Problem
- 需求工程中常常要同时满足彼此冲突的质量属性，如安全、性能、隐私与合规；手工平衡这些约束费时且易出错。
- 现有 LLM RE 方法多依赖单代理推理或隐式汇总，难以**显式发现、分类并解决**跨质量冲突，导致权衡理由不透明。
- 软件项目失败中很大一部分与需求问题有关；在自动驾驶等安全关键场景中，这种缺陷会直接影响系统可靠性与监管合规性。

## Approach
- 使用 5 个质量专长代理（Safety、Efficiency、Green、Trustworthiness、Responsibility）加 1 个 Orchestrator，将需求分析按质量维度而非任务维度分解。
- 设计了 5 阶段流水线：并行生成需求、辩证式谈判、KAOS 目标模型集成与拓扑校验、RAG+规则的合规验证、标准化工程产物生成。
- 核心机制是显式协商：代理围绕冲突需求进行“提案—批评—综合”的多轮对话，最多 3 轮；冲突先用嵌入相似度筛出，再由 LLM 分类为冗余、资源冲突或逻辑不兼容。
- 谈判结果被转换为结构化 KAOS 目标图，并通过 DAG/拓扑有效性检查以及对 ISO 26262、ISO 27001、ISO/IEC/IEEE 29148 等标准的检索增强验证来保证工程可用性。
- 评测上除了传统语义保持与一致性，还引入五维质量空间中的几何指标，如 CHV 和 MDC，衡量需求覆盖的广度与分散度。

## Results
- 在 5 个案例研究（MARE、iReDev 基准及工业自动驾驶规范）上，QUARE 报告 **98.2% compliance coverage**，相对两类基线都提升 **+105%**。
- 语义保持达到 **94.9% semantic preservation**，比最佳基线高 **+2.3 个百分点**。
- 可验证性评分达到 **4.96/5.0**。
- 生成的需求数量比现有多智能体 RE 框架多 **25–43%**。
- 论文称谈判在所有场景下都能在 **最多 3 轮** 内收敛；实验使用 **gpt-4o-mini-2024-07-18**，共 5 个案例、4 种设置、3 个随机种子，合计 **180 次运行**。
- 论文未在给定摘录中提供所有几何指标（如 CHV、MDC、CRR）的具体数值，但最强定量结论是其在合规覆盖、语义保持和需求数量上全面优于单代理、无谈判多代理、MARE 与 iReDev 基线。

## Link
- [http://arxiv.org/abs/2603.11890v1](http://arxiv.org/abs/2603.11890v1)
