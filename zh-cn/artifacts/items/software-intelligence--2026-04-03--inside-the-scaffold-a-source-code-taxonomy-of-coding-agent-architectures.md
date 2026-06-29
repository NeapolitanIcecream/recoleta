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
本文构建了一个针对 13 个开源编码代理脚手架的源码级分类法。它认为，编码代理之间的差异，与其说来自“规划”或“工具使用”这类高层标签，不如说来自控制循环、工具、状态和上下文处理这些具体的脚手架选择。

## 问题
- 研究综述通常按抽象能力对编码代理分组，但这些标签无法区分脚手架代码、成本和失效模式差别很大的系统。
- 轨迹研究展示的是代理在运行时做了什么，但没有检查驱动这些行为的源代码。
- 这很重要，因为脚手架设计会影响可靠性、token 用量和评估，而现有基准结果往往把脚手架效应和模型效应混在一起。

## 方法
- 作者分析了 13 个开源编码代理，版本固定在指定提交哈希，覆盖 CLI 工具、SWE-bench 代理和一个最小基线。
- 他们基于源代码检查而不是文档来归纳分类法，并把每条结论都落实到文件路径和行号。
- 每个代理都从 12 个维度、3 个层次来描述：控制架构、工具与环境接口、资源管理。
- 研究识别出 5 个可复用的循环原语：ReAct、generate-test-repair、plan-execute、multi-attempt retry 和 tree search。
- 研究比较了代理如何组合这些原语，以及它们在工具数量、上下文压缩、状态管理、执行隔离和模型路由上的差异。

## 结果
- 语料库包含 **13 个代理**，从最初的 **22** 个候选项中选出。
- **13 个中的 11 个代理** 组合了多个循环原语，而不是只用单一控制结构。
- **13 个中的 7 个代理** 把顺序式 **ReAct** 循环作为主要控制结构。
- 工具可用性从 Aider 的 **0 个工具** 到 Moatless Tools 的 **37 个动作类** 不等。
- 上下文压缩包含 **7 种不同策略**，控制设计则从固定流水线一直到完整的 **Monte Carlo Tree Search**。
- 论文**没有报告基准提升或新的任务性能数值**。它的主要具体结论是，编码代理脚手架很难被清晰地离散分类，更适合被描述为沿着连续设计谱的组合。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03515v1](http://arxiv.org/abs/2604.03515v1)
