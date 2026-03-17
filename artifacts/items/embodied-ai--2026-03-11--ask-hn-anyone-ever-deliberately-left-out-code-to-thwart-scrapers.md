---
source: hn
url: https://news.ycombinator.com/item?id=47343587
published_at: '2026-03-11T23:00:08'
authors:
- truelinux1
topics:
- open-source
- web-scraping
- anti-scraping
- developer-community
relevance_score: 0.01
run_id: materialize-outputs
---

# Ask HN: Anyone ever deliberately left out code to thwart scrapers?

## Summary
这不是一篇研究论文，而是一则 Hacker News 讨论帖，提出是否应故意在公开代码中留缺口以干扰抓取机器人的问题。核心价值在于反映开源作者对自动化抓取、署名缺失与社区互动消失的担忧。

## Problem
- 讨论的问题是：开发者是否应故意省略部分代码、依赖或关键实现，以阻碍自动化抓取系统直接复制其工作成果。
- 其重要性在于帖子认为“bots scrape GitHub 24/7”，且抓取行为常缺乏致谢、互动或原本社区中的人为交流。
- 本质上这是一个关于开源发布策略、反抓取姿态与社区规范的社会技术问题，而非算法性能问题。

## Approach
- 文中没有提出正式研究方法，而是给出几种可能的做法：调用未定义函数、不包含某个依赖、或在 readme 中注明“缺失部分请邮件联系我”。
- 这些做法的共同机制很简单：故意让仓库无法直接完整运行，从而提高自动抓取与无互动复用的成本。
- 帖子进一步询问这种做法是否“coherent stance”还是“pointless gesture”，因此更像是开放性伦理/策略讨论，而非验证过的方法。

## Results
- 文本**没有提供任何定量实验结果**，没有数据集、指标、基线或对比方法。
- 唯一较具体的经验性主张是："bots scrape GitHub 24/7"，即作者认为代码托管平台存在持续高频的自动抓取现象，但未给出测量数字或证据来源。
- 没有报告故意留缺口是否真的降低抓取、增加署名、改善互动，或对正常用户造成多大负面影响。
- 因此，这段内容的最强结论只是：有人正在考虑把“不完整公开代码”作为一种反抓取姿态，但其有效性与合理性均未被实证证明。

## Link
- [https://news.ycombinator.com/item?id=47343587](https://news.ycombinator.com/item?id=47343587)
