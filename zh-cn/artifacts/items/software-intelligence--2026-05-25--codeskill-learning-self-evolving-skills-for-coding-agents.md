---
source: arxiv
url: https://arxiv.org/abs/2605.25430v1
published_at: '2026-05-25T05:12:49'
authors:
- Yanzhou Li
- Yiran Zhang
- Xiaoyu Zhang
- Xiaoxia Liu
- Yang Liu
topics:
- coding-agents
- skill-learning
- procedural-memory
- reinforcement-learning
- software-engineering-agents
- swe-bench
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# CODESKILL: Learning Self-Evolving Skills for Coding Agents

## Summary
## 总结
CODESKILL 训练一个小型 LLM，把编码代理的轨迹转成可复用技能，并维护一个紧凑的技能库。作者声称，它能在不改动编码代理本身的情况下，提高冻结式编码代理的通过率。

## 问题
- 编码代理在修复仓库或使用终端时会留下很长的操作轨迹，但原始轨迹太大，也太依赖具体任务，不能直接复用。
- 现有的技能和记忆方法常用固定提示词或手写更新规则，因此会保留质量差、重复或过于特定的知识。
- 这很重要，因为更好的技能库能提升后续的软件工程任务表现，同时让主编码模型保持冻结。

## 方法
- CODESKILL 从轨迹中学习一个技能管理策略。它输出操作，用来生成新技能、修改已有技能、添加候选技能、把它和另一条技能合并，或者删除它。
- 每条技能都是一段 markdown 指令，包含标题、触发条件和编码代理可以执行的步骤。
- 技能库里有面向任务层级的技能，用于更宽泛的修复流程，也有面向事件驱动的技能，用于命令失败、测试错误或重复失败模式等局部事件。
- 训练先从教师模型给出的监督目标开始，再使用 GRPO 强化学习。
- 强化学习奖励结合了基于评分标准的技能质量、基于验证器的执行改进，以及一个对齐分数，用来检查编码代理是否真的用了这条技能。

## 结果
- 在 Qwen3.5-35B-A3B 作为冻结编码策略时，CODESKILL 在 EnvBench-Python、EnvBench-Java、SWE-Bench Verified 和 Terminal-Bench 2 上的平均成功率达到 39.26；无技能基线为 29.57，最强的提示词或记忆基线为 35.25。
- 在同样设置下，平均解决实例步骤数降到 35.15；无技能基线为 44.12，最强的提示词或记忆基线为 36.99。
- 在 Qwen3.5-35B-A3B 上，各基准的成功率分别是：EnvBench-Python 18.60，对比无技能 6.98；EnvBench-Java 38.32，对比 27.10；SWE-Bench Verified 66.00，对比 57.33；Terminal-Bench 2 34.12，对比 25.88。
- 在 GPT-5.4-mini 作为冻结编码策略时，CODESKILL 的平均成功率达到 30.73；无技能基线为 21.80，最强的提示词或记忆基线为 27.86。
- 摘要报告称，相比无技能基线，平均通过率提升 9.69 个百分点；相比最强的基于提示词或记忆的基线，提升 4.01 个百分点，约等于 33% 和 11% 的相对提升。
- 在生命周期消融实验中，完整系统保留了 676 条技能；只做抽取的版本和抽取加演化的版本都保留了 1252 条技能，同时在 Qwen3.5-35B-A3B 设置下保持了 39.26 的平均成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.25430v1](https://arxiv.org/abs/2605.25430v1)
