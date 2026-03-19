---
source: hn
url: https://excipio.tech/blog/the-hype-beast-crisis/
published_at: '2026-03-15T22:57:03'
authors:
- lvales
topics:
- ai-security-reports
- vulnerability-analysis
- llm-hallucination
- open-source-security
- security-hype
relevance_score: 0.79
run_id: materialize-outputs
language_code: zh-CN
---

# The Hype-Beast Crisis

## Summary
这篇文章并非学术论文，而是一篇技术评论/反驳文。作者通过追踪 Mattermost 一则被 AI 生成报告标记为“严重漏洞”的代码路径，论证该 XSS 报告在当前实现下实际上不可触发，并进一步批评 AI 安全报告的炒作与低质量泛滥。

## Problem
- 文章要解决的问题是：一个由 LLM 生成并传播的“Mattermost 存在严重 XSS 漏洞”的安全结论是否真实，以及这种未经验证的 AI 安全报告为何有害。
- 这很重要，因为错误的高危漏洞声明会浪费开源项目维护者与安全团队时间，污染漏洞披露/赏金流程，并误导公众对 AI 代码与 AI 安全分析能力的认知。
- 作者还关注更广泛的问题：AI 驱动的“安全发现”如果缺乏人工验证，会制造虚假紧迫感和行业噪音。

## Approach
- 作者从被指控的 Mattermost 函数 `prepareTextForEmail` 入手，检查所谓 XSS 是否依赖错误分支 `return template.HTML(text)` 被执行。
- 然后沿调用链向下分析 `utils.MarkdownToHTML()`、`goldmark.Convert()`、`renderer.Render()`，寻找唯一可能返回错误的位置。
- 核心机制非常简单：如果 markdown 转 HTML 的过程实际上不会报错，那么上层的错误处理分支就是死代码，未转义文本就永远不会从该路径返回。
- 作者进一步查看 `goldmark` 渲染流程，指出在该具体调用场景中，`nodeRendererFuncs` 不会产生错误，因此 `Render()` 不会失败，进而整条“可触发 XSS”链条不成立。
- 最后，作者将这一技术核查放到社会层面讨论，认为这是典型的“AI 先猜测、人大肆传播、却不验证”的安全报告炒作模式。

## Results
- 文章的核心结论是定性的：当前实现下，`prepareTextForEmail()` 中相关 `err` 分支“始终为 nil”，因此被指控的 XSS 利用路径不可达；作者直接称其为“dead code”。
- 作者声称：`MarkdownToHTML()` 唯一可能失败的位置是 `md.Convert()`，而 `Convert()` 又只会从 `Render()` 传播错误；在该场景下，`Render()` 实际上“never returns an error”，所以漏洞报告不成立。
- 没有提供实验数据、基准测试或标准数据集上的量化指标，因此不存在可报告的 accuracy / recall / benchmark 数字。
- 最强的具体技术主张是：这不是一个“critical vulnerability”，最多只是一个潜在未来风险——如果未来 `goldmark` 改变行为、使该错误路径可触发，才可能形成真实漏洞。
- 文章还给出一个工程建议：即便当前不可触发，错误分支也应返回 `template.HTML(escapedText)` 而不是未转义的 `text`，以避免未来回归风险。

## Link
- [https://excipio.tech/blog/the-hype-beast-crisis/](https://excipio.tech/blog/the-hype-beast-crisis/)
