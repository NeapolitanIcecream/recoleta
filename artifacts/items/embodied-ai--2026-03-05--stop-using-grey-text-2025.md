---
source: hn
url: https://catskull.net/stop-using-grey-text.html
published_at: '2026-03-05T23:15:57'
authors:
- catskull
topics:
- web-accessibility
- color-contrast
- ui-design
- css
relevance_score: 0.0
run_id: materialize-outputs
---

# Stop using grey text (2025)

## Summary
这不是一篇机器人或机器学习研究论文，而是一篇关于网页可读性与无障碍的短文。作者强烈反对在浅色背景上使用灰色正文，认为这会显著降低阅读体验并排斥部分用户。

## Problem
- 文章要解决的问题是：许多网页设计故意使用低对比度的灰色文字配浅灰/米白背景，导致内容难以阅读。
- 这很重要，因为低对比度会伤害可访问性，增加普通用户和视力受限用户的阅读负担，并直接缩小潜在受众。
- 作者还指出，这种做法通常是人为覆盖默认文字颜色造成的，也就是说问题并非技术限制，而是设计选择。

## Approach
- 核心方法非常简单：**不要再用低对比度灰字**，优先使用高对比度正文颜色。
- 如果设计上坚持使用低对比度方案，作者建议至少支持 CSS 的 `prefers-contrast` 媒体查询，让需要更高对比度的用户能够获得更易读的版本。
- 文章通过直接对设计师发出批评、给出简单 CSS 方向、以及展示“对比度演示”来说明可读性问题。
- 本质机制是：提高前景文字与背景之间的亮度/颜色对比，从而提升信息传达的清晰度与阅读舒适度。

## Results
- 文本**没有提供正式实验、数据集、指标或定量结果**，因此没有可报告的数值型突破结果。
- 最强的具体主张是：灰字配浅背景会让用户怀疑自己“是不是视力变差了”，说明其主观阅读负担明显增加。
- 作者声称，提高对比度对所有人都有帮助，并能提升内容的“信息密度”与“保真度”。
- 文中给出的唯一可执行技术建议是支持 `prefers-contrast`，但没有附带 A/B 测试、可访问性评分提升或用户研究数字。

## Link
- [https://catskull.net/stop-using-grey-text.html](https://catskull.net/stop-using-grey-text.html)
