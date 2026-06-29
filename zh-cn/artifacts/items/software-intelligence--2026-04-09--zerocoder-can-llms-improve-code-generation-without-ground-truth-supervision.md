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
## 总结
ZeroCoder 让模型同时写代码和生成测试，不用人工编写的测试或参考答案。它根据模型自己生成的代码和测试之间的执行结果来构造奖励，再通过协同进化同时提升这两个角色。

## 问题
- 代码生成里的标准强化学习通常需要人工编写的单元测试，或者基于参考答案生成的测试，这些都很耗成本，也很难扩展。
- 只用模型自己生成的测试时，测试往往不够强，坏代码也可能通过，奖励信号就会变得很噪。
- 论文想回答的是，LLM 能不能在完全没有真值监督的情况下，只靠代码和测试的执行反馈来改进代码生成。

## 方法
- ZeroCoder 把同一个模型放在两种提示角色里：**coder** 负责采样候选程序，**tester** 负责为同一个问题采样候选测试。
- 它把每个采样程序和每个采样测试都跑一遍，生成一个通过/失败矩阵，然后用 MaxPass、CodeT 或 **B^4** 这类选择器挑出一组一致的、可能更好的解和测试。
- coder 如果被选入一致解集合，就得到奖励。tester 如果生成的测试既能通过一个代理的较优解，又能杀掉这个解的变体，就得到奖励，这会推动测试变得更有区分度，而不是只图简单。
- 在强化学习之前，ZeroCoder 会先过滤掉信息量低的训练问题，只保留通过/失败矩阵秩足够高的样本，因为低秩矩阵给出的学习信号很弱。
- 论文还加入了 **DyB^4**，这是 Bayesian selector 的动态版本。它在训练过程中用最少 10 个带标注的校准样本重新校准先验，用来减轻 selector drift。

## 结果
- 在完全无标签设置下，ZeroCoder 在 **Qwen2.5-Coder-7B-Instruct** 上使用 **B^4** 时，代码生成比基础模型提升 **14.5%**，测试生成提升 **15.6%**。
- 在同一个模型上加入 **DyB^4** 后，代码生成提升到 **21.6%**，测试生成提升到 **24.3%**，论文说这和 oracle 监督训练有竞争力。
- 在 **3 个模型家族**和 **6 个基准**上的平均结果显示，ZeroCoder 搭配 **DyB^4** 相比基础模型，代码生成提升 **18.8%**，测试生成提升 **62.7%**。
- 该方法评估了 **4 个代码生成基准**和 **2 个测试生成基准**。代码生成使用贪心解码下的 **Pass@1**；测试生成使用 **test accuracy** 和 **mutation score**。
- DyB^4 只用了 **10 个带标注样本**做校准，论文报告这一步大约增加 **2%** 的单步墙钟时间。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07864v1](http://arxiv.org/abs/2604.07864v1)
