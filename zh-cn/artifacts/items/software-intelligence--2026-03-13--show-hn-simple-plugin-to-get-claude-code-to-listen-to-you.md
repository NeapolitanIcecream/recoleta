---
source: hn
url: https://www.gopeek.ai
published_at: '2026-03-13T23:15:22'
authors:
- itsankur
topics:
- code-assistant
- developer-tools
- preference-learning
- prompt-injection
- human-ai-interaction
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Simple plugin to get Claude Code to listen to you

## Summary
这是一款面向 Claude Code 的简单插件，声称能自动学习用户偏好，并在合适时机注入提示，从而比静态 markdown 规则文件更好地引导代码助手行为。给定内容更像产品简介而非论文，因此技术细节和实证证据非常有限。

## Problem
- 代码助手往往难以持续“听懂”并遵循用户的个人偏好、工作方式和隐含规则。
- 仅依赖 markdown 文件来约束助手行为可能不够灵活，无法在正确上下文与时机生效。
- 这很重要，因为开发效率与生成质量高度依赖助手是否能稳定遵循用户意图。

## Approach
- 核心机制是：**自动学习用户偏好**，而不是要求用户手动维护大量规则说明。
- 然后在“合适的时机”把这些偏好**注入给 Claude Code**，以更精准地影响其响应与行为。
- 用最简单的话说：它像一个会记住你习惯的中间层，在你写代码时及时提醒 Claude Code 按你的方式做事。
- 产品还强调“5 行即可开始”，暗示集成方式较轻量，但未提供实现细节。

## Results
- 文本**没有提供定量结果**，没有数据集、评测指标、基线方法或消融实验。
- 最强的明确主张是：Peek “比 markdown files 更能引导 Claude Code”。
- 还声称其能力来自两点：**自动学习偏好** 与 **在正确时机注入偏好**。
- 未给出任何具体数字，如成功率提升、代码质量提升、延迟开销或用户研究结果。

## Link
- [https://www.gopeek.ai](https://www.gopeek.ai)
