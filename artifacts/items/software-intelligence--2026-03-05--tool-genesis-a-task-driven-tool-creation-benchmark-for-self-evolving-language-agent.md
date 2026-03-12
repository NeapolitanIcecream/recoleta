---
source: arxiv
url: http://arxiv.org/abs/2603.05578v1
published_at: '2026-03-05T17:44:29'
authors:
- Bowei Xia
- Mengkang Hu
- Shijian Wang
- Jiarui Jin
- Wenxiang Jiao
- Yuan Lu
- Kexin Li
- Ping Luo
topics:
- tool-creation-benchmark
- language-agents
- code-generation
- mcp
- self-evolving-agents
relevance_score: 0.93
run_id: materialize-outputs
---

# Tool-Genesis: A Task-Driven Tool Creation Benchmark for Self-Evolving Language Agent

## Summary
Tool-Genesis 是一个面向“自进化语言代理”工具创建能力的诊断型基准，要求模型仅从抽象任务需求中推断工具接口、生成可执行实现，并衡量这些工具在真实任务中的可复用性与效用。论文表明，即使最先进模型在一次生成中也常因接口或实现的小错误而在后续流程中被放大，导致端到端性能显著下滑。

## Problem
- 现有工具使用/工具创建评测大多依赖预定义规格或参考接口，无法真正测试代理能否**从模糊需求自主设计工具**。
- 很多基准只看最终任务结果，像“黑箱”一样，难以区分失败是来自**接口设计错误、代码实现错误，还是工具使用策略错误**。
- 这很重要，因为真实部署中 API/工具规格常缺失、变化或不完整；若代理不能创建、修复和维护工具，就难以支持长期的软件自动化与自进化能力。

## Approach
- 提出 **Tool-Genesis**：一个 requirement-driven 的工具创建基准，要求模型从自然语言需求生成 **MCP 工具 schema** 和 **可执行 server 实现**，而不是只调用现成 API。
- 将任务拆成两阶段：**接口预测**（先猜工具名、参数、约束、描述）和 **工具具象化**（再按 schema 写出可执行实现），并区分 **Oracle Materialization** 与 **Cascaded Materialization** 以隔离不同误差来源。
- 设计四层评测：L1 表面合规/可执行性，L2 **Schema-F1** 接口语义保真，L3 **UT_soft / UT_hard** 功能正确性（含边界/负例测试），L4 下游任务成功率 **SR**。
- 引入 **oracle-normalized success rate**，把生成工具与参考真值工具在同一任务分布下比较，量化“离理想可用工具还差多少”。
- 数据集通过 MCP server 抓取、任务与轨迹生成、单元测试抽取/合成、人工复核构建，最终包含 **86 servers、508 tools、24 domains、2150 tasks、9441 unit tests**；人工复核的 Cohen’s kappa 为 **0.85**。

## Results
- 基准规模上，Tool-Genesis 覆盖 **86** 个 MCP servers、**508** 个工具、**24** 个领域、**2150** 个任务、**9441** 个单元测试；平均任务长度 **53** tokens、平均 **6** 步执行、平均使用 **3** 个工具。
- 在 **Direct** 一次生成下，最佳模型 **gpt-5.1** 也只有：Compliance **0.826**、Exec **0.759**、Schema-F1 **0.688**、UT_soft **0.281**、UT_hard **0.161**、SR **0.372**，说明单次生成下端到端可用性仍然有限。
- 在 **Code-Agent** 闭环修复下，最好结果显著提升：**gpt-5.1** 达到 Compliance **0.895**、Exec **0.941**、Schema-F1 **0.867**、UT_soft **0.421**、UT_hard **0.246**、SR **0.604**；**Kimi-K2** 的 SR 为 **0.585**，**gemini-3-flash-preview** 的 SR 为 **0.581**。
- 论文强调闭环执行反馈带来跨层改进。例如 **gemini-3-flash-preview** 从 Direct 到 Code-Agent：Exec **0.140→0.977**，Schema-F1 **0.116→0.912**，UT_soft **0.084→0.448**，UT_hard **0.037→0.255**，SR **0.103→0.581**。
- 即便上游信号较强，下游效用仍可能明显不足，暴露“utility-conversion bottleneck”。例如在表 2 中，**Qwen3-32B (Code-Agent)** 的 Exec **0.892**、Schema-F1 **0.801**，但 SR 仅 **0.495**；说明接口像样并不等于工具真正稳健可用。
- 论文的核心结论是：**最先进模型仍难以在 one-shot 情况下准确构造工具接口和可执行逻辑**，且这些微小初始错误会沿流水线累积放大；Tool-Genesis 因此更像一个定位问题根因的“诊断仪”，而不只是排行榜。

## Link
- [http://arxiv.org/abs/2603.05578v1](http://arxiv.org/abs/2603.05578v1)
