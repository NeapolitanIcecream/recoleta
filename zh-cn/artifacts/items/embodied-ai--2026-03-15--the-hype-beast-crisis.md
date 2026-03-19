---
source: hn
url: https://excipio.tech/blog/the-hype-beast-crisis/
published_at: '2026-03-15T22:57:03'
authors:
- lvales
topics:
- ai-security-reports
- xss-analysis
- static-code-review
- mattermost
- llm-hype
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# The Hype-Beast Crisis

## Summary
这篇文章并非学术论文，而是一篇技术评论与社会批评文章。作者通过代码追踪论证某个被AI标注为“严重漏洞”的Mattermost XSS报告实际上不可触发，并进一步批评AI生成安全报告的炒作文化。

## Problem
- 文章要解决的问题是：一个被宣称为 **CRITICAL** 的Mattermost邮件模板XSS漏洞是否真实存在，以及为什么错误的AI安全报告会造成实际危害。
- 这很重要，因为虚假的高危漏洞报告会浪费维护者时间、污染漏洞披露流程，甚至像文中提到的cURL案例一样破坏漏洞赏金机制。
- 更广泛地，作者关注的是AI炒作导致的错误认知：把未经验证的模型输出包装成“安全发现”或“AI优于人工”的证据。

## Approach
- 作者从Mattermost函数 `prepareTextForEmail` 入手，指出看似危险的分支是在Markdown转HTML失败时返回未转义文本。
- 然后逐层追踪调用链：`prepareTextForEmail -> MarkdownToHTML -> goldmark.Convert -> renderer.Render`，检查错误究竟能否发生。
- 核心机制非常简单：如果底层 `md.Convert()` 根本不会在该路径上返回错误，那么上层“未转义返回”的分支就是死代码，漏洞也就不可利用。
- 作者分析 `goldmark` 的 `Render()` 实现，认为在这里传入 `strings.Builder` 被包装为 `bufio.Writer` 后，唯一可能的报错来源是节点渲染函数，而在当前场景下这些函数不会返回错误。
- 因此其结论是：这是一个“理论上未来库行为变化后可能出现的问题”，但不是当前可触发的现实漏洞；正确修复虽应返回 `escapedText`，但现状不构成实际XSS。

## Results
- 文中最核心的技术结论是定性的：作者声称 `prepareTextForEmail()` 中的错误处理分支 **“always nil”**，即当前代码路径下 `err` 实际上始终为 `nil`，因此所谓XSS不可触发。
- 逐层结论链条是：`Render()` **never returns an error** → `Convert()` 不会报错 → `MarkdownToHTML()` 不会报错 → `prepareTextForEmail()` 的危险fallback为死代码。
- 没有提供实验数据、基准测试或标准安全指标；**文中无定量结果**，也没有CVSS、PoC成功率、数据集或对比实验。
- 最强的具体主张是：该报告不是“关键漏洞”，甚至不是当前真实漏洞；它最多是一个未来依赖行为变化时才可能暴露的潜在缺陷。
- 社会层面的结果性主张包括：AI生成的粗糙漏洞报告已经污染安全披露生态，作者以cURL关闭漏洞赏金计划作为相关案例，但未提供更多数字证据。

## Link
- [https://excipio.tech/blog/the-hype-beast-crisis/](https://excipio.tech/blog/the-hype-beast-crisis/)
