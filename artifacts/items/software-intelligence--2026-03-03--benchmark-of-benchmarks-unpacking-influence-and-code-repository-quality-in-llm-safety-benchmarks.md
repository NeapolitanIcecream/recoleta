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
- benchmark-evaluation
- repository-quality
- research-metrics
- reproducibility
relevance_score: 0.58
run_id: materialize-outputs
---

# Benchmark of Benchmarks: Unpacking Influence and Code Repository Quality in LLM Safety Benchmarks

## Summary
本文系统评估了LLM安全基准论文的“影响力”和其配套代码仓库“质量”是否一致，覆盖提示注入、越狱和幻觉三类主题。结论是：基准论文在学术影响力上并不显著优于非基准论文，但其代码可用性与维护性整体更好，且“有名作者/高影响论文”并不意味着更高代码质量。

## Problem
- LLM安全研究增长极快，研究者越来越依赖benchmark来追踪进展，但哪些benchmark会更有影响力、为什么会更受关注，并不清楚。
- 现有工作很少系统检查benchmark论文的代码仓库质量、可复现性与补充材料是否真的可用，这直接影响研究复现和实际采用。
- 如果论文影响力与代码质量脱节，社区可能会更关注“名气大”的工作，而不是“更易复现、更负责任”的工作。

## Approach
- 作者构建了一个跨主题数据集：**31篇benchmark论文**与**382篇non-benchmark论文**，时间范围为 **2022-11-30 到 2024-11-01**，覆盖 **prompt injection、jailbreak、hallucination**。
- 用五类影响力指标评估论文/项目影响，包括 **Citation Count、Citation Density、GitHub Star Count、GitHub Star Density、Scientific Field Count**，并与non-benchmark对照比较。
- 用自动化与人工两种方式评估代码质量：自动化使用 **Pylint、Radon** 和GitHub维护指标；人工评估代码是否可运行、是否需要额外修改、安装指南/数据指南/伦理说明是否完善。
- 进一步分析影响力与11个潜在因素的关系，如 **作者h-index、作者引用数、机构、地区、发表状态、搜索出现频率**，并检验影响力与代码质量之间是否相关。

## Results
- 数据规模：共分析 **31 个benchmark论文**（其中 **27 个公开仓库**）和 **382 个non-benchmark论文**（其中 **168 个公开仓库**）。
- 学术影响力方面，benchmark与non-benchmark **无显著差异**：Citation Density **p=0.309, Cliff's δ=-0.112**；Citation Count **p=0.237, δ=-0.130**；Scientific Field Count **p=0.632, δ=-0.052**。
- 开源社区影响方面，benchmark更强：GitHub Star Density **p=0.012, δ=-0.301（small）**；GitHub Star Count **p=0.004, δ=-0.347（medium）**。
- 作者声望与影响力存在相关性：Author H-Index (Top-1) 与 Citation Count **ρ=0.73**、Citation Density **ρ=0.71**、Scientific Field Count **ρ=0.68**；Author Citation Count (Top-1) 与 GitHub Star Count **ρ=0.58**、Star Density **ρ=0.55**。
- 代码开放与工具评估上，benchmark更好：公开仓库比例 **87% vs 44%**；Pylint Score **p=0.031, δ=-0.276**；Reply Time **p=0.044, δ=-0.239**；Number of Commits **p=0.001, δ=-0.389**；Commit Frequency **p=0.010, δ=-0.309**。
- 人工复现显示仍有明显短板：只有 **68%** benchmark提供可运行脚本，只有 **39%** 仓库“无需修改即可运行”，仅 **16%** 提供**无缺陷**安装指南，仅 **6%** 包含伦理考虑；并且论文影响力与代码内在质量/维护频率 **未发现显著相关**。

## Link
- [http://arxiv.org/abs/2603.04459v1](http://arxiv.org/abs/2603.04459v1)
