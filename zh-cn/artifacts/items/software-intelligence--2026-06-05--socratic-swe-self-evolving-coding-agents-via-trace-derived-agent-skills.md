---
source: arxiv
url: https://arxiv.org/abs/2606.07412v1
published_at: '2026-06-05T16:00:17'
authors:
- Chuan Xiao
- Zhengbo Jiao
- Shaobo Wang
- Wei Wang
- Bing Zhao
- Hu Wei
- Linfeng Zhang
- Lin Qu
topics:
- software-engineering-agents
- code-intelligence
- self-evolving-agents
- synthetic-training-data
- reinforcement-learning
- swe-bench
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Socratic-SWE: Self-Evolving Coding Agents via Trace-Derived Agent Skills

## Summary
## 摘要
Socratic-SWE 通过把编码代理过去在仓库中的求解轨迹转成技能，来指导下一批合成修复任务。论文报告，在相同的 36k 任务训练预算下，它在 SWE-bench 和 Terminal-Bench 上的通过率高于自演化基线。

## 问题
- 高质量的软件工程训练任务很稀缺，而静态的漏洞注入流程无法跟上代理当前的失败模式。
- SWE 代理会产生包含搜索、编辑、命令、测试、失败和修复的丰富轨迹，但很多训练方法只把这些轨迹压缩成奖励，剩下的内容都丢掉了。
- 这很重要，因为当求解器变强后，固定的任务池能提供的有效信号会变少，训练增益可能放缓或停住。

## 方法
- 系统收集真实仓库任务中的成功和失败求解轨迹。
- 一个蒸馏模型把重复的失败模式和有用的修复模式转成结构化技能，包含名称、描述、适用条件和按顺序的操作。
- 生成器用这些技能在真实仓库中创建有针对性的修复任务，并用测试或命令作为验证器。
- 每个任务在用于训练前，都要通过格式、仓库锚定、执行稳定性和语义检查。
- 当某个任务的求解器更新与留出的验证集梯度对齐时，生成器会得到奖励；求解器使用 GDPO 训练，奖励包括完整通过、部分修复和避免回归。

## 结果
- 经过 3 轮迭代和 36k 个已验证训练实例后，Socratic-SWE 在 SWE-bench Verified 上达到 50.40%，在 SWE-bench Lite 上达到 36.67%，在 SWE-bench Pro 上达到 22.85%，在 Terminal-Bench 2.0 上达到 14.61%。
- 与 Qwen3.5-9B 基础代理相比，它在 SWE-bench Verified 上提高了 +7.80 个百分点，在 Lite 上提高了 +7.00 个百分点，在 Pro 上提高了 +5.61 个百分点，在 Terminal-Bench 2.0 上提高了 +4.50 个百分点。
- 四个基准的平均分是 31.13%，基础代理为 24.91%，提升了 +6.22 个百分点。
- 在 SWE-bench Verified 上，最强基线 SSR 在 3 轮后提升 +4.40 个百分点，而 Socratic-SWE 提升 +7.80 个百分点。
- 在 SWE-bench Verified 的 5 轮扩展实验中，Socratic-SWE 达到 52.00%，SSR 达到 48.00%。
- 在 SWE-bench Verified 第 3 轮的消融实验中，去掉轨迹蒸馏后降到 48.00%，把 GDPO 换成 GRPO 后降到 48.60%，完整系统为 50.40%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07412v1](https://arxiv.org/abs/2606.07412v1)
