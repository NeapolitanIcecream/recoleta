---
source: arxiv
url: https://arxiv.org/abs/2605.08112v1
published_at: '2026-04-27T20:38:55'
authors:
- Drew Dillon
- Kasyap Varanasi
topics:
- code-generation
- coding-agents
- product-context
- retrieval-augmented-generation
- software-engineering-benchmarks
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%

## Summary
## 总结
这篇论文测试产品上下文是否能帮助 AI 编码代理遵守写在源代码之外的团队决策。在一个 8 个任务的基准上，Claude Code + Brief 将加权决策遵守率从 46% 提高到 95%，但作者也承认流程变化带来了混杂因素。

## 问题
- AI 编码代理可以生成能编译的代码，但仍会遗漏存放在规范、wiki、审计记录和产品工具中的产品决策。
- 这很重要，因为遗漏这些决策会造成合规失败、使用过时的 UI、错误的功能开关，或者需要人工返工的改动。
- 现有代码基准如 SWE-bench 关注的是问题修复，不会评分代码是否遵循团队特定的产品决策。

## 方法
- 论文把决策遵守定义为一种加权的通过/失败得分，用来衡量任务中的特定要求，例如必须有审计日志、批准的 UI 组件、功能开关、ORM 选择和 auth 包装器。
- 基准使用一个干净室 Next.js 14 应用 Prism Analytics，包含 8 个现实任务、41 个加权决策点、15 个预设产品决策、3 个 persona、5 个客户信号和 3 个竞品资料。
- 基线是只有代码库访问权限的 Claude Code，代码生成使用 Claude Sonnet 4.6。
- 增强方案加入 Brief，它在生成规范和构建中期咨询时检索已记录的决策、persona、客户信号和竞争上下文；Opus 4.6 负责规划，Sonnet 4.6 负责代码生成。
- 评分用 git diff 上的正则检查加人工复核完成，每个任务、每种设置各跑 3 次，共 48 次运行。

## 结果
- Claude Code 的决策遵守得分是 19/41，或 46%；Claude Code + Brief 提升到 39/41，或 95%，增加了 49 个百分点。
- Claude Code + Brief 在 8 个任务中有 6 个达到 100% 遵守率，Claude Code 只有 2 个；0% 的任务从 2/8 降到 0/8。
- 阻断性违规从 5 次降到 0 次，使用过时模式从 3 次降到 0 次，`any` 类型数量从 9 个降到 0 个。
- 可合并任务从 2/8（25%）增加到 8/8（100%）；每个可合并任务的成本从 $2.07 降到 $0.66，下降 68%，虽然总成本从 $4.13 增加到 $5.28。
- 增强方案写了 838 个测试，而基线写了 0 个；两种设置的 lint 和 typecheck 通过率都是 100%，但基线的测试通过率是 0%，增强方案是 100%。
- 证据受到几个限制：这个干净室基准规模很小，只有 16 对 PR，只有一位人工审稿人，而且存在一个混杂因素，Brief 同时改变了可用上下文和编码流程，包括规范、验收标准和构建中期指导。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08112v1](https://arxiv.org/abs/2605.08112v1)
