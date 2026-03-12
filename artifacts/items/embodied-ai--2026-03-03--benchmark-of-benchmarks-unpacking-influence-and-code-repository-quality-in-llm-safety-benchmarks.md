---
source: arxiv
url: http://arxiv.org/abs/2603.04459v1
published_at: '2026-03-03T09:10:45'
authors:
- Junjie Chu
- Xinyue Shen
- Ye Leng
- Michael Backes
- Yun Shen
- Yang Zhang
topics:
- llm-safety
- benchmark-analysis
- research-metrics
- code-quality
- reproducibility
relevance_score: 0.02
run_id: materialize-outputs
---

# Benchmark of Benchmarks: Unpacking Influence and Code Repository Quality in LLM Safety Benchmarks

## Summary
这篇论文系统评估了 LLM 安全基准测试论文的**学术影响力**与**代码仓库质量**，并分析两者是否一致。核心结论是：基准论文并没有显著更高的学术影响力，但其代码与维护通常更好，而且“有名作者/高影响论文”并不等于“高质量代码”。

## Problem
- LLM 安全研究增长极快，基准测试被广泛用于追踪进展，但**哪些基准更有影响力、为什么更有影响力**并不清楚。
- 社区通常默认“更有名的论文/作者”意味着更可靠、更可复现，但**代码仓库质量与可用性**缺乏系统审查。
- 这很重要，因为如果基准影响力与代码质量脱节，研究者可能会追随“更受关注”而非“更可复现”的评测工具，影响 LLM 安全研究的可靠性。

## Approach
- 收集并人工筛选 **31 篇 benchmark 论文** 与 **382 篇非 benchmark 论文**，覆盖 **prompt injection、jailbreak、hallucination** 三类 LLM 安全主题；对应公开仓库分别为 **27** 和 **168** 个。
- 用 **5 个影响力指标**评估论文影响：Citation Count、Citation Density、GitHub Star Count、GitHub Star Density、Scientific Field Count，并将 benchmark 与非 benchmark 做统计比较。
- 用 **自动化代码分析 + 人工运行评测**评估代码质量：自动部分含 Pylint、Radon、静态错误、维护频率等；人工部分检查代码是否可运行、是否需额外修改、安装说明、数据说明、伦理说明等。
- 进一步分析影响力与 11 个潜在因素的关系，包括作者声望、机构、地理、发表状态、搜索曝光，并检验**论文影响力与代码质量之间是否相关**。

## Results
- 在学术影响上，benchmark 论文**没有显著优于**非 benchmark：Citation Density **p=0.309**、Citation Count **p=0.237**、Scientific Field Count **p=0.632**，效应都可忽略。
- 在开源社区影响上，benchmark 论文更强：GitHub Star Density **p=0.012, Cliff's δ=-0.301（small）**；GitHub Star Count **p=0.004, δ=-0.347（medium）**。
- 作者声望与论文影响显著相关：Author H-Index (Top-1) 与 Citation Count **ρ=0.73**、Citation Density **ρ=0.71**、Scientific Field Count **ρ=0.68**；Author Citation Count (Top-1) 与 GitHub Star Count **ρ=0.58**、Star Density **ρ=0.55**。
- benchmark 论文的仓库开放度更高：**87%** benchmark 论文提供可访问仓库，而非 benchmark 仅 **44%**。
- 代码质量/维护方面，benchmark 仓库在 Pylint Score 与维护活跃度上更好：Pylint Score **p=0.031, δ=-0.276**；Reply Time **p=0.044, δ=-0.239**；Number of Commits **p=0.001, δ=-0.389**；Commit Frequency **p=0.010, δ=-0.309**。
- 但可复现性仍然较差：仅 **68%** benchmark 论文提供可运行脚本，只有 **39%** 的仓库可**无需修改直接运行**；仅 **16%** 提供**无缺陷安装指南**，仅 **6%** 涵盖伦理考虑。论文还声称：**作者声望和论文影响都与代码质量无显著相关**，说明“受关注”不等于“代码好用”。

## Link
- [http://arxiv.org/abs/2603.04459v1](http://arxiv.org/abs/2603.04459v1)
