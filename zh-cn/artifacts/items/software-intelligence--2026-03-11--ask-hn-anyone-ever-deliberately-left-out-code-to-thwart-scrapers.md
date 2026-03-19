---
source: hn
url: https://news.ycombinator.com/item?id=47343587
published_at: '2026-03-11T23:00:08'
authors:
- truelinux1
topics:
- code-scraping
- open-source
- anti-scraping
- human-ai-interaction
relevance_score: 0.43
run_id: materialize-outputs
language_code: zh-CN
---

# Ask HN: Anyone ever deliberately left out code to thwart scrapers?

## Summary
这是一则关于开发者是否应故意在公开代码中留缺口以阻碍抓取机器人的讨论，而不是一篇正式研究论文。它提出了一个与开源分享、数据抓取和人与人互动消失相关的实践性问题。

## Problem
- 讨论的问题是：开发者是否应故意省略部分代码、依赖或关键实现，以降低被自动抓取和无署名复用的风险。
- 其重要性在于 GitHub 等平台上的代码正被持续大规模抓取，用于模型训练或再分发，而原作者可能得不到互动、署名或回馈。
- 核心张力在于：这种做法是否能有效表达立场或保护劳动成果，还是只是损害可复现性和正常协作的无效举动。

## Approach
- 文本没有提出正式方法，而是给出几种“人为留缺口”的简单机制：声明但不定义函数、不提供某个依赖、或在 README 中写“缺失部分请邮件联系我”。
- 这些做法的最简单理解是：让人类读者仍有机会通过沟通获取完整内容，但让自动化抓取和直接复用变得更困难。
- 它隐含的机制不是技术防护，而是通过增加人工交互门槛，迫使使用者从“直接抓取”转向“联系作者”。
- 文本同时质疑这种机制的有效性，认为它可能只是象征性姿态，而非真正可执行的反抓取策略。

## Results
- 没有提供任何定量实验结果、数据集、基线或指标比较。
- 没有报告这种“故意缺失代码”策略对抓取阻断率、人工联系率、项目采用率或社区反馈的具体数字。
- 最强的具体主张是：代码托管平台上的机器人“24/7”抓取代码，且当前环境相比过去“少了人与人的互动”。
- 文本未证明该策略有效，只是提出了可操作示例并请求社区判断其是否“coherent”或“pointless”。

## Link
- [https://news.ycombinator.com/item?id=47343587](https://news.ycombinator.com/item?id=47343587)
