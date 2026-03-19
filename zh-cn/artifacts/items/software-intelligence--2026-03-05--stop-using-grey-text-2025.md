---
source: hn
url: https://catskull.net/stop-using-grey-text.html
published_at: '2026-03-05T23:15:57'
authors:
- catskull
topics:
- web-accessibility
- ui-design
- readability
- css
- human-ai-interaction
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Stop using grey text (2025)

## Summary
这是一篇关于网页可读性与可访问性的短文，核心主张是不要在浅色背景上使用低对比度灰色正文。作者认为这种常见设计会直接损害阅读体验，并且其实很容易通过更高对比度或 `prefers-contrast` 支持来避免。

## Problem
- 文章批评网页设计中常见的“灰字配灰白背景”做法，会显著降低正文可读性。
- 这会影响更广泛的用户，而不只是明确有视力障碍的人，因为低对比文本会让普通读者也更费力地阅读。
- 之所以重要，是因为设计者为了追求所谓“设计感”主动覆盖默认文字颜色，结果牺牲了信息传达与可访问性。

## Approach
- 核心方法很简单：不要把正文文本设成低对比度灰色，尤其不要放在偏白背景上。
- 如果出于风格原因一定要使用低对比配色，至少应支持 CSS 的 `prefers-contrast` 媒体查询，为需要更高对比度的用户恢复可读样式。
- 作者用最直白的机制解释问题：低对比会让文字信息像被压缩失真一样，降低“信息密度”和内容保真度。
- 文中还通过并列展示的“demo”来说明高对比文本与低对比文本在阅读体验上的明显差异。

## Results
- 文中**没有提供正式实验、数据集或量化指标**，因此没有可报告的准确数值结果。
- 最强的具体主张是：提高对比度会让内容“更高保真”、提升信息密度，并改善所有人的阅读体验，而不仅是有视力障碍的用户。
- 文章还给出一个明确的工程建议：使用 `prefers-contrast` 媒体查询作为补救方案，表明修复成本很低，“很容易”实现。
- 相比“灰字+灰白底”的设计基线，作者断言默认或更高对比度的文本显示会显著更易读，但未给出量化比较。

## Link
- [https://catskull.net/stop-using-grey-text.html](https://catskull.net/stop-using-grey-text.html)
