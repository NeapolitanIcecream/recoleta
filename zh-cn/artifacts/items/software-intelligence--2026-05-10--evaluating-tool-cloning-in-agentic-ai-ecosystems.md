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
## 摘要
这篇论文测量了公开 MCP 和 Skills 工具仓库中的代码克隆，发现重复实现已经多到足以扭曲工具计数、基准拆分和安全审查。

## 问题
- 公开的智能体工具平台会统计许多仓库和工具，但这些数字里可能包含被复制的代码、轻微修改的分支和从模板派生的工具。
- 重复实现会让相似代码泄漏到训练/测试拆分中，传播有漏洞的脚手架，并掩盖来源、归属和许可证义务。
- 这篇论文想回答的是，MCP 和 Skills 仓库里的克隆是少数现象，还是已经大到足以影响评估和治理。

## 方法
- 作者构建了一个统一的仓库级数据集，包含 7,508 个 MCP 仓库和 1,353 个 Skills 仓库，总共覆盖 100,011 条工具记录。
- 他们通过移除依赖项、生成产物、二进制文件、注释、多余空白和大小写差异来规范化仓库源码。
- 他们用 token 级 Jaccard 相似度和 `ssdeep` 模糊哈希比较仓库，然后对 MCP-MCP、Skills-Skills 和 MCP-Skills 配对做两两比较。
- 主要的跨开发者估计会排除同一开发者配对；他们还按相似度分桶手动核验抽样配对，检验高分是否真的表示代码克隆。

## 结果
- 数据集包含 8,861 个仓库：其中 7,508 个 MCP 仓库提取出 87,564 个工具，1,353 个 Skills 仓库提取出 12,447 个工具。
- 在 MCP-MCP 比较中，最高的 Jaccard 分桶 80-100 包含 758 对；人工复核把抽样的 20 对中的 12 对标为克隆，克隆率为 60%，95% CI 为 0.39-0.78。
- 在 MCP-MCP 比较中，最高的 `ssdeep` 分桶 80-100 包含 517 对；人工复核把抽样的 20 对中的 17 对标为克隆，克隆率为 85%，95% CI 为 0.64-0.95。
- 在 Skills-Skills 比较中，`ssdeep` 的 80-100 分桶包含 94 对；抽样的 20 对里有 15 对是克隆，克隆率为 75%，95% CI 为 0.53-0.89。
- 跨领域的 MCP-Skills 克隆较弱，但仍然存在：在 60-80 的 Jaccard 分桶中，抽样 8 对里有 4 对是克隆，克隆率为 50%，95% CI 为 0.22-0.78。
- 元数据高度集中：MCP 中的数据检索和 API 交互占 MCP 工具的 76.6%，Skills 中的开发者工具占 Skills 工具的 59.1%；这支持了论文的判断，即重复的包装器模式会让代码复用更可能发生。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09817v2](https://arxiv.org/abs/2605.09817v2)
