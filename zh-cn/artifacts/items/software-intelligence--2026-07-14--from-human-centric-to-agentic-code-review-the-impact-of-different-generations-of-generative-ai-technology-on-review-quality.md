---
source: arxiv
url: https://arxiv.org/abs/2607.13196v1
published_at: '2026-07-14T18:48:20'
authors:
- Suzhen Zhong
- Shayan Noei
- Bram Adams
- Ying Zou
topics:
- agentic-code-review
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# From Human-Centric to Agentic Code Review: The Impact of Different Generations of Generative AI Technology on Review Quality

## Summary
## 摘要
本研究考察了在 207 个 GitHub 项目的 102 万个拉取请求中，LLM 和 AI 智能体的参与如何改变代码评审的效率与质量。涉及 AI 智能体的评审通常与更快的决策相关，但评审异味的出现率总体上升，因此证据并未显示质量得到一致改善。

## 问题
- 随着 AI 增加软件变更量，代码评审正日益成为瓶颈，但关于 LLM 辅助评审和智能体评审的实证证据仍然有限。
- 研究考察了哪些 AI 采用模式和人机协作模式与评审效率及质量风险相关。

## 方法
- 作者分析了来自不同项目、横跨三个项目特定阶段的已评审拉取请求：LLM 出现前的以人为中心的评审、LLM 辅助评审和智能体评审。
- 研究使用 soft-DTW 对按月归一化的 AI 评审者参与时间序列进行聚类，以识别常见的采用轨迹。
- 研究将评审讨论建模为由人工评审者、LLM 和 AI 智能体参与的序列，然后比较每千行代码（KLOC）的评审时长和六种评审异味，其中包括 Sleeping Review、Review Buddies、Large Changeset 和 Lack of Review。
- 逻辑回归模型在纳入拉取请求特征、评审活动和评审者经验的同时，评估人机协作的影响；研究使用 GPT-4.1-mini 对拉取请求类型进行分类，该模型在验证样本上的 Cohen's kappa 达到 0.91。

## 结果
- 数据集包含来自 2,490 个候选项目中筛选出的 207 个开源项目的 102 万个已评审拉取请求；AI 评审者行为被归为三种实践：渐进式 AI 采用（Gradual AI Adoption，占项目的 46%）、快速 LLM 采用（Rapid LLM Adoption，占 22%）和快速 AI 智能体采用（Rapid AI Agent Adoption，占 32%）。
- 在渐进式 AI 采用模式下，LLM 在 LLM 阶段评审了 8% 的拉取请求，智能体在智能体阶段评审了 36%；智能体阶段的归一化评审效率提高了 2.5 个单位，而总体评审异味出现率上升了 2.0 个百分点。
- 在快速 AI 智能体采用模式下，LLM 评审了 19% 的拉取请求，智能体评审了 76%；智能体阶段的效率提高了 4.5 个单位，而评审异味出现率上升了 2.5 个百分点。
- 快速 LLM 采用与较差的质量指标相关：LLM 阶段的评审异味出现率上升了 8.0 个百分点，智能体阶段上升了 4.4 个百分点；Review Buddies 的比例分别上升了 26.0 和 23.2 个百分点。
- 在渐进式 AI 采用和快速 AI 智能体采用模式下，由 AI 智能体发起或涉及多个智能体的评审显著快于仅由人工进行的评审，但大多数涉及 LLM 或智能体的模式相比仅由人工进行的评审具有更高的评审质量风险。
- 这些发现是基于项目特定阶段定义和评审异味代理指标的观察性相关结果；它们无法证明 AI 评审者导致了效率提升或质量风险。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13196v1](https://arxiv.org/abs/2607.13196v1)
