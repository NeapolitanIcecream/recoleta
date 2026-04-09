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
## 摘要
GrandCode 是一个用于竞赛编程的多智能体强化学习系统。论文称，它是首个在多场 Codeforces 实时比赛中获得第一名、并领先所有人类选手的 AI 系统。

## 问题
- 竞赛编程对 AI 仍然很难，因为解法必须正确、高效，并且在实时比赛的时间压力下经得起隐藏测试用例的检验。
- 标准的单模型提示方法和常规强化学习，难以处理漫长的多阶段求解循环、延迟奖励，以及异步训练中的 off-policy drift。
- 这很重要，因为竞赛编程是检验代码推理、调试、验证和限时解题能力的强测试场景。

## 方法
- GrandCode 使用多个协同组件：负责推理和写代码的主求解器、用于提出猜想的假设模型、用于压缩长上下文的摘要模型，以及用于对抗性检查的测试用例生成器。
- 系统通过继续预训练、有监督微调、联合多组件强化学习，以及比赛期间的在线测试时强化学习来训练这些组件。
- 它的主要强化学习方法 Agentic GRPO 会在中间奖励到达时立刻更新策略，然后在最终奖励已知后再做一次后续修正。这个设计用于处理长智能体 rollout 中的延迟奖励问题。
- 在验证方面，系统会通过寻找能区分候选解的输入来生成对抗测试，在训练中用候选解与标准解互相攻击，并在提交前在线刷新测试池。
- 对于更难的问题，系统还会提出紧凑的假设，在小规模暴力实例上检查这些假设，并把通过验证的假设回填到求解器提示中。

## 结果
- 在 Codeforces Round 1087、1088 和 1089 的实时比赛中，GrandCode 三场都获得第 1 名，并且每次都是最先完成全部题目。
- 论文报告的实时比赛得分为：Round 1087：separate 9269，joint 8334，完成时间 00:51:11；Round 1088：separate 16511，joint 15008，完成时间 01:40:35；Round 1089：separate 11596，joint 9506，完成时间 00:56:43。
- 在 50 道真实 Codeforces 题目上，它的测试套件流程将通过数从基础测试套件下的 42/50，提高到加入 difference-driven generation 和 solution attack 后的 48/50，再到结合提交反馈和持续在线生成后的 50/50。
- 在一个包含 200 道题的假设生成评测中，Qwen-3.5-27B 的 pass@1 为 34%，pass@5 为 44%；+SFT 达到 45% 和 52%；+SFT+RL 达到 52% 和 57%。
- 论文还报告了一个涵盖 100 道题的前沿模型基准：Gemini 3.1 Pro 的 accept rate 为 75%，Level 5 上为 7/20；Claude Opus 4.6 为 73% 和 8/20；GPT-5.4 为 72% 和 7/20。这些数字为论文声称的提升提供了背景，但摘录中没有给出 GrandCode 在同一基准上的直接消融对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02721v1](http://arxiv.org/abs/2604.02721v1)
