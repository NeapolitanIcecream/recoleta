---
source: arxiv
url: http://arxiv.org/abs/2604.11270v2
published_at: '2026-04-13T10:24:28'
authors:
- Islem Bouzenia
- Cristian Cadar
- Michael Pradel
topics:
- llm-agents
- software-analysis
- benchmarking
- code-intelligence
- multi-step-automation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating LLM Agents on Automated Software Analysis Tasks

## Summary
## 总结
本文研究 LLM agent 是否能端到端地在开源项目上搭建并运行真实的软件分析工具。论文提出 AnalysisBench 作为这类任务的基准，并显示一个专门设计的 agent 的人工验证成功率远高于改造后的基线 agent。

## 问题
- 把分析工具用到新项目上很难，因为 agent 必须同时配置工具和目标项目、满足依赖、生成所需产物，并确认工具确实分析了项目。
- 之前的 agent 评估主要关注修复问题、代码修补或环境搭建，没有针对带工具特定证据检查的端到端自动化软件分析。
- 这会影响分析器、fuzzer、符号执行工具和性能分析工具在实际中的使用，因为配置和验证不可靠会挡住落地。

## 方法
- 论文把 **automated software analysis** 定义为完整流程：创建隔离容器、安装分析工具、构建目标项目、运行分析，并产出项目特定证据。
- 论文引入 **AnalysisBench**，这是一个包含 35 个工具-项目任务的基准，覆盖 7 种分析工具和 10 个开源 C/C++ 与 Java 项目，并配有人工构建的参考配置和验证产物。
- 作者在 4 个 LLM 后端上评估 4 种 agent 架构：RAG-Agent、Mini-SWE-Agent、ExecutionAgent，以及他们自定义的 **AnalysisAgent**。
- AnalysisAgent 采用三项主要机制：明确的工作流阶段、每轮只执行一个动作并对日志做确定性压缩，以及在停止前用 LLM 裁判做基于证据的完成检查。
- 成功标准是手动验证可复现环境和工具特定的分析输出，而不只是 agent 自称成功。

## 结果
- **AnalysisAgent + Gemini-3-Flash** 的**人工验证成功率为 94%（33/35 个任务）**，相比之下**最佳基线是 77%（ExecutionAgent + Gemini-3-Flash）**。
- 按 LLM 后端取平均，最佳基线的**人工验证成功率为 57%**，而 **AnalysisAgent 为 79%**，差距为 **20 个百分点**。
- 内部验证器把 **131/140** 个 AnalysisAgent 提交判为成功，但人工验证只确认了 **111** 个，因此自验证的**假阳性率为 15%**。
- 失败运行的代价更高：它们消耗的轮次是成功运行的 **2.77 倍**，成本是 **1.27 倍**，所以更高的成功率也提高了整体成本效率。
- 研究指出，**whole-program analyses 和 symbolic execution** 是最难的任务，**Java toolchains** 比 **C/C++** 更难。
- 常见的基线失败很具体：阶段混淆、从长日志里提取根因的能力差，以及在出现 `--help`、玩具运行或项目构建成功但没有真实分析输出时就过早停止。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11270v2](http://arxiv.org/abs/2604.11270v2)
