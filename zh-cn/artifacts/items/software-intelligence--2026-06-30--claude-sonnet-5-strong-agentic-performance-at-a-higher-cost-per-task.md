---
source: hn
url: https://artificialanalysis.ai/articles/claude-sonnet-5-agentic-cost
published_at: '2026-06-30T23:35:07'
authors:
- himata4113
topics:
- llm-evaluation
- agentic-ai
- code-intelligence
- knowledge-work
- model-cost
- reasoning-benchmarks
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Claude Sonnet 5: strong agentic performance at a higher cost per task

## Summary
## 摘要
这项评估认为，Claude Sonnet 5 达到一线的 agentic 性能，知识工作和编码基准分数高于 Sonnet 4.6；同时，由于使用更多 token 和 agentic 轮次，单任务成本更高。

## 问题
- 前沿模型常按 token 价格比较，但 agentic 任务还取决于模型为完成任务消耗多少 token 和工具使用轮次。
- Anthropic 需要一个外部基准视角，用来比较 Claude Sonnet 5 与 Sonnet 4.6、Opus 4.8、GPT-5.5 及其他领先模型。
- 这个结果对使用模型做知识工作、编码和 agent 工作流的团队有影响，因为即使每 token 价格不变，更高能力也可能提高总任务成本。

## 方法
- Artificial Analysis 在 Claude Sonnet 5 发布前对其进行评估，并在 Artificial Analysis Intelligence Index 上打分。
- 评估比较了不同 effort 设置，包括 max effort 和新增的 xhigh 设置，以测量质量、token 使用量、轮次、与延迟相关的行为，以及单任务成本。
- 评估使用开源 Stirrup agent harness，通过 AA-Briefcase 和 GDPval-AA 测试 agentic 知识工作。
- 评估还报告了 CritPt、Terminal-Bench v2.1、Humanity’s Last Exam 和 SciCode 上的基准变化。

## 结果
- Claude Sonnet 5 在 Artificial Analysis Intelligence Index 上得分 53，比 Sonnet 4.6 高 6 分，与启用 high reasoning 的 GPT-5.5 持平，总体排名第 #5。
- 它比 GPT-5.5 xhigh 和 Claude Opus 4.8 max 低 2 到 3 个 Intelligence Index 分数点，并且在总体指数上仍落后于 Opus 4.7 和 Opus 4.8。
- 在 max effort 下，Sonnet 5 每个 Intelligence Index 任务使用的输出 token 比 Sonnet 4.6 多约 40%，在 AA-Briefcase 和 GDPval-AA 上的 agentic 轮次约为 3 倍。
- 在 GDPval-AA 上，max effort 使用的轮次约为 low effort 的 6 倍。
- 标准价格为每 1M 输入 token 3 美元、每 1M 输出 token 15 美元，与 Sonnet 4.6 相同；测得每个 Intelligence Index 任务成本为 2.29 美元，在促销价格前约为 Sonnet 4.6 的 2 倍，并比 Opus 4.8 高约 15%。
- 相比 Sonnet 4.6，报告的提升包括 Terminal-Bench v2.1 上 +9 分、Humanity’s Last Exam 上 +10 分、SciCode 上 +7 分，以及 CritPt 得分 17%，比 Sonnet 4.6 高 14 分。

## Problem

## Approach

## Results

## Link
- [https://artificialanalysis.ai/articles/claude-sonnet-5-agentic-cost](https://artificialanalysis.ai/articles/claude-sonnet-5-agentic-cost)
