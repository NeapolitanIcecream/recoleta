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
## 摘要
本文研究 LLM 智能体是否能在开源项目上端到端地搭建并运行真实的软件分析工具。论文提出了用于这一任务的基准 AnalysisBench，并表明，一个为该任务专门设计的智能体，其经验证的成功率明显高于改造后的基线智能体。

## 问题
- 将分析工具应用到新项目上很难，因为智能体必须同时搭建工具和目标项目，满足依赖，生成所需产物，并确认工具确实对项目完成了分析。
- 以往对智能体的评估主要关注问题解决、修复或环境搭建，而不是带有工具特定证据检查的端到端自动化软件分析。
- 这很重要，因为搭建和验证做不好，会阻碍分析器、模糊测试器、符号执行工具和性能分析器在实际中的采用。

## 方法
- 论文将**自动化软件分析**定义为一条完整流程：创建隔离容器、安装分析工具、构建目标项目、运行分析，并生成项目特定的证据。
- 论文提出 **AnalysisBench**，这是一个包含 35 个工具-项目任务的基准，覆盖 7 种分析工具和 10 个开源 C/C++ 与 Java 项目，并提供人工构建的参考搭建方案和验证产物。
- 作者在 4 个 LLM 后端上评估了 4 种智能体架构：RAG-Agent、Mini-SWE-Agent、ExecutionAgent，以及他们自定义的 **AnalysisAgent**。
- AnalysisAgent 使用三项主要机制：显式工作流阶段、每轮一个动作并配合确定性的日志压缩，以及在停止前用 LLM 裁判执行基于证据的完成检查。
- 成功与否通过人工验证可复现环境和工具特定分析输出来衡量，而不只是看智能体是否声称成功。

## 结果
- **AnalysisAgent + Gemini-3-Flash** 达到 **94% 的验证成功率（33/35 个任务）**，而 **77%（最佳基线：ExecutionAgent + Gemini-3-Flash）**。
- 在各个 LLM 后端上取平均时，最佳基线达到 **57% 的验证成功率**，而 **AnalysisAgent 达到 79%**，相差 **20 个百分点**。
- 内部验证器将 **131/140** 个 AnalysisAgent 提交判定为成功，但人工验证只确认了 **111** 个，因此自验证的**假阳性率为 15%**。
- 失败运行成本更高：它们消耗的循环次数是成功运行的 **2.77×**，成本是成功运行的 **1.27×**，所以更高的成功率也提升了总成本效率。
- 研究报告称，**全程序分析和符号执行**是最难的任务，而在这个基准中，**Java 工具链**比 **C/C++** 更难处理。
- 基线方法的常见失败原因很具体：阶段混杂、无法从长日志中准确提取根因，以及在只看到 `--help`、一次玩具式运行，或仅完成项目构建而没有真实分析输出时就提前停止。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11270v2](http://arxiv.org/abs/2604.11270v2)
