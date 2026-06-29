---
source: arxiv
url: https://arxiv.org/abs/2605.22526v1
published_at: '2026-05-21T14:18:29'
authors:
- Zhao Tian
- Zifan Zhang
- Tao Xiao
- Dong Wang
- Masanari Kondo
- Junjie Chen
- Yasutaka Kamei
topics:
- coding-agents
- automated-software-engineering
- issue-resolution
- refactoring
- patch-quality
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# "Refactoring Runaway": Understanding and Mitigating Tangled Refactorings in Coding Agents for Issue Resolution

## Summary
## 摘要
这篇论文研究了用于 Java 问题修复的编码代理补丁中未经请求的重构，并表明这些改动常常会损害编译。论文提出了 RefUntangle 这一细化步骤，用来检查重构是否必要且安全，然后移除或修复有风险的操作。

## 问题
- 编码代理有时会把小的缺陷修复或功能改动扩展成大规模的结构性编辑，从而增加评审成本，并可能破坏构建。
- 现有的 SWE-bench 风格评估主要衡量测试是否通过，因此会遗漏补丁的结构质量和重构带来的副作用。
- 论文要回答的是，代理生成的重构与人类开发者的重构有何不同，以及它们是否会影响可编译性或问题修复成功率。

## 方法
- 研究使用 Multi-SWE-bench 的 Java 部分：128 个人工黄金补丁，以及由 3 个代理系统和 12 个 LLM 生成的 4,608 个补丁。
- 在补丁过滤并移除 2 个异常回滚补丁后，分析覆盖 3,691 个有效代理补丁。
- RefactoringMiner 3.0 用于检测人类补丁和代理补丁中的 tangled refactorings。
- 作者比较了不同代理、模型和人类补丁之间的重构频率、密度和类型多样性。
- RefUntangle 使用基于 LLM 的评估来判断每个重构是否必要且安全，然后选择性地移除或修复有问题的操作。

## 结果
- 代理补丁包含 tangled refactorings 的频率低于人类补丁：代理补丁中有 21.43%（791/3,691），而人类补丁中有 36.72%（47/128）。
- 代理补丁的重构密度低于人类补丁：每个补丁 0.66 个重构（2,429/3,691），而人类补丁为每个补丁 1.75 个（224/128）。
- 代理覆盖了更多重构类型：73 种不同类型，而人类补丁中是 46 种。
- 在各个代理系统中，SWE-agent 的 tangled-refactoring 比例最高，为 25.85%（371/1,435），OpenHands 最低，为 14.68%（154/1,049）。
- 逻辑回归发现，tangled refactorings 与较低的可编译性相关，但与功能正确性之间没有统计显著的关联。
- RefUntangle 将平均编译成功率从 19.34% 提高到 38.33%，并让 2.79% 之前未解决的补丁通过了全部测试。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22526v1](https://arxiv.org/abs/2605.22526v1)
