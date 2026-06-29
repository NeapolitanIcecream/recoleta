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
TestDecision 将单元测试生成视为一个序列决策问题，并训练一个开源 LLM 选择能为当前测试套件增加最多新价值的下一个测试。论文声称，这种贪心加强化学习的设置能提升覆盖率、执行成功率和缺陷发现能力，使一个 7B 模型在部分评测上达到 GPT-5.2 的水平。

## 问题
- 现有基于 LLM 的测试生成通常一次构建一个测试，但开源模型在根据测试套件已覆盖内容来选择下一个测试时表现较差。
- 这很重要，因为重复测试会浪费固定的测试预算，遗漏未覆盖分支，并降低缺陷发现能力。
- 论文认为，仅靠带反馈的提示并不能解决这个问题：在它的试点研究中，带引导的迭代在 ULT 上几乎没有比盲迭代带来提升。

## 方法
- 作者将测试套件生成建模为一个有限时域的马尔可夫决策过程，状态是当前测试套件的检查状态，每个动作是一个新测试用例。
- 他们证明，在这些假设下，套件效用目标是单调子模的，因此每一步选择边际增益最大的测试，可以得到经典的 \((1-1/e)\approx 63.2\%\) 最优近似界。
- TestDecision 在推理阶段使用这一思路：逐步生成测试，执行测试，更新覆盖率和其他反馈，然后继续选择能带来最大新增价值的下一个测试。
- 他们还用逐步强化学习训练基础 LLM，让模型学会生成更有效的测试，并对无效执行进行惩罚。
- 论文把开源模型的主要失败模式概括为“结构性视野狭窄”：模型能看到局部提示，但不能稳定地跨步骤规划套件层面的收益。

## 结果
- 在 ULT 基准上，TestDecision 在摘要中相对所有基础模型将分支覆盖率提高了 38.15% 到 52.37%；引言中报告的提升为 38.15% 到 65.87%。
- 在 ULT 上，执行通过率相对基础模型提高了 298.22% 到 558.88%。
- TestDecision 找到的缺陷比普通基础 LLM 多 58.43% 到 95.45%。
- 论文声称，一个 7B 骨干模型的表现可与专有的 GPT-5.2 相当。
- 它还声称在 LiveCodeBench 上有更好的分布外泛化能力，但摘录没有给出详细的 LiveCodeBench 数字。
- 在 TestDecision 之前的试点研究中，仅靠带引导的提示帮助很小：对 ULT 上的 Qwen2.5-Coder-7B，Iter-Blind 的行覆盖率是 52.43%，Iter-Guided 是 52.34%；分支覆盖率是 43.52% 对 43.49%；变异分数在两种设置下都保持在 33.81%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01799v1](http://arxiv.org/abs/2604.01799v1)
