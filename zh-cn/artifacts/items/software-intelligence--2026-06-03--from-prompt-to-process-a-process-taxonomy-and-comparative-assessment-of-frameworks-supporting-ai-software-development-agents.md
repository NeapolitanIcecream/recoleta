---
source: arxiv
url: https://arxiv.org/abs/2606.04967v1
published_at: '2026-06-03T14:49:15'
authors:
- Sanderson Oliveira de Macedo
topics:
- ai-software-development
- coding-agents
- multi-agent-software-engineering
- spec-driven-development
- process-taxonomy
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# From Prompt to Process: a Process Taxonomy and Comparative Assessment of Frameworks Supporting AI Software Development Agents

## Summary
## 摘要
本文提出了一个六维分类法，用于比较运行在 AI 编码代理之上的流程框架。研究发现，现有框架会通过工件、角色和审查来增强可追溯性，但没有哪个框架能同时把规范、上下文、角色、执行、验证和可移植性都覆盖好。

## 问题
- AI 编码代理可以规划、编辑文件、运行命令并反复迭代，但原始代理会话会丢失上下文、隐藏决策，让审查变难。
- 现有综述把代理、LLM 任务或代理内部机制分开归类；产品指南则按安装和功能比较工具。它们没有把支持框架当作软件工程流程来比较。
- 这个缺口很重要，因为团队需要一种方法来判断 AI 开发工作流是否保留规范、上下文、验证证据，以及跨代理的可移植性。

## 方法
- 论文把支持框架定义为一组结构化的工件、命令、角色、模板、工作流或策略，由已经在使用 AI 编码代理的开发者来使用。
- 研究采用定向定性检索，覆盖正式论文、官方文档、代码仓库、社区列表和公开工具对比。
- 纳入条件要求框架提供流程支持、建立在现有编码代理之上使用、排除代理本身或封闭式 IDE、并排除通用的代理构建 SDK。
- 牵引力筛选保留至少有 1,000 个 GitHub stars 且在过去 6 个月内至少有一次 push 的候选项，数据通过 2026 年 5 月 26 日至 28 日的 GitHub API 获取。
- 核心方法是一个覆盖 6 个流程维度的评分量表：规范、上下文、角色、执行、验证和可移植性。

## 结果
- 最终样本包含 6 个框架：GitHub Spec Kit、GSD、OpenSpec、BMAD Method、Spec Kitty 和 Reversa。
- 在筛选时报告的牵引力为：GitHub Spec Kit 106,786 stars，GSD 63,754，OpenSpec 51,404，BMAD Method 48,209，Spec Kitty 1,273，Reversa 1,100。
- 该分类法被应用到 6 个入选框架，以及 1 个样本外案例 Spec-Flow。Spec-Flow 有 85 个 stars，因为牵引力较低被排除。
- 论文给出的主要比较结论是：没有任何框架能强力覆盖全部 6 个维度。
- 研究识别出流程深度与跨代理可移植性之间的权衡：工件和控制更丰富的框架，往往更依赖特定约定、工具或平台。
- 论文没有报告针对完整开发流程的独立定量性能基准。它最明确的具体结论是 6 维分类法、可审计的筛选标准、对 6 个高牵引力框架的比较，以及对规范与代码漂移、对生成工件过度信任、社区扩展脆弱、平台依赖和缺少基准这些风险的归纳。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04967v1](https://arxiv.org/abs/2606.04967v1)
