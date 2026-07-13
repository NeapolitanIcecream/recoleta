---
source: arxiv
url: https://arxiv.org/abs/2607.09366v1
published_at: '2026-07-10T12:44:08'
authors:
- Shirley Yu
- Ruben Martins
topics:
- code-verification
- llm-code-generation
- program-synthesis
- formal-methods
- automated-software-production
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability

## Summary
## 摘要
Diversify2Verify 研究同一编程任务的不同实现是否更容易或更难通过自动演绎验证。在 73 个任务和 292 个 Why3 产物上，生成数组/列表以及递归/命令式变体后，产物验证率达到 52.7%，任务覆盖率达到 67.1%。

## 问题
- 完全验证的软件需要正确的实现、形式化契约，以及不变量和终止性论证等证明指导。
- 等价实现可能产生不同的证明义务，因此验证失败可能源于实现结构或缺少注释，也可能源于任务行为错误。
- 这一点会影响基于 LLM 的软件生产：可执行测试无法证明正确性，而一次性生成通常会同时处理规约、实现和证明修复。

## 方法
- 该流水线分为三个阶段：推断并验证表示特定的 Why3 契约，生成可执行实现，以及添加完整验证所需的证明注释。
- 对每个任务，系统生成四类变体：数组递归、数组命令式、列表递归和列表命令式。
- 契约通过后会被冻结。后续修复可以在指定类别内修改代码或证明注释，但不能弱化语义目标，也不能切换表示方式或控制结构。
- Why3 会检查契约、测试引理、可执行行为、安全性、终止性和函数正确性。该流水线采用有界修复，最多尝试五次实现，并进行两轮最终验证修复。

## 结果
- 基准包含 73 个任务和 292 个实现产物，覆盖整数、数组和列表。
- 初始有 96 个产物通过验证，产物级验证率为 32.9%；两轮修复后增加到 154 个，验证率达到 52.7%。
- 73 个任务中有 49 个至少有一个变体通过验证，任务级成功率为 67.1%。
- 单个表现最强的实现类别验证了 44 个任务，因此组合多个类别后，任务覆盖率高于任何单一类别。
- 研究显示，表示方式和控制结构会实质性地改变验证结果；但研究没有证明数组契约和列表契约在形式上等价，只能确认它们都针对同一基准层面的任务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09366v1](https://arxiv.org/abs/2607.09366v1)
