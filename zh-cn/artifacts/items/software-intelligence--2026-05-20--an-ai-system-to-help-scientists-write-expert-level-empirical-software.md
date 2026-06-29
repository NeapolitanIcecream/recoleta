---
source: hn
url: https://www.nature.com/articles/s41586-026-10658-6
published_at: '2026-05-20T23:54:12'
authors:
- anigbrowl
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- generative-engineering
- ai-for-science
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# An AI system to help scientists write expert-level empirical software

## Summary
## 摘要
ERA 是一个由 LLM 和树搜索组成的系统，用来为经验性任务编写科学软件，并针对特定任务的质量指标做优化。摘要声称，它在生物信息学、流行病学和其他科学领域都超过了强的人类或机构基线。

## 问题
- 当研究人员必须手工编写支持计算实验的定制软件时，科学发现会变慢。
- 许多经验性任务的设计空间很大，一次性代码生成可能找不到更好的算法或模型变体。
- 更好的自动化软件生成很重要，因为它可以测试更多想法，并减少构建实验专用工具所需的时间。

## 方法
- ERA 使用 LLM 来提出、实现和修改科学软件。
- 树搜索保留多个候选解路径，用质量指标给它们打分，并扩展最强的分支。
- 该系统可以读取并使用外部研究想法，然后测试生成的代码是否能改善该指标。
- 它把软件创建当作迭代优化：生成代码、评估、保留强的变体，再继续搜索。

## 结果
- 生物信息学：ERA 发现了 40 种用于单细胞数据分析的新方法，在公开排行榜上超过了最好的人工开发方法。
- 流行病学：ERA 生成了 14 个用于预测 COVID-19 住院情况的模型，在报告的基准中超过了 CDC 集成模型和其他所有单独模型。
- 其他领域：摘要称 ERA 在另外 4 个领域生成了专家级软件，分别是地理空间分析、斑马鱼神经活动预测、数值积分和时间序列预测。
- 摘要没有给出总体指标值、错误率或排行榜分数，只给出了 40 种方法和 14 个模型的数量，以及上述基线胜出结果。

## Problem

## Approach

## Results

## Link
- [https://www.nature.com/articles/s41586-026-10658-6](https://www.nature.com/articles/s41586-026-10658-6)
