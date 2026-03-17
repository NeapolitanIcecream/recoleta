---
source: arxiv
url: http://arxiv.org/abs/2603.11356v1
published_at: '2026-03-11T22:43:55'
authors:
- Jatin Ganhotra
- Sami Serhan
- Antonio Abu Nassar
- Avraham Shinnar
- Ziv Nevo
- Martin Hirzel
topics:
- java-code-repair
- issue-resolution
- llm-agents
- static-analysis
- software-engineering-benchmarks
relevance_score: 0.01
run_id: materialize-outputs
---

# Resolving Java Code Repository Issues with iSWE Agent

## Summary
本文提出面向 Java 代码仓库问题修复的 iSWE Agent，通过将定位与编辑拆成两个子代理，并结合 Java 静态分析与受控编辑工具，提升自动 issue resolution 的效果与效率。作者声称该方法在两个 Java 基准上达到当前最优或接近最优的修复成功率，同时显著降低推理成本。

## Problem
- 现有自动化 issue resolution 系统大多偏向 Python，在 Java 上表现较弱，而 Java 在企业软件中非常重要。
- Java 的强类型、编译依赖、多文件改动和面向对象结构，使自动修复比 Python 更难，单靠通用工具或简单 linter 不够。
- 需要回答一个关键问题：**Java 专用工具和语言感知机制**是否能实质提升仓库级问题修复能力。

## Approach
- 将任务拆成两个 ReAct 子代理：**localization agent** 先找需要修改的代码位置，**editing agent** 再根据这些位置生成补丁。
- localization 使用 7 个主要为只读的 Java 专用工具，如类/方法/符号查询、调用链、继承层次分析；底层基于 **CLDK + Tree-Sitter** 做规则式静态分析。
- editing 使用受控的 **search-replace / merge-conflict 格式** 生成补丁，而不是任意执行 bash 或代码，减少副作用并降低 LLM 交互轮数。
- 编辑阶段采用逐级校验：先检查补丁格式与匹配，再做轻量 Java lint，最后仅在必要时进入容器执行项目构建/编译检查，以兼顾安全性与反馈质量。
- 系统整体是 **LLM-agnostic** 的，提示与流程通过 PDL 编排，强调规则式工具与模型式推理的结合。

## Results
- 在 **Multi-SWE-bench (Java, 128 个实例)** 和 **SWE-PolyBench (Java, 165 个实例)** 上评测，总计 **293 个 Java 实例**。
- 论文声称 iSWE 在两个公开 Java 榜单上都达到 **state-of-the-art 或 near-the-top** 的 issue resolution success rate，但摘录中**未给出具体成功率百分比、对比方法数值或分榜单详细指标**。
- 在成本方面，作者明确声称：相较于使用**同一 LLM** 的其他领先 agent，iSWE 的模型 API 推理费用降低约 **2× 到 3×**。
- 文中还提到分析了其他指标，如 **localization precision / recall** 以及按问题复杂度分解的表现，但当前提供文本中**没有展开具体数值**。
- 最强的可核实结论是：**Java 专用、规则增强的两阶段代理**在 Java issue resolution 上兼顾了更强表现与更低成本。

## Link
- [http://arxiv.org/abs/2603.11356v1](http://arxiv.org/abs/2603.11356v1)
