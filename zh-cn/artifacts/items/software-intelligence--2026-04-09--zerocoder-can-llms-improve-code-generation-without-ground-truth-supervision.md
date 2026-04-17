---
source: arxiv
url: http://arxiv.org/abs/2604.07864v1
published_at: '2026-04-09T06:24:54'
authors:
- Lishui Fan
- Mouxiang Chen
- Tingwei Zhu
- Kui Liu
- Xin Xia
- Shanping Li
- Zhongxin Liu
topics:
- code-generation
- test-generation
- reinforcement-learning
- self-supervision
- program-synthesis
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?

## Summary
## 摘要
ZeroCoder 同时训练模型写代码和生成测试，不需要人工编写的测试或参考答案。它利用模型自己生成的代码与测试之间的执行结果构造奖励，再通过共同演化同时提升这两个角色的能力。

## 问题
- 代码生成中的标准强化学习通常需要人工编写的单元测试，或基于参考答案构造的测试，这类监督成本高，也难以扩展。
- 只依赖模型自生成的测试通常效果较弱，因此错误代码也可能通过测试，奖励信号会变得嘈杂。
- 论文要回答的问题是：LLM 是否能在完全没有真实监督的情况下，仅依靠代码与测试的执行反馈提升代码生成能力。

## 方法
- ZeroCoder 让同一个模型在两种提示角色下工作：**coder** 负责采样候选程序，**tester** 负责为同一道题采样候选测试。
- 它会执行每个候选程序与每个候选测试的组合，构造一个通过/失败矩阵，然后使用 MaxPass、CodeT 或 **B^4** 这样的选择器，挑出一个在共识下看起来较好的解和测试集合。
- coder 因被选入共识解集合而获得奖励。tester 的奖励则来自生成可执行的测试，这些测试既要能在一个代理优质解上通过，又要能杀死该解的变异版本，从而推动测试具备区分能力，而不是只是形式上通过。
- 在强化学习开始前，ZeroCoder 会过滤掉低信息量的训练题目，只保留通过/失败矩阵秩足够高的样本，因为低秩矩阵提供的学习信号较弱。
- 论文还提出了 **DyB^4**，这是贝叶斯选择器的动态版本。它会在训练过程中用少至 10 个带标注的校准样本重新校准先验，以减少选择器漂移。

## 结果
- 在完全无标注设置下，在 **Qwen2.5-Coder-7B-Instruct** 上，使用 **B^4** 的 ZeroCoder 相比基础模型将代码生成提升了 **14.5%**，测试生成提升了 **15.6%**。
- 在同一模型上，加入 **DyB^4** 后，代码生成增幅提高到 **21.6%**，测试生成增幅提高到 **24.3%**。论文称这一结果与使用 oracle 监督的训练具有竞争力。
- 在 **3 个模型家族** 和 **6 个基准** 上取平均，使用 **DyB^4** 的 ZeroCoder 相比基础模型将代码生成提升了 **18.8%**，测试生成提升了 **62.7%**。
- 该方法在 **4 个代码生成基准** 和 **2 个测试生成基准** 上进行了评估。代码生成使用贪心解码下的 **Pass@1**；测试生成使用 **test accuracy** 和 **mutation score**。
- DyB^4 只使用包含 **10 个带标注样本** 的校准集，论文报告这一步校准带来的单步实际运行时间开销约为 **2%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07864v1](http://arxiv.org/abs/2604.07864v1)
