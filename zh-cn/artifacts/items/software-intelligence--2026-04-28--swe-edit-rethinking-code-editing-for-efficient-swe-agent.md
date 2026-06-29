---
source: arxiv
url: https://arxiv.org/abs/2604.26102v1
published_at: '2026-04-28T20:35:09'
authors:
- Yikai Zhang
- Jiaxin Pei
- Kenan Li
- Maoquan Wang
- Jin Pan
- Yu Kang
- Shengyu Fu
- Elsie Nallipogu
- Junjie Hu
- Yufan Huang
- Zijian Jin
topics:
- code-editing
- swe-bench
- coding-agents
- multi-agent-systems
- reinforcement-learning
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent

## Summary
## 总结
SWE-Edit 是一种代码代理设计，把文件查看和补丁编写拆成两个独立子代理，让主模型保留更干净的上下文，减少严格编辑格式带来的工作量。在 SWE-bench Verified 上，它声称比一个强的单体基线有更高的问题解决率、更好的编辑成功率和更低的推理成本。

## 问题
- 传统代码代理会在同一个上下文窗口里查看文件、规划修复并输出编辑结果，所以探索性读到的文件内容会留在上下文中，盖住真正相关的代码。
- 编辑格式会带来失败模式：find-and-replace 需要精确字符串匹配，whole-file rewrite 会消耗更多 token，也可能改到无关代码。
- 这很重要，因为 SWE 代理把大量预算花在仓库搜索和补丁应用上；上下文噪声和编辑格式失败会降低解决的问题数量，并抬高成本。

## 方法
- SWE-Edit 增加了一个 Viewer 子代理，它接收文件路径和自然语言查询，然后只返回与任务相关的代码块，而不是整份文件。
- 它还增加了一个 Editor 子代理，它接收文件路径和自然语言编辑指令，然后直接应用补丁，不让主代理去写精确的 find-and-replace 命令。
- 主代理仍然负责推理 bug 和修复方案，而在主实验中由 GPT-5-mini 处理查看和编辑。
- 在编辑器训练中，作者用 GRPO 微调 Qwen3-8B，让模型根据编辑请求在 find-and-replace 和 whole-file rewrite 之间选择。
- 奖励使用归一化匹配：先去掉注释，再规范化空白字符，用它来近似判断生成的编辑是否匹配目标。

## 结果
- 在包含 500 个问题、使用 3 次运行平均的 SWE-bench Verified 上，SWE-Edit 将 resolved rate 从 69.9% 提高到 72.0%，比基线高 2.1 个百分点。
- 总推理成本从 $243.7 降到 $200.1，减少 17.9%；同时 edit success 从 93.4% 提高到 96.9%，增加 3.5 个百分点。
- 单独的 Viewer 平均只返回请求文件内容的 39.7%，把代码覆盖面减少了 60.3%；在组合设置里，主代理的非缓存输入 token 从 276.7K 降到 181.3K。
- 在 50 个留出的 PR-Edit 样例上，与检索基线相比，LLM Viewer 的 recall 为 93.8%，F1 为 0.272；dense retrieval 的 recall 为 86.8%，F1 为 0.140；BM25 的 recall 为 53.7%，F1 为 0.083。
- 在 100 个 SWE-bench Verified 实例上，换用其他主推理模型时，SWE-Edit 让 Kimi K2 Thinking 的 resolved rate 提高 2.7 个百分点，让 MiniMax-M2.1 提高 4.1 个百分点，让 GLM-4.7 提高 1.6 个百分点；edit success 的增幅在 12.8 到 18.3 个百分点之间。
- GRPO 让 Qwen3-8B 在 PR-Edit 上的 format success 从 76.8% 提高到 90.4%，GPT Grader accuracy 从 56.0% 提高到 68.4%，normalized match 从 32.0% 提高到 38.8%；作为 SWE-bench Verified 上的编辑器时，它把 resolved rate 从 68.5% 提高到 69.9%，把 edit success 从 68.6% 提高到 81.1%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26102v1](https://arxiv.org/abs/2604.26102v1)
