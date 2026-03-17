---
source: arxiv
url: http://arxiv.org/abs/2603.11082v1
published_at: '2026-03-10T23:49:09'
authors:
- Yen-Ku Liu
- Yun-Cheng Tsai
topics:
- llm-agents
- software-design
- inference-time-reasoning
- self-verification
- code-quality
relevance_score: 0.94
run_id: materialize-outputs
---

# Quality-Driven Agentic Reasoning for LLM-Assisted Software Design: Questions-of-Thoughts (QoT) as a Time-Series Self-QA Chain

## Summary
本文提出 QoT（Questions-of-Thoughts），一种面向软件设计质量的推理脚手架，让 LLM 先分解工程步骤，再对每一步做自问自答式检查。它旨在减少遗漏、提升模块化与安全性，并留下可复用的轻量推理记录。

## Problem
- 现有 LLM 辅助软件开发常能生成“看起来能用”的代码，但在**完整性、模块化、安全性**上经常不足，尤其在多模块、长链路任务中容易漏掉关键约束。
- 只看功能是否跑通不够，因为真实软件系统还需要**可维护、可审计、可部署**；这对后端系统、企业流程和合规场景尤其重要。
- 现有 CoT/ToT/自我修正方法通常更偏向“生成后再改”，缺少围绕软件质量属性的**前置约束梳理和逐步验证机制**。

## Approach
- QoT 把用户目标先拆成**有顺序的工程步骤**（Sequential Process Chain），例如先用户模块、再业务模块、再路由与集成，避免一次性生成时遗漏依赖关系。
- 对每一步，模型会自动提出一组**自检问题**（Question-Answer Chain），用最简单的话说，就是“边做边问自己：有没有权限控制？有没有错误处理？有没有并发/一致性问题？”
- 系统把中间结论持续写入一个**推理知识库**（Reasoning Knowledge Base），作为后续步骤的上下文，帮助后面的设计与前面的约束保持一致。
- 该方法是**推理时增强**而不是训练新模型：底座模型不变，只在推理流程外面套上一个质量驱动的 agentic scaffold。
- 评测中，作者用一个受 ISO/IEC 启发的质量量表，对**Scalability、Completeness、Modularity、Security**四项进行 1–4 分打分，并比较 QoT 与 NoQoT、CoT 的差异。

## Results
- 在 **QoT vs CoT** 对比中，**llama3.1_70b** 提升最明显：API Design **+5.8±1.30**，Data Communication **+6.6±0.89**，File Systems **+3.2±1.48**。
- 在 **QoT vs CoT** 中，**llama3.3_70b** 也在三域全部为正：API **+2.2±2.28**，Data Communication **+4.8±2.17**，File Systems **+2.2±3.90**。
- 小模型也有收益但更不稳定：**llama3.1_8b** 对 CoT 的提升为 API **+2.0±1.73**、Communication **+2.4±3.05**、FS **+1.2±2.77**；**llama3.2_3b** 为 API **+3.6±2.51**、Communication **+1.4±1.67**、FS **+1.4±5.86**。
- 在 **QoT vs NoQoT** 中，结果呈现容量依赖与任务依赖：例如 **llama3.1_70b** 在 API **+3.4±1.34**、Communication **+5.4±1.67**，但在 File Systems **-2.8±1.10**；**llama3.3_70b** 在 FS 也出现 **-3.0±3.46**，作者将其解释为可能的“过度思考/过度工程化”。
- 图中汇总百分比结果显示：**llama3.2_3b** 在 QoT vs NoQoT 下总改进达 **101.49%**，**llama3.1_70b** 为 **23.08%**，**llama3.1_8b** 为 **23.81%**，**llama3.3_70b** 为 **2.80%**。
- 论文的核心突破性主张是：QoT 能在**不改模型参数**的前提下，通过“分步规划 + 自检问答 + 累积记忆”显著提升软件设计质量，并且在部分场景下让**较小模型逼近较大模型的单次生成质量**。

## Link
- [http://arxiv.org/abs/2603.11082v1](http://arxiv.org/abs/2603.11082v1)
