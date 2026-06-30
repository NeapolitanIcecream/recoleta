---
source: arxiv
url: https://arxiv.org/abs/2606.29957v1
published_at: '2026-06-29T08:35:15'
authors:
- Yifan Wu
- Zhuokai Zhao
- Songlin Li
- Ho Hin Lee
- Jiacheng Zhu
- Shirley Wu
- Tianhe Yu
- Serena Li
- Lizhu Zhang
- Xiangjun Fan
- Shengzhi Li
topics:
- coding-agents
- software-benchmarks
- multi-turn-evaluation
- user-simulation
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Together: Evaluating Coding Agents in Interactive User Sessions

## Summary
## 摘要
SWE-Together 是一个包含 109 个任务的基准，用重放的多轮用户会话测试编码智能体，而不只使用一次性任务提示。它同时衡量最终仓库正确性，以及智能体需要多少纠正性用户反馈。

## 问题
- 大多数编码智能体基准会在开始时给出完整任务，并且只评分最终代码；真实用户会在多轮交互中澄清目标、添加约束并纠正错误。
- 这一点很重要，因为两个智能体可能达到相近的最终代码质量，但需要的用户投入差异很大。
- 真实会话日志很难直接用于基准测试，因为很多日志缺少可复现的仓库状态、清晰目标，或可检查的本地结果。

## 方法
- 作者从 11,260 条记录的用户-智能体编码会话中筛选出 109 个仓库级任务，这些任务有可恢复的提交、清晰的用户目标和可在本地检查的结果。
- 每个任务以原始用户的首次请求开始，并在固定沙箱中恢复仓库。
- 一个基于状态条件的 LLM 用户模拟器会观察被评估智能体的轨迹，并且只在原始会话中的触发条件适用时发送反馈。
- 最终代码使用确定性验证器证据和固定的逐任务评分规则来评分，评分对象是最终仓库状态。
- 该基准还报告 User Correction，它统计显式纠正加上 0.2 倍的较轻提示；还报告 Intent Coverage，用于检查模拟器消息是否与原始用户意图保持一致。

## 结果
- 最终套件包含从 11,260 条原始会话中得到的 109 个任务，转换率为 0.97%。来源包括 DataClaw 29 个任务、Pi-staging 23 个、Hyperswitch 9 个，以及 SWE-chat 48 个。
- 研究使用 opencode harness 评估了 7 个前沿模型，每个任务运行 2 次重复实验，并将 judge score >= 0.85 作为成功阈值。
- Claude Opus 4.8 在被评估智能体中领先，pass@1 为 63%，stable solve rate 为 59%，pass² 为 52%，mean judge score 为 0.801，mean User Correction 为 1.38。
- GPT-5.5 按 mean judge score 排名第二，pass@1 为 58%，stable solve rate 为 55%，pass² 为 48%，mean judge score 为 0.763，User Correction 为 1.59。
- 参考补丁基线的 pass@1 约为 78%，因此表现最好的被评估智能体比它低约 15 个百分点。
- 在 7 个模型中，User Correction 与能力呈强负相关：与 pass@1 的 Pearson 相关系数为 -0.92，与 stable solve rate 的 Pearson 相关系数为 -0.84。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.29957v1](https://arxiv.org/abs/2606.29957v1)
