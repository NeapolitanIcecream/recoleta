---
source: hn
url: https://github.blog/changelog/2026-07-20-github-code-quality-is-now-generally-available/
published_at: '2026-07-20T23:45:53'
authors:
- andsoitis
topics:
- code-intelligence
- software-quality
- ai-assisted-development
- code-analysis
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# GitHub Code Quality is now generally available

## Summary
## 摘要
GitHub Code Quality 已在 GitHub Enterprise Cloud 和 GitHub Team 上正式发布，作为一款付费产品，用于检测拉取请求中的可维护性、可靠性和测试覆盖率问题。它结合确定性的 CodeQL 分析、AI 辅助检测和 Copilot Autofix，帮助团队在合并前审查并处理质量问题。

## 问题
- AI 生成的代码增加了团队需要审查的代码量，使可维护性和可靠性问题更难在发布前被发现。
- 团队需要将质量检查和覆盖率阈值集成到拉取请求中，以便交付值得信赖的代码。

## 方法
- 将 CodeQL 的确定性分析与 AI 辅助检测结合起来，用于发现可维护性和可靠性问题。
- 使用 Copilot Autofix 提出修复建议，由开发者在合并前进行审查。
- 提供组织级仪表板、根据 Cobertura XML 报告生成的拉取请求覆盖率指标，以及通过 GitHub rulesets 实现的质量门禁。
- 提供用于启用仓库和获取发现结果的 API，并通过评估模式支持渐进式发布。

## 结果
- 在 GitHub 自己的工程组织中，团队会在合并拉取请求前解决 67.3% 的 Code Quality 发现的问题。
- 在公开预览期间，有超过 10,000 家企业使用了 Code Quality。
- 正式发布于 2026 年 7 月 20 日开始，面向 GitHub Enterprise Cloud 和 GitHub Team；发布时尚未支持 GitHub Enterprise Server。
- 定价为每位活跃提交者每月 10 美元，另加按用量计费的 AI 辅助工作费用，以及运行 CodeQL 分析所产生的 GitHub Actions 计算费用。
- 摘要提供了采用情况和内部问题解决率，但没有提供独立基准测试或与其他代码质量工具的比较。

## Problem

## Approach

## Results

## Link
- [https://github.blog/changelog/2026-07-20-github-code-quality-is-now-generally-available/](https://github.blog/changelog/2026-07-20-github-code-quality-is-now-generally-available/)
