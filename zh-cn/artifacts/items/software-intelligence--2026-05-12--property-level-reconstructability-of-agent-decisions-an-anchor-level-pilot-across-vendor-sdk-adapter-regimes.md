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
这项试点检验了来自 agent SDK 的轨迹是否包含足够证据，能在属性级别重建 agent 决策。结果显示，可恢复的信息缺口很大，尤其是推理证据；但这项研究每个 SDK 只用了一个 worked-example anchor，也没有生产语料。

## 问题
- agent 失败后需要事后重建：发生了什么动作、谁授权了它、适用了哪项策略、以及哪些推理导致了这一步。
- 现有 agent 轨迹会因 SDK、适配器、运维侧仪表化和保存的工件不同而不同，所以同类决策下游调查者看到的证据也可能不同。
- 这篇论文与 agent 运维和治理相关，因为缺失的轨迹属性会阻碍对有害动作的事件分析，例如工具调用或状态变更。

## 方法
- 论文在不修改的情况下应用了已有的 Decision Trace Reconstructor v0.1.0。
- 它评估了 6 种 vendor SDK 机制中的 7 类 Decision Event Schema 属性：AWS Bedrock Agents、LangSmith/LangChain、Anthropic Claude tool use、OpenAI Agents/Assistants、OpenTelemetry GenAI/Vertex Agent Engine 和 MCP。
- 它增加了 2 个对照列：作者的 Operational Evidence Plane 作为上限参考，以及对 Replit DROP DATABASE 事件的公开记录重建。
- 每个属性都被归类为 fully fillable、partially fillable、structurally unfillable 或 opaque。
- 输入是固定的 worked-example anchors，每个单元格一个，输出可通过 checksum 验证，并放在一个 reproducibility package 中。

## 结果
- 主要的定量结论是，strict-governance-completeness 在锚点集合中分成 3 个层级，范围从 42.9% 到 85.7%。
- 论文报告了 1 个 regime-independent gap：在大多数被调查机制中，reasoning trace 证据缺失或不可用。
- 它报告了 4 个 regime-dependent gaps 和 1 个 Mixed 属性，这意味着大多数缺口随 SDK 证据形态变化，而不是统一出现。
- 研究覆盖了 6 种 vendor SDK 机制、2 个对照列、7 类属性，以及每个单元格 1 个 worked-example anchor。
- 该方法在固定输入上是确定性的；论文说明每个 anchor 最多有 50 个 fragments，在消费级笔记本上每个 anchor 运行时间少于 10 秒。
- 证据规模是试点级：单一标注者、用 worked examples 而不是采集到的生产轨迹，而且没有对 SDK 可互换性做统计检验。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12078v1](https://arxiv.org/abs/2605.12078v1)
