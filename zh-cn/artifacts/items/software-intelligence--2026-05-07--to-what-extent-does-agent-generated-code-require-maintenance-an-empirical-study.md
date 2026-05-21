---
source: arxiv
url: https://arxiv.org/abs/2605.06464v2
published_at: '2026-05-07T15:52:41'
authors:
- Shota Sawada
- Tatsuya Shirai
- Yutaro Kashiwa
- Ken'ichi Yamaguchi
- Hiroshi Iwata
- Hajimu Iida
topics:
- agentic-coding
- software-maintenance
- ai-generated-code
- code-intelligence
- empirical-software-engineering
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# To What Extent Does Agent-generated Code Require Maintenance? An Empirical Study

## Summary
## 摘要
论文发现，在六个月内，由编码代理创建的文件比匹配的人类创建文件需要更少维护，但大部分后续工作仍由人类完成。AI 创建的文件更多被用于功能扩展，而不是修复错误。

## 问题
- 团队使用编码代理添加代码，但缺少证据说明代理创建的文件合并后会发生什么。
- 这很重要，因为长期维护可能降低生产率收益，并迫使人类编辑自己没有编写的代码。
- 以往工作主要衡量生成时质量或短期影响，对合并后的维护衡量不足。

## 方法
- 研究使用 AIDev 数据集，其中包含来自约 61,000 个代码库的 456,000 多个自主编码代理拉取请求。
- 研究通过机器人提交者名称识别由 Claude Code、Cursor、GitHub Copilot 和 Devin 添加的文件，并排除 Codex，因为无法从提交中验证所有权。
- 研究从 100 个星标超过 100 的代码库中抽样 508 个 AI 生成文件和 508 个匹配的人类生成文件。
- 研究跟踪截至 2026 年 1 月 31 日的创建后提交，使每个文件至少有六个月的观察窗口。
- 研究比较提交频率、文件大小变更百分比、使用 Conventional Commits Classification System 得到的提交类型，以及维护者是机器人还是人类。

## 结果
- 数据集包含 1,543 个针对 AI 生成文件的维护提交和 1,695 个针对人类生成文件的维护提交；初始文件创建提交被排除。
- 在第一个月，AI 生成文件收到的提交数量约为人类生成文件的一半。论文报告称，在前六个月中，AI 生成文件的维护频率较低。
- AI 生成文件每月变更的行数占比也小于人类生成文件，因此其维护变更相对于文件大小通常更小。
- 对于 AI 生成文件，最常见的维护类型是功能工作：1,543 个提交中有 336 个，占 21.78%。错误修复有 181 个提交，占 11.73%。
- 对于人类生成文件，错误修复是最常见类型：1,695 个提交中有 284 个，占 16.76%。文档变更有 275 个提交，占 16.22%；功能工作有 256 个提交，占 15.10%。
- 人类完成了针对 AI 生成文件的 1,543 个提交中的 1,284 个，占 83.21%。AI 代理完成 259 个提交，占 16.79%；在人类生成文件上，代理完成 1,695 个提交中的 119 个，占 7.02%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06464v2](https://arxiv.org/abs/2605.06464v2)
