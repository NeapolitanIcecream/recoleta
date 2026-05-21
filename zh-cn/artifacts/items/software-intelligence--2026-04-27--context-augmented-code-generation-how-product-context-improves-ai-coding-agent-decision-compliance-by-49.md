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
## 摘要
本文测试产品上下文是否能帮助 AI 编码代理遵循源代码中不存在的团队决策。在一个包含 8 个任务的基准上，Claude Code + Brief 将加权决策遵循率从 46% 提高到 95%；作者也承认其中存在工作流混杂因素。

## 问题
- AI 编码代理可以生成能够编译的代码，但会漏掉存放在规格说明、wiki、审计记录和产品工具中的产品决策。
- 这会带来合规失败、使用已弃用 UI、错误的功能开关，或需要人工返工的变更。
- SWE-bench 等现有代码基准关注问题解决能力，不评分代码是否遵循团队特定的产品决策。

## 方法
- 论文将决策遵循定义为针对任务特定易错点的加权通过/失败得分，例如必需的审计日志、获批准的 UI 组件、功能开关、ORM 选择和认证包装器。
- 该基准使用一个名为 Prism Analytics 的洁净室 Next.js 14 应用，包含 8 个真实感任务、41 个加权决策点、15 个预置产品决策、3 个用户画像、5 个客户信号和 3 个竞争对手资料。
- 基线是仅能访问代码库的 Claude Code，使用 Claude Sonnet 4.6 生成代码。
- 增强设置加入 Brief，在规格生成和构建中咨询阶段检索已记录的决策、用户画像、客户信号和竞争上下文；Opus 4.6 负责规划，Sonnet 4.6 负责代码生成。
- 评分对 git diff 使用正则检查并加入人工审查；每个任务、每种设置独立运行 3 次，总计 48 次运行。

## 结果
- Claude Code 的决策遵循得分为 19/41，即 46%；Claude Code + Brief 提高到 39/41，即 95%，增加 49 个百分点。
- Claude Code + Brief 在 6/8 个任务上达到 100% 遵循率；Claude Code 为 2/8；0% 的任务从 2/8 降到 0/8。
- 阻断性违规从 5 次降到 0 次，已弃用模式使用从 3 次降到 0 次，`any` 类型数量从 9 个降到 0 个。
- 可合并任务从 2/8，即 25%，增加到 8/8，即 100%；每个可合并任务的成本从 2.07 美元降到 0.66 美元，下降 68%，但总成本从 4.13 美元升至 5.28 美元。
- 增强设置编写了 838 个测试，基线编写 0 个；两者的 lint 和 typecheck 通过率均为 100%，基线的测试通过率为 0%，增强设置为 100%。
- 证据受限于小规模洁净室基准、16 对 PR、一名人工审查者，以及一个混杂因素：Brief 同时改变了可用上下文和编码工作流，包括规格、验收标准和构建中指导。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08112v1](https://arxiv.org/abs/2605.08112v1)
