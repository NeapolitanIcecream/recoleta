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
编码代理经常会在代码已经修复后仍去修改它们，而它们本该保持不变。FixedBench 用 200 个 SWE-bench Verified 任务测试这种“保持不动”的能力，这些任务里 golden patch 已经提前应用。

## 问题
- 自主维护代理会遇到过时或重复的 bug 报告；论文引用的先前工作说，重复报告可能占 bug 报告的 49%。
- 如果代理去补丁一个已经正确的代码，它会增加技术债，也会掩盖问题是否已经被验证。
- 现有编码基准主要奖励生成补丁，缺少对“提交零代码改动”这个决策的考察。

## 方法
- 作者构建 FixedBench 的方式，是取 200 个 SWE-bench Verified 问题，并在把任务交给代理之前先应用每个问题的 golden patch。
- Resolved 任务里的正确输出是一个空的可执行代码补丁；为了评估是否应当保持不动，测试、注释和文档的改动都不计入评分。
- 他们在四种 agent harness 上测试了五个模型，包括 Sonnet-4.6、GPT-5.3 Codex、GPT-5.4 mini、Gemini-3 Pro 和 Qwen3.5-122B。
- 他们比较了几种提示：Issue、Edit、Reproduce、以及 Abstain or Fix，还比较了带或不带 git 历史和可直接运行环境的 Best 与 Worst 场景。
- Partial 任务给 150 个实例先加上一个错误的前置补丁，用来测试“保持不动”提示是否会让代理跳过真正需要的修复。

## 结果
- 在主 Resolved 设置和 Issue 提示下，代理在 35% 到 65% 的已修复案例中仍然做出了不该有的可执行代码改动。
- 在 Best 场景中，Sonnet-4.6 在 Issue 提示下的保持不动率为 65.0%±6.6，GPT-5.4 mini 为 60.5%±6.8。
- Edit 提示降低了保持不动率：GPT-5.4 mini 从 60.5% 降到 36.5%，Sonnet-4.6 从 65.0% 降到 56.5%。
- Abstain or Fix 提示在 Best 场景中把保持不动率提高到 Sonnet-4.6 的 80.5% 和 GPT-5.4 mini 的 88.5%；报告的提升分别是 15.5 个百分点（p=9.5e-3）和 28.0 个百分点（p=2.3e-8）。
- 单独使用 Reproduce 并没有修正这种行为：Sonnet-4.6 从 65.0% 变到 65.5%，GPT-5.4 mini 从 60.5% 降到 47.5%。
- 在 Partial 任务上，同一个 Abstain or Fix 提示增加了错误的保持不动：GPT-5.4 mini 错误保持不动的比例为 93.6%±4.3，只正确修复了 2.9%±2.8 的案例；Sonnet-4.6 错误保持不动的比例为 81.3%±6.2，正确修复了 6.0%±3.8。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07769v1](https://arxiv.org/abs/2605.07769v1)
