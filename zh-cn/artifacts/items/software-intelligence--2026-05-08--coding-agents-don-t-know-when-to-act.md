---
source: arxiv
url: https://arxiv.org/abs/2605.07769v1
published_at: '2026-05-08T14:10:00'
authors:
- Thibaud Gloaguen
- "Niels M\xFCndler"
- "Mark M\xFCller"
- Veselin Raychev
- Martin Vechev
topics:
- coding-agents
- software-maintenance
- code-intelligence
- swe-bench
- agent-evaluation
- abstention
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Coding Agents Don't Know When to Act

## Summary
## 摘要
编码代理经常修改已经修复的代码，而正确做法是保持代码不变。FixedBench 用 200 个 SWE-bench Verified 任务测试这种放弃修改的能力；这些任务的 golden patch 已经提前应用。

## 问题
- 自主维护代理会遇到过时或重复的 bug 报告；论文引用的既有研究称，重复报告可占 bug 报告的 49%。
- 如果代理给已经正确的代码打补丁，可能增加技术债，也会掩盖该问题是否已被验证。
- 现有编码基准主要奖励生成补丁，因此会漏掉提交无代码变更这一决策。

## 方法
- 作者通过选取 200 个 SWE-bench Verified issue，并在把任务交给代理前应用每个 issue 的 golden patch，构建了 FixedBench。
- 在 Resolved 任务中，正确输出是空的可执行代码补丁；对测试、注释和文档的修改在放弃修改评分中会被忽略。
- 他们在四种 agent harness 上测试了五个模型，包括 Sonnet-4.6、GPT-5.3 Codex、GPT-5.4 mini、Gemini-3 Pro 和 Qwen3.5-122B。
- 他们比较了多种提示：Issue、Edit、Reproduce、Abstain or Fix，以及带或不带 git 历史和就绪环境的 Best 与 Worst 场景。
- Partial 任务会对 150 个实例应用一个错误的先前补丁，用来测试放弃修改提示是否会导致代理跳过真正需要的修复。

## 结果
- 在使用 Issue 提示的主要 Resolved 设置中，代理在 35% 到 65% 的已修复案例中做出了不应出现的可执行代码修改。
- 在 Best 场景中，使用 Issue 提示时，Sonnet-4.6 的放弃修改率为 65.0%±6.6，GPT-5.4 mini 为 60.5%±6.8。
- Edit 提示降低了放弃修改率：GPT-5.4 mini 从 60.5% 降至 36.5%，Sonnet-4.6 从 65.0% 降至 56.5%。
- Abstain or Fix 提示在 Best 场景中提高了放弃修改率，Sonnet-4.6 达到 80.5%，GPT-5.4 mini 达到 88.5%；报告的提升分别为 15.5 个百分点（p=9.5e-3）和 28.0 个百分点（p=2.3e-8）。
- 单独使用 Reproduce 未能修正这种行为：Sonnet-4.6 从 65.0% 变为 65.5%，而 GPT-5.4 mini 从 60.5% 降至 47.5%。
- 在 Partial 任务上，同一个 Abstain or Fix 提示增加了错误放弃修改：GPT-5.4 mini 的错误放弃修改率为 93.6%±4.3，只解决了 2.9%±2.8 的案例；Sonnet-4.6 的错误放弃修改率为 81.3%±6.2，解决了 6.0%±3.8。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07769v1](https://arxiv.org/abs/2605.07769v1)
