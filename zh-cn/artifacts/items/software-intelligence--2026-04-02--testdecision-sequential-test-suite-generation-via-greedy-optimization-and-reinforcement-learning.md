---
source: arxiv
url: http://arxiv.org/abs/2604.01799v1
published_at: '2026-04-02T09:13:52'
authors:
- Guoqing Wang
- Chengran Yang
- Xiaoxuan Zhou
- Zeyu Sun
- Bo Wang
- David Lo
- Dan Hao
topics:
- test-generation
- reinforcement-learning
- code-llms
- software-testing
- submodular-optimization
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# TestDecision: Sequential Test Suite Generation via Greedy Optimization and Reinforcement Learning

## Summary
## 摘要
TestDecision 将单元测试生成视为一个序列决策问题，并训练开源 LLM 选择下一个能为当前测试套件带来最多新增价值的测试。论文称，这种“贪心 + 强化学习”的设置提升了覆盖率、执行成功率和找 bug 能力，足以让一个 7B 模型在部分评测中达到 GPT-5.2 的水平。

## 问题
- 现有基于 LLM 的测试生成通常一次构建一个测试，但开源模型很难根据测试套件已经覆盖的内容选出下一个合适的测试。
- 这很重要，因为重复测试会浪费固定的测试预算，漏掉未覆盖的分支，并降低找 bug 的能力。
- 论文认为，仅靠带反馈的提示并不能解决这个问题：在其预研实验中，在 ULT 上，引导式迭代相比盲迭代几乎没有提升，或者根本没有提升。

## 方法
- 作者将测试套件生成建模为一个有限时域的马尔可夫决策过程，其中状态是当前测试套件的检查状态，每个动作是一个新的测试用例。
- 他们证明，在其假设下，测试套件效用目标是单调子模的，因此每一步都选择边际收益最大的测试时，可以得到经典的 \((1-1/e)\approx 63.2\%\) 最优解近似界。
- TestDecision 在推理阶段使用这一思路：逐步生成测试，执行它们，更新覆盖率和其他反馈，并持续选择下一个能带来最大新增价值的测试。
- 他们还用逐步强化学习训练基础 LLM，让模型学会生成边际收益更高且可有效执行的测试，并对无效执行施加惩罚。
- 论文将开源模型的主要失败模式概括为“结构性短视”：模型能看到局部提示，但无法在多步过程中稳定地规划测试套件层面的收益。

## 结果
- 在 ULT 基准上，摘要称 TestDecision 相比所有基础模型将分支覆盖率提高了 38.15% 到 52.37%；而引言报告的是 38.15% 到 65.87%。
- 在 ULT 上，执行通过率相比基础模型提高了 298.22% 到 558.88%。
- TestDecision 找到的 bug 比原始基础 LLM 多 58.43% 到 95.45%。
- 论文称，一个 7B 主干模型可以达到与闭源 GPT-5.2 相当的性能。
- 论文还称其在 LiveCodeBench 上有更好的分布外泛化能力，但摘录中没有给出 LiveCodeBench 的详细数字。
- 在 TestDecision 之前的预研实验中，仅靠引导式提示几乎没有帮助：对于 ULT 上的 Qwen2.5-Coder-7B，Iter-Blind 与 Iter-Guided 的行覆盖率分别为 52.43% 和 52.34%，分支覆盖率分别为 43.52% 和 43.49%，两种设置下的变异分数都为 33.81%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01799v1](http://arxiv.org/abs/2604.01799v1)
