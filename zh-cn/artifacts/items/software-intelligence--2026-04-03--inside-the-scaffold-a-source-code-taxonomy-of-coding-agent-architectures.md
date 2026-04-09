---
source: arxiv
url: http://arxiv.org/abs/2604.03515v1
published_at: '2026-04-03T23:30:02'
authors:
- Benjamin Rombaut
topics:
- coding-agents
- source-code-taxonomy
- agent-architecture
- software-engineering
- llm-scaffolds
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures

## Summary
## 摘要
这篇论文基于源代码，为 13 个开源编程代理脚手架建立了一套分类体系。论文认为，编程代理之间的差异，更多来自控制循环、工具、状态和上下文处理这些具体的脚手架选择，而不是“规划”或“工具使用”这类高层标签。

## 问题
- 研究综述通常按抽象能力对编程代理分组，但这些标签无法区分脚手架代码、成本和失效模式差异很大的系统。
- 轨迹研究展示了代理在运行时做了什么，但没有检查驱动这些行为的源代码。
- 这很重要，因为脚手架设计会影响可靠性、token 使用和评估，而当前基准测试结果往往把脚手架效应和模型效应混在一起。

## 方法
- 作者分析了 13 个固定 commit hash 的开源编程代理，覆盖 CLI 工具、SWE-bench 代理和一个最小基线。
- 他们不是根据文档，而是通过检查源代码来建立分类，并用文件路径和行号支撑每一项结论。
- 每个代理都从 3 个层级的 12 个维度进行描述：控制架构、工具与环境接口、资源管理。
- 研究识别出 5 种可复用的循环原语：ReAct、生成-测试-修复、规划-执行、多次尝试重试、树搜索。
- 论文比较了各个代理如何组合这些原语，以及它们在工具数量、上下文压缩、状态管理、执行隔离和模型路由上的差异。

## 结果
- 语料库包含 **13 个代理**，从最初 **22** 个候选中筛选而来。
- **13 个代理中的 11 个** 组合了多种循环原语，而不是只使用单一控制结构。
- **13 个代理中的 7 个** 将顺序式 **ReAct** 循环作为主要控制结构。
- 工具可用性差异很大，从 Aider 的 **0 个工具** 到 Moatless Tools 的 **37 个动作类**。
- 上下文压缩涵盖 **7 种不同策略**，控制设计则从固定流水线延伸到完整的 **Monte Carlo Tree Search**。
- 论文**没有报告基准提升或新的任务表现数据**。它最具体的结论是，编程代理脚手架很难被干净地划分为离散类别，更适合被描述为沿连续设计谱系进行组合。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03515v1](http://arxiv.org/abs/2604.03515v1)
