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
论文发现，在六个月内，由编码代理创建的文件比匹配的人类创建文件需要更少维护，但后续工作仍主要由人完成。AI 创建的文件更常被扩展功能，而不是修复漏洞。

## 问题
- 团队使用编码代理来添加代码，但对代理创建的文件合并后会发生什么，缺少证据。
- 这很重要，因为长期维护会抵消生产力收益，还会迫使人去修改自己没有写的代码。
- 以往研究主要测量生成时的质量或短期影响，对合并后的维护关注不足。

## 方法
- 该研究使用 AIDev 数据集，其中包含来自约 61,000 个仓库的 456,000 多个自治编码代理拉取请求。
- 研究通过 bot 提交者名称识别由 Claude Code、Cursor、GitHub Copilot 和 Devin 添加的文件，并排除 Codex，因为无法从提交记录验证所有权。
- 研究从 100 个星标超过 100 的仓库中抽样 508 个 AI 生成文件和 508 个匹配的人类生成文件。
- 研究跟踪这些文件到 2026 年 1 月 31 日的后续提交，为每个文件提供至少六个月的观察窗口。
- 研究比较了提交频率、文件大小变化百分比、基于 Conventional Commits Classification System 的提交类型，以及维护者是 bot 还是人。

## 结果
- 数据集包含 1,543 次针对 AI 生成文件的维护提交和 1,695 次针对人类生成文件的维护提交；首次创建文件的提交不计入。
- 在第一个月，AI 生成文件的提交次数大约只有人类生成文件的一半。论文报告称，在前六个月内，AI 生成文件的维护频率都更低。
- AI 生成文件每月变更的行数占比也小于人类生成文件，因此它们的维护改动通常相对文件大小更小。
- 对 AI 生成文件来说，最常见的维护类型是功能工作：1,543 次提交中有 336 次，占 21.78%。漏洞修复有 181 次，占 11.73%。
- 对人类生成文件来说，漏洞修复是最常见类型：1,695 次提交中有 284 次，占 16.76%。文档变更有 275 次，占 16.22%，功能工作有 256 次，占 15.10%。
- 人类完成了 1,543 次针对 AI 生成文件的提交中的 1,284 次，占 83.21%。AI 代理完成 259 次，占 16.79%；在针对人类生成文件的提交中，代理完成 1,695 次中的 119 次，占 7.02%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06464v2](https://arxiv.org/abs/2605.06464v2)
