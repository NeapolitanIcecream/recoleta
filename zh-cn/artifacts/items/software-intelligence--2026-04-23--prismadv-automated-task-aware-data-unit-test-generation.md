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
PrismaDV 会结合数据集概要和下游任务代码生成数据单元测试，让测试贴合每个任务的真实假设。论文还提出了 SIFTA，这是一种提示调优方法，会根据稀疏的测试和任务执行结果更新系统。

## 问题
- 现有的数据验证工具，如 Deequ、TFDV 和 Great Expectations，大多只检查数据样本，而忽略了消费这些数据的代码。
- 这种差距会导致两类失败：漏掉会破坏下游作业的任务特定数据错误，以及对任务其实可以处理的数据条件报出过严的误报。
- 手工编写和维护任务特定数据测试的成本很高，尤其是在一个数据集要供多个会随时间变化的下游服务使用时。

## 方法
- PrismaDV 通过把样本数据集和下游任务的源代码结合起来，为特定任务构建测试。
- 它会分析数据，检测代码访问了哪些列和列组合，并追踪这些字段在程序中的流向。
- 它使用基于 LLM 的模块，把这些代码位置转换成明确的自然语言数据假设，并把这些假设存到一个二部数据-代码假设图中，用列、推断出的假设和代码片段连接起来。
- 它再把这个图转换成目标验证系统中的可执行约束，例如 Deequ 或 Great Expectations，然后过滤掉无效约束，以及那些在已知良好样本上已经失败的约束。
- SIFTA 使用稀缺的执行反馈随时间改进提示：它跟踪哪些约束失败和下游任务失败同时出现，用 failure-precision 信号回溯到对应的假设和代码，再把这个信号送入提示优化。

## 结果
- 论文报告了两个新基准：ICDBench，包含 63 个手工构造的约束发现案例；以及 EIDBench，包含跨 5 个公共数据集的 60 个下游任务，每个数据集有 25 个错误案例。
- PrismaDV 在 ICDBench 上比强基线高出 20 多个 F1 点。
- PrismaDV 在 EIDBench 上比任务无关和任务感知基线高出 26 个 F1 点以上。
- 使用 SIFTA 后，学习得到的提示优于手写提示和通用提示优化器生成的提示。
- 摘录没有给出最终的精确 F1 数值、基线名称或按数据集划分的指标表，只给出了上述差距结论。
- 作者还在所述的 GitHub 仓库公开了代码、基准和一个原型实现。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21765v1](http://arxiv.org/abs/2604.21765v1)
