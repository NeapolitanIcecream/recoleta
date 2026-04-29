---
source: arxiv
url: http://arxiv.org/abs/2604.21765v1
published_at: '2026-04-23T15:18:50'
authors:
- Hao Chen
- Arnab Phani
- Sebastian Schelter
topics:
- data-validation
- code-intelligence
- llm-for-code
- test-generation
- prompt-optimization
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# PrismaDV: Automated Task-Aware Data Unit Test Generation

## Summary
## 摘要
PrismaDV 生成的数据单元测试会同时使用数据集概况和下游任务代码，因此测试能贴合每个任务的真实假设。论文还提出了 SIFTA，这是一种提示词调优方法，可根据稀疏的测试执行结果和任务执行结果持续更新系统。

## 问题
- 现有数据验证工具，如 Deequ、TFDV 和 Great Expectations，主要检查数据样本，忽略了消费这些数据的代码。
- 这一缺口会带来两类问题：漏掉会破坏下游任务的任务特定数据缺陷，以及对任务其实可以处理的数据情况设置过严检查，从而产生误报。
- 手动编写和维护任务特定的数据测试成本很高，尤其是在同一个数据集会被许多下游服务使用、且这些服务还会随时间变化时。

## 方法
- PrismaDV 通过结合样本数据集和下游任务的源代码来构建任务特定测试。
- 它会分析数据，识别代码访问了哪些列和列组合，并追踪这些字段在程序中的流向。
- 它使用基于 LLM 的模块，把这些代码位置转换成明确的自然语言数据假设，并存入一个二部数据-代码假设图中，把列、推断出的假设和代码片段连接起来。
- 它再将该图转换为目标验证系统（如 Deequ 或 Great Expectations）中的可执行约束，然后过滤掉无效约束，以及任何在已知正确样本上已经失败的约束。
- SIFTA 利用稀疏的执行反馈持续改进提示词：它通过 failure-precision 信号跟踪哪些约束失败与下游任务失败同时出现，将其回溯到对应假设和代码，再把该信号用于提示词优化。

## 结果
- 论文报告了两个新基准：ICDBench，包含 63 个手工构造的约束发现案例；EIDBench，包含来自 5 个公共数据集的 60 个下游任务，以及每个数据集 25 个错误案例。
- PrismaDV 在 ICDBench 上比强基线高出 20 多个 F1 点。
- PrismaDV 在 EIDBench 上比任务无关和任务感知基线高出 26 多个 F1 点。
- 加入 SIFTA 后，学得的提示词优于手写提示词和通用提示词优化器生成的提示词。
- 这段摘录没有给出最终的精确 F1 数值、基线名称或按数据集划分的指标表，只给出了上述领先幅度。
- 作者还在文中所述的 GitHub 仓库公开了代码、基准和原型实现。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21765v1](http://arxiv.org/abs/2604.21765v1)
