---
source: arxiv
url: https://arxiv.org/abs/2605.09817v2
published_at: '2026-05-10T23:39:44'
authors:
- Taein Kim
- David Jiang
- Yuepeng Hu
- Yuqi Jia
- Neil Gong
topics:
- agent-tools
- code-cloning
- mcp
- skills
- benchmark-contamination
- software-provenance
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating Tool Cloning in Agentic-AI Ecosystems

## Summary
## 概要
本文衡量公共 MCP 和 Skills 工具仓库中的代码克隆情况，发现重复实现已经常见到足以扭曲工具数量、基准测试划分和安全审查。

## 问题
- 公共 agent 工具平台统计了大量仓库和工具，但这些数量可能包含复制代码、轻度编辑的 fork，以及从模板派生的工具。
- 重复实现可能让相似代码泄漏到训练/测试划分两侧，传播有漏洞的脚手架，并使来源、署名和许可证义务变得不清楚。
- 论文研究 MCP 和 Skills 仓库中的克隆是否已经大到会影响评估和治理。

## 方法
- 作者构建了一个统一的仓库级数据集，包含 7,508 个 MCP 仓库和 1,353 个 Skills 仓库，总计覆盖 100,011 个工具条目。
- 他们通过移除依赖项、生成产物、二进制文件、注释、多余空白，并统一大小写，对仓库源代码进行规范化。
- 他们使用 token 级 Jaccard 相似度和 `ssdeep` 模糊哈希比较仓库，然后对 MCP-MCP、Skills-Skills 和 MCP-Skills 仓库对进行成对比较。
- 他们在主要跨开发者估计中排除同一开发者的仓库对，并人工核查各相似度区间中的抽样仓库对，以测试高分是否对应真实克隆。

## 结果
- 数据集包含 8,861 个仓库：7,508 个 MCP 仓库，提取出 87,564 个工具；1,353 个 Skills 仓库，包含 12,447 个工具。
- 在 MCP-MCP 比较中，最高 Jaccard 区间 80-100 包含 758 个仓库对；人工审查将 20 个抽样仓库对中的 12 个标记为克隆，克隆率为 60%，95% CI 为 0.39-0.78。
- 在 MCP-MCP 比较中，最高 `ssdeep` 区间 80-100 包含 517 个仓库对；人工审查将 20 个抽样仓库对中的 17 个标记为克隆，克隆率为 85%，95% CI 为 0.64-0.95。
- 在 Skills-Skills 比较中，80-100 `ssdeep` 区间包含 94 个仓库对；20 个抽样仓库对中有 15 个是克隆，克隆率为 75%，95% CI 为 0.53-0.89。
- 跨域 MCP-Skills 克隆较弱但存在：在 60-80 Jaccard 区间，8 个抽样仓库对中有 4 个是克隆，克隆率为 50%，95% CI 为 0.22-0.78。
- 元数据呈集中分布：MCP 数据检索和 API 交互占 MCP 工具的 76.6%，而 Skills 开发者工具占 Skills 工具的 59.1%；这支持了论文的说法，即重复的包装器模式使代码复用更可能发生。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09817v2](https://arxiv.org/abs/2605.09817v2)
