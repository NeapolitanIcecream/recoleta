---
source: arxiv
url: https://arxiv.org/abs/2605.12078v1
published_at: '2026-05-12T13:05:02'
authors:
- Oleg Solozobov
topics:
- agent-observability
- decision-reconstruction
- software-agents
- runtime-tracing
- ai-governance
relevance_score: 0.68
run_id: materialize-outputs
language_code: zh-CN
---

# Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes

## Summary
## 摘要
这项试点研究测试代理 SDK 的轨迹是否包含足够证据，能够在属性层级重建代理决策。研究发现，可恢复内容存在较大缺口，推理证据尤其不足，但该研究对每个 SDK 只使用一个工作示例锚点，没有使用生产语料库。

## 问题
- 代理故障需要事后重建：发生了什么动作、由谁授权、适用了哪项策略，以及哪些推理导致了该动作。
- 当前代理轨迹会随 SDK、适配器、操作方埋点和已存储工件而变化，因此后续调查人员面对同一类决策时，可能看到不同的证据。
- 这篇论文对代理运维和治理有意义，因为缺失的轨迹属性可能阻碍对工具调用或状态变更等有害动作的事件分析。

## 方法
- 论文直接使用现有的 Decision Trace Reconstructor v0.1.0，没有修改。
- 它在 6 个厂商 SDK 机制中评估 7 类 Decision Event Schema 属性：AWS Bedrock Agents、LangSmith/LangChain、Anthropic Claude tool use、OpenAI Agents/Assistants、OpenTelemetry GenAI/Vertex Agent Engine 和 MCP。
- 它增加了 2 个对照列：作者的 Operational Evidence Plane，作为上限参照；以及对 Replit DROP DATABASE 事件的公开记录重建。
- 每个属性被分类为完全可填充、部分可填充、结构上不可填充或不透明。
- 输入是固定的工作示例锚点，每个单元格一个；输出包含在可复现包中，可通过校验和验证。

## 结果
- 主要定量结论是，在该锚点集合中，strict-governance-completeness 分为 3 个层级，范围从 42.9% 到 85.7%。
- 论文报告了 1 个与机制无关的缺口：在大多数受调查机制中，推理轨迹证据缺失或不可用。
- 论文报告了 4 个依赖机制的缺口和 1 个 Mixed 属性，意思是多数缺口会随 SDK 证据形态变化，并非统一出现。
- 研究覆盖 6 个厂商 SDK 机制、2 个对照列、7 类属性，以及每个单元格 1 个工作示例锚点。
- 该方法在固定输入上是确定性的；论文称每个锚点最多 50 个片段，在消费级笔记本电脑上每个锚点运行时间低于 10 秒。
- 证据规模属于试点级别：单一标注者，使用工作示例而非捕获的生产轨迹，也没有对 SDK 可互换性进行统计检验。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12078v1](https://arxiv.org/abs/2605.12078v1)
