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
## 总结
USACOArena 是一个编码基准，会对代理的 token、测试和耗时收费，因此它们必须在正确性和成本之间权衡。论文认为，当前对编码代理的评估忽略了这一约束，而且即使是强模型，在预算管理上也表现不佳。

## 问题
- 现有编码基准只给最终正确性评分，通常不计 API 成本、本地测试成本和墙钟时间。
- 这个缺口对真实软件工作和多代理系统很重要，因为低效的搜索和协调会耗尽共享预算。
- 论文想衡量的是编码代理能否把有限资源分配好，而不只是能否在没有约束的环境里写出正确代码。

## 方法
- 作者构建了 **USACOArena**，这是一个交互式的、类似 ACM-ICPC 的环境，基于 2024–2025 USACO 赛季的 48 道题，每场 12 题。
- 每个代理拿到固定信用额度。信用会因 LLM 推理、提示/测试，以及通过系数 \(\alpha\) 计入的墙钟时间而消耗；错误提交也会增加罚分。
- 排名沿用 ICPC 规则：总分优先，消耗的信用作为平局判定，且更难的已通过题目分值更高。
- 代理通过轮流制的 MCP/JSON 协议交互，提交的代码会在沙箱化在线评测器中运行，以保证可复现性。
- 实验比较了前沿单代理、同构代理之间的自对弈，以及在相同预算规则下的早期多代理/群体设置。

## 结果
- 在四场比赛、每场 **5 次运行** 中，**Gemini-2.5-pro** 和 **GPT-5-Codex** 在仅计算成本、即 **\(\alpha=0\)** 的设置下，始终排在 **第一** 和 **第二**。
- 这个基准离饱和还很远：每场比赛的理论最高分是 **54 分**，而顶级代理平均只有大约 **15 分**。
- 在一对一画像中，**Gemini-2.5-pro** 的 **平均名次 1.3±0.47**、**胜率 70.0%**、**最高分 19**、**最低分 4**；**GPT-5-Codex** 的 **平均名次 1.7±0.47**、**胜率 30.0%**、**最高分 29**、**最低分 3**。
- 在提到的最难比赛 **USACO 2025 US Open** 中，**Gemini-2.5-pro** 得分 **14.6**，**GPT-5-Codex** 得分 **3.0**。
- 在自对弈中，论文报告了 **9 场** 同构 **gemini-2.5-pro** 代理之间的比赛，覆盖 **18 名参赛者**，方差很高，平局很少，而且更多信用消耗和更高分数之间没有简单关系。
- 在预算大小的消融实验中，把信用上限降到 **10M**，会让 **Gemini-2.5-pro** 的分数从 **13.2** 降到 **8.3**；把上限提高到 **40M**，性能仍接近 **13.0**。作者把这解读为：当前代理在成为预算受限之前，先受到能力上限限制。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10182v1](http://arxiv.org/abs/2604.10182v1)
