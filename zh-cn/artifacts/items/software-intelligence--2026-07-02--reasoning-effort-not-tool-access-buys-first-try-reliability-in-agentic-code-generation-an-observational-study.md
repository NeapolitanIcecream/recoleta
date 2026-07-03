---
source: arxiv
url: https://arxiv.org/abs/2607.02436v1
published_at: '2026-07-02T17:08:21'
authors:
- Achint Mehta
topics:
- agentic-code-generation
- code-intelligence
- reasoning-effort
- software-evaluation
- human-ai-interaction
- coding-agents
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Reasoning effort, not tool access, buys first-try reliability in agentic code generation: an observational study

## Summary
## 摘要
研究发现，在代理式代码生成中，提高推理强度比提供浏览器测试工具访问更能改善首次成功可靠性。在对同一个回顾看板应用进行 90 次重复构建时，Playwright 增加了成本，却没有提高功能评分；xHigh 推理则明显减少了修复提示。

## 问题
- 团队常给编码代理添加浏览器测试工具和偏设计的提示，假设这些配置能产出更好的软件。
- 单次运行的编码代理对比会掩盖运行间差异，也会把模型选择与工具、提示和推理设置混在一起。
- 实际问题是成本：团队需要知道哪些代理设置能减少首次尝试后的人工修复工作。

## 方法
- 研究在同一个详细 OpenSpec 任务上运行了 90 个独立代理会话：构建一个 React/Vite 和 Node.js 实时回顾看板，包含 SQLite、WebSockets、Docker 部署、CSV 导出和文档。
- 每个输出按 14 项功能标准评分，最高 42 分。某项标准首次运行可用得 3 分，一次纠正提示后修好得 2 分，仍然损坏得 1 分。
- 研究在重复相同配置的同时，改变模型家族、代理运行框架、Playwright 工具访问、推理强度和设计提示使用情况。
- 视觉质量根据截图按 1 到 5 分单独评分，然后由人工评估者复核。
- 分析还跟踪了按标准划分的首次失败、会话成本、输出 token、缓存读取 token、模型耗时和新增代码行数。

## 结果
- 前沿模型家族的得分接近 42 分上限：Claude Opus 4.7 平均 41.3，Claude Opus 4.6 平均 40.7，Claude Sonnet 4.6 平均 41.0。Qwen 在 2 次运行中平均 30.5，分数为 24 和 37。
- 将 Claude Opus 4.7 从 High 推理提高到 xHigh 推理后，首次即满分的运行从 18 次中的 5 次（28%）升至 18 次中的 16 次（89%）。纠正提示从总计 16 条降至 3 条，中位成本根据条件上升 9% 到 29%。
- Docker 部署是主要缺陷：90 次运行中有 40 次（44%）首次失败。本地环境设置有 15 次首次失败，因此两个环境标准合计占 100 次首次标准失败中的 55 次。
- 在匹配对比中，Playwright 没有提高功能评分或可靠性。在 Opus 4.7 上，它使 High 强度下的中位成本增加 42%，使 xHigh 强度下的中位成本增加 68%；在 Opus 4.6 上，它让平均分保持在 40.6，同时使中位成本增加 27%。
- 工具成本主要来自上下文重复读取。在 Opus 4.7 网格中，启用 Playwright 后，缓存读取 token 在 High 强度下从 2.3M 增至 5.3M，在 xHigh 强度下从 2.3M 增至 7.0M。
- 设计提示改善了外观，但没有改善功能。完整设计提示运行的视觉质量平均为 5 分制的 4.5 分，简写提示运行平均为 4.7 分，未使用提示的 Claude Code 运行全部评为 3.0 分；使用设计提示的 40 次运行中有 11 次出现拖放功能首次失败，未使用提示的 45 次运行中有 5 次出现该问题。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02436v1](https://arxiv.org/abs/2607.02436v1)
