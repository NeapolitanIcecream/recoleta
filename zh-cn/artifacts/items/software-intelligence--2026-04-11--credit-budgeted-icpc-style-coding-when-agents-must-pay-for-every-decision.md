---
source: arxiv
url: http://arxiv.org/abs/2604.10182v1
published_at: '2026-04-11T12:22:10'
authors:
- Lingfeng Zhou
- Junhao Shi
- Jin Gao
- Dequan Wang
topics:
- coding-agents
- benchmarking
- resource-aware-agents
- competitive-programming
- multi-agent-systems
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Credit-Budgeted ICPC-Style Coding: When Agents Must Pay for Every Decision

## Summary
## 概要
USACOArena 是一个编程基准，会对智能体消耗的 token、测试和经过时间收费，因此智能体必须在正确性和成本之间权衡。论文认为，当前对编程智能体的评测忽略了这种约束，并表明即使是强模型，在预算管理上仍然做得很差。

## 问题
- 当前编程基准主要按最终正确性评分，通常忽略 API 成本、本地测试成本和实际经过时间。
- 这个缺口在真实软件工作和多智能体系统中很重要，因为低效的搜索和协作会耗尽共享预算。
- 这篇论文要衡量的不是编程智能体能否在无约束环境下写出正确代码，而是它们能否合理分配有限资源。

## 方法
- 作者构建了 **USACOArena**，这是一个交互式 ACM-ICPC 风格环境，基于 2024–2025 赛季 USACO 的 48 道题，每场比赛使用其中 12 道题。
- 每个智能体都有固定的 credit 预算。credit 会用于 LLM 推理、提示/测试，以及通过系数 \(\alpha\) 计入的实际经过时间；错误提交还会产生额外惩罚。
- 排名遵循 ICPC 风格规则：总分优先，消耗的 credit 作为平分条件，较难且通过的题目分值更高。
- 智能体通过基于回合的 MCP/JSON 协议交互，提交的代码会在沙箱化的在线评测系统中运行，以保证可复现性。
- 实验在相同预算规则下比较了前沿单智能体、相同智能体之间的自对弈，以及早期多智能体/群体设置。

## 结果
- 在四场比赛、**每场 5 次运行**中，**Gemini-2.5-pro** 和 **GPT-5-Codex** 在仅计算设置 **\(\alpha=0\)** 下稳定排名 **第一** 和 **第二**。
- 这个基准离饱和还很远：每场比赛的理论最高分是 **54 分**，而顶级智能体的平均得分大约是 **15 分**。
- 在一对一画像中，**Gemini-2.5-pro** 的 **平均排名为 1.3±0.47**、**胜率为 70.0%**、**最高分 19**、**最低分 4**；**GPT-5-Codex** 的 **平均排名为 1.7±0.47**、**胜率为 30.0%**、**最高分 29**、**最低分 3**。
- 在文中提到的最难比赛 **USACO 2025 US Open** 中，**Gemini-2.5-pro** 得分 **14.6**，**GPT-5-Codex** 为 **3.0**。
- 在自对弈中，论文报告了 **9 场**由相同 **gemini-2.5-pro** 智能体参与的比赛，共覆盖 **18 个参赛者**，结果方差很高、平局很少，而且更高的 credit 消耗与更高得分之间没有简单关系。
- 在关于预算规模的消融实验中，将 credit 上限降到 **10M** 后，**Gemini-2.5-pro** 的得分从 **13.2** 降到 **8.3**；将上限提高到 **40M** 后，表现仍接近 **13.0**。作者据此认为，当前智能体在受到预算限制之前，先受到能力上限限制。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10182v1](http://arxiv.org/abs/2604.10182v1)
