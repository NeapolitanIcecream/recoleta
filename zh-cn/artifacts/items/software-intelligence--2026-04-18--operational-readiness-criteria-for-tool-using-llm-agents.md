---
source: hn
url: https://zenodo.org/records/19211676
published_at: '2026-04-18T23:22:13'
authors:
- rogelsjcorral
topics:
- llm-agents
- tool-using-agents
- deployment-readiness
- agent-evaluation
- ai-governance
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Operational Readiness Criteria for Tool-Using LLM Agents

## Summary
本文提出了一个面向使用工具的 LLM 代理的部署就绪模型。重点是判断一个代理在真实运营中何时已经足够安全、可靠，可以获得委派自治权限。

## Problem
- 团队可以构建使用工具的 LLM 代理，但在部署决策时，能力、自治、可审计性和发布控制往往缺少明确标准。
- 这很重要，因为一旦代理可以调用工具并以委派权限行动，若没有结构化检查就上线，可能引发运营、安全和合规问题。
- 这篇论文瞄准的是代理演示和生产运营之间的差距。

## Approach
- 核心方法是一个实用的就绪模型：在代理获得更多自治权限之前，先定义它必须满足的明确条件。
- 它围绕能力分级、自治预算、就绪评分卡、审计要求、评估工具链和分阶段发布门槛来组织部署。
- 能力分级用于划分代理可以处理哪些任务以及它能如何使用工具。
- 自治预算用于限制代理可以进行多少独立行动。
- 评分卡、审计和评估工具链让运营人员能在更大范围部署前测试并记录就绪情况。

## Results
- 摘要未报告量化基准结果、测试指标或一对一的基线比较。
- 主要的具体主张是，这项工作为部署使用工具的 LLM 代理提供了一个实用的就绪模型。
- 文中称其包含六个运营要素：能力分级、自治预算、就绪评分卡、审计要求、评估工具链和分阶段发布门槛。
- 该版本于 2026 年 3 月 25 日以 1.0 版发布。
- 这项工作还附带一个活跃的公开软件仓库：`rogelsjcorral/agentic-ai-readiness`。

## Link
- [https://zenodo.org/records/19211676](https://zenodo.org/records/19211676)
