---
source: hn
url: https://www.gopeek.ai
published_at: '2026-03-13T23:15:22'
authors:
- itsankur
topics:
- developer-tools
- coding-assistant
- preference-learning
- prompt-injection
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Simple plugin to get Claude Code to listen to you

## Summary
这不是一篇机器人或机器学习研究论文，而是一个面向 Claude Code 的插件宣传摘要。它声称通过自动学习用户偏好并在合适时机注入提示，让 Claude Code 更好地“听从”用户。

## Problem
- 现有用 markdown 文件手动约束 Claude Code 行为的方式据称效果有限，难以持续、准确地体现用户偏好。
- 如果编码助手不能稳定遵循个人工作习惯与指令，开发体验和输出一致性会受影响。
- 提供文本没有说明该问题的范围、评测设置或实际影响规模。

## Approach
- 核心机制是一个名为 Peek 的简单插件。
- 它声称会**自动学习用户偏好**，而不是只依赖用户手写的 markdown 说明文件。
- 然后在“合适的时间”把这些偏好注入给 Claude Code，以更好地引导其响应和行为。
- 从描述看，本质上是一个**偏好捕获 + 时机化提示注入**的辅助层，但没有公开技术细节。

## Results
- 提供内容**没有任何定量结果**，没有数据集、指标、基线或消融实验。
- 最强的具体主张是：Peek “比 markdown files 更能引导 Claude Code”。
- 还声称它能够“自动学习你的偏好”并“在正确时间注入”。
- 没有给出准确率、成功率、用户研究样本量、延迟、成本或与其他插件/方法的数值比较。

## Link
- [https://www.gopeek.ai](https://www.gopeek.ai)
