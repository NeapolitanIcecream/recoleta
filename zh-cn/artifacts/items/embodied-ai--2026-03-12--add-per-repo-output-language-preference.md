---
source: hn
url: https://news.ycombinator.com/item?id=47358750
published_at: '2026-03-12T23:32:35'
authors:
- nishiohiroshi
topics:
- developer-tools
- code-review
- localization
- ai-assistant
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Add per-repo output language preference

## Summary
这不是一篇研究论文，而是一则产品更新说明：GitAuto 新增了按代码仓库设置输出语言偏好的功能，让 AI 生成的代码审查评论可用团队母语展示。其价值主要在于改善非英语开发团队阅读和审查 AI 生成 PR 评论的可用性，而非提出新的算法方法。

## Problem
- 非英语开发团队在审查 AI 生成的 PR 评论和代码注释时，若内容默认是英语，会增加理解成本与协作摩擦。
- 多仓库团队可能需要不同语言策略，缺少按仓库粒度的语言配置会降低工作流灵活性。
- 该问题重要性在于代码审查是高频协作环节，语言障碍会直接影响审查效率与沟通质量。

## Approach
- 提供**per-repo** 的输出语言偏好设置，可在仓库规则设置（Rules Settings）中单独配置。
- GitAuto 将其生成的代码评论与 GitHub 评论翻译或输出为目标母语，支持 **70+ 种语言**。
- 同时保留 **PR 标题和正文为英文**，说明其机制是对部分输出通道做语言本地化，而不是整个 PR 元数据全面切换语言。
- 文本未描述底层模型、翻译管线、质量控制或任何新的研究性技术机制。

## Results
- 给出的唯一明确量化信息是：支持 **70+ languages**。
- 文章未提供任何实验、基准、数据集、A/B 测试或效率指标，因此**没有可验证的定量研究结果**。
- 最强的具体产品声明是：非英语团队现在可以用母语阅读 GitAuto 的代码评论和 GitHub 评论。
- 另一个具体约束性声明是：**PR titles and bodies stay in English**，说明当前功能范围有限且是局部本地化。

## Link
- [https://news.ycombinator.com/item?id=47358750](https://news.ycombinator.com/item?id=47358750)
