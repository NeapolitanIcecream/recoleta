---
source: arxiv
url: https://arxiv.org/abs/2607.05666v1
published_at: '2026-07-06T22:15:54'
authors:
- Illia Dovhoshliubnyi
- Nima Soroush
- Ashkan Sami
- Alexander Brownlee
topics:
- ai-coding-agents
- code-intelligence
- software-performance
- genetic-improvement
- mutation-taxonomy
- llm-as-judge
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# What Do AI Agents Actually Change? An Empirical Taxonomy of Mutation Patterns in Performance-Improving Pull Requests

## Summary
## 摘要
本文通过把代码 diff hunk 分类到突变类别，梳理 AI 编码代理在性能相关 pull request 中改了什么。核心结论是，代理身份和优化目标可以帮助为搜索式软件工程选择更小的一组突变算子。

## 问题
- AI 编码代理会提交生产 pull request，但其内部决策过程难以检查；可观察信号是它们修改的代码。
- 搜索式软件工程和遗传改进需要与真实代码变换匹配的突变算子，性能优化场景尤其如此。
- 性能 PR 在 AIDev-pop 中很少：33,596 个代理 PR 中有 324 个带性能标签，占比低于 1%。

## 方法
- 作者使用 AIDev-pop 中来自 Devin、GitHub Copilot、Cursor、OpenAI Codex 和 Claude Code 的 pull request，覆盖 100 个加星仓库。
- 他们将 324 个带性能标签的 PR 缩减为 280 个可获取 diff 的 PR、269 个源码 PR，以及 216 个含有已接受的性能相关 hunk 的 PR。
- 他们使用 Even-Mendoza 等人（2025）的 18 类句法突变分类法，对 1,254 个性能相关 diff hunk 进行分类。
- 两个 LLM 评审器 claude-sonnet-4-6 和 gpt-5.4 对每个 hunk 分类；完全一致则保留标签，部分一致则保留类别交集，完全不一致则丢弃。
- 简单说，该方法把每次代码修改当作证据，标注其编辑类型，然后按代理和优化策略比较标签模式。

## 结果
- 最高频的突变类别是 name_modification，占 1,254 个 hunk 的 37.0%；object_creation 占 26.4%，type_change 占 22.7%，control_flow 占 20.9%，statement_splitting 占 18.5%。
- 既有遗传改进数据中，no_change 占补丁的 84%；本语料中 no_change 为 0.0%，因此代理性能 PR 的突变画像不同。
- 在 Apriori 挖掘中，name_modification 和 type_change 共同出现，lift 为 3.07。
- 性能策略解释了部分模式：284 个 type_change 标签中有 253 个，即 89%，出现在 Data Structure 变更中；463 个 name_modification 标签中有 345 个，即 75%，出现在 Build & Infrastructure 变更中。
- 代理画像存在差异：Devin 在 670 个类别分配中有 361 个 name_modification 标签，Copilot 在 591 个中有 224 个 type_change 标签，Codex 在 574 个中有 136 个 control_flow 标签，Cursor 在 184 个中有 41 个 comment_modification 标签。
- 作者称，在遗传改进循环中，根据目标策略和代理进行条件化，可以把突变算子空间从 18 个类别缩减到约 5 个。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05666v1](https://arxiv.org/abs/2607.05666v1)
