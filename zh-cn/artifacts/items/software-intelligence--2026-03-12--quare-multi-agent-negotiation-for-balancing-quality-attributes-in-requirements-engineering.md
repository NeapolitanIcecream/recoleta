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
- multi-agent-systems
- requirements-engineering
- llm-agents
- negotiation-protocol
- software-quality
- kaos-modeling
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# QUARE: Multi-Agent Negotiation for Balancing Quality Attributes in Requirements Engineering

## Summary
QUARE 是一个用于需求工程的多智能体框架，把不同质量属性之间的冲突显式地变成“协商”过程，而不是让单个 LLM 隐式折中。它的核心主张是：比起更大的模型，结构化的角色分工、谈判协议和自动验证更能提升需求分析质量。

## Problem
- 需求工程中常常要同时满足 **安全、效率、可持续、可信、责任/合规** 等互相冲突的质量属性，手工平衡这些约束既费时又容易出错。
- 现有 LLM 方法多是单体推理或隐式聚合，难以**显式暴露冲突、解释权衡理由、保留利益相关者原意**。
- 在软件项目里，需求问题很关键；文中指出**70% 以上失败项目**可追溯到需求相关缺陷，因此自动化且可追踪的需求分析很重要。

## Approach
- QUARE 将需求分析拆成 **5 个质量专长代理**（Safety、Efficiency、Green、Trustworthiness、Responsibility）加 **1 个 orchestrator**，所有代理共享同一 LLM 骨干，但通过不同系统提示实现角色隔离。
- 它使用一个**辩证式协商协议**：代理先提出需求，再由其他代理批评约束冲突，最后由协调器综合；冲突被分为 **resource-bound** 和 **logical incompatibility** 两类，并最多进行 **3 轮**协商。
- 为了找冲突，系统先用 **BERT embedding 余弦相似度阈值 0.85** 找潜在重叠，再用 LLM 判断是冗余还是两类冲突之一。
- 协商后的结果会被转换成 **KAOS 目标模型**，并做 **拓扑/DAG 校验**、规则检查、RAG 支持的幻觉与合规验证（如 **ISO 26262、ISO 27001**），最后输出标准化工程材料。
- 实验中用 **gpt-4o-mini-2024-07-18**，在 **5 个案例**（MARE、iReDev 基准和一个工业自动驾驶规格）上，对比 single-agent、无协商多代理、MARE、iReDev。

## Results
- 文中声称 QUARE 达到 **98.2% compliance coverage**，相对基线为 **+105%** 提升。
- 在语义保持上达到 **94.9% semantic preservation**，比最佳基线高 **+2.3 个百分点**。
- 可验证性评分达到 **4.96/5.0**。
- 生成的需求数量比现有多智能体 RE 框架多 **25–43%**。
- 协商在所有场景中都在 **3 轮上限内收敛**；实验使用 **3 个随机种子**、统一配置，共 **180 次运行**。
- 摘要与节选未提供每个数据集/每个基线的完整逐项数值表，但最强定量结论是：QUARE 在**合规覆盖、语义保持、可验证性和需求产出量**上整体优于所比较方法。

## Link
- [http://arxiv.org/abs/2603.11890v1](http://arxiv.org/abs/2603.11890v1)
