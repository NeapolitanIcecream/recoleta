---
source: arxiv
url: http://arxiv.org/abs/2604.02721v1
published_at: '2026-04-03T04:26:56'
authors:
- DeepReinforce Team
- Xiaoya Li
- Xiaofei Sun
- Guoyin Wang
- Songqiao Su
- Chris Shum
- Jiwei Li
topics:
- competitive-programming
- multi-agent-rl
- code-generation
- test-time-rl
- code-intelligence
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# GrandCode: Achieving Grandmaster Level in Competitive Programming via Agentic Reinforcement Learning

## Summary
## 概述
GrandCode 是一个用于竞赛编程的多智能体强化学习系统。论文声称，它是第一个在多场线下 Codeforces 比赛中拿到第一名、并且领先所有人类选手的 AI 系统。

## 问题
- 竞赛编程对 AI 来说仍然很难，因为解法必须在现场计时压力下保持正确、有效率，并且能应对隐藏测试用例。
- 传统的单模型提示和普通 RL 很难处理长链条的多阶段求解、延迟奖励，以及异步训练中的 off-policy drift。
- 这很重要，因为竞赛编程可以很好地检验代码推理、调试、验证和限时解题能力。

## 方法
- GrandCode 使用多个协作组件：用于推理和写代码的主求解器、用于提出猜想的假设模型、用于压缩长上下文的总结模型，以及用于对抗性检查的测试用例生成器。
- 这个系统通过继续预训练、监督微调、联合多组件 RL，以及比赛期间的在线测试时 RL 来训练这些组件。
- 其主要 RL 方法 Agentic GRPO 会在中间奖励一到达时立即更新策略，然后在最终奖励已知后再做一次后续修正。这样做是为了处理长时间 agent rollout 中的延迟奖励。
- 在验证阶段，它通过寻找能区分候选解的输入来生成对抗测试，在训练时让候选解和标准解对抗，并在提交前在线刷新测试池。
- 对于更难的问题，系统还会提出简短假设，在小规模暴力实例上检查这些假设，然后把已验证的假设回灌到求解器提示中。

## 结果
- 在线下 Codeforces Round 1087、1088 和 1089 中，GrandCode 三场都拿到了第 1 名，并且每次都最先完成所有题目。
- 论文报告的线下比赛分数如下：Round 1087：9269 separate，8334 joint，完成时间 00:51:11；Round 1088：16511 separate，15008 joint，完成时间 01:40:35；Round 1089：11596 separate，9506 joint，完成时间 00:56:43。
- 在 50 道真实 Codeforces 题上，测试集流水线把通过数从基础测试集的 42/50 提升到差分驱动生成加解法攻击后的 48/50，随后又通过提交反馈和持续在线生成提升到 50/50。
- 在一个 200 题的假设生成评测中，Qwen-3.5-27B 的 pass@1 为 34%，pass@5 为 44%；+SFT 达到 45% 和 52%；+SFT+RL 达到 52% 和 57%。
- 论文还报告了一个包含 100 道题的前沿模型基准：Gemini 3.1 Pro 的 accept rate 为 75%，Level 5 为 7/20；Claude Opus 4.6 为 73% 和 8/20；GPT-5.4 为 72% 和 7/20。这个结果可以作为论文所称提升的背景，但摘录里没有给出 GrandCode 在同一基准上的直接消融对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02721v1](http://arxiv.org/abs/2604.02721v1)
