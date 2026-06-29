---
source: arxiv
url: http://arxiv.org/abs/2603.29957v2
published_at: '2026-03-31T16:24:03'
authors:
- Xue Jiang
- Tianyu Zhang
- Ge Li
- Mengyang Liu
- Taozhi Chen
- Zhenhua Xu
- Binhua Li
- Wenpin Jiao
- Zhi Jin
- Yongbin Li
- Yihong Dong
topics:
- code-generation
- reasoning-llm
- reinforcement-learning
- test-time-reasoning
- code-benchmarks
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Think Anywhere in Code Generation

## Summary
## 总结
Think-Anywhere 把代码生成从一次性、前置的推理块，改成了可以在写代码过程中插入推理。论文声称，这样在四个代码基准上能取得更好的 pass@1 结果，也能让模型把额外推理放到更难的代码位置附近。

## 问题
- 标准的推理型 LLM 通常先思考一次，再生成代码。在代码任务里，很多错误会在实现阶段才出现，这时最初的计划已经固定了。
- 代码难度在不同 token 和不同代码行之间并不均匀。样板代码几乎不需要推理，算法选择和边界情况则需要更多推理。
- 只靠提示词，模型并不能稳定学会在代码生成过程中停下来思考，所以这种行为需要通过训练来学。

## 方法
- 该方法让模型在生成正常代码的同时，在任意 token 位置输出带有 `<thinkanywhere>...</thinkanywhere>` 标记的行内推理块，最终可执行代码则通过去掉所有推理块得到。
- 训练分两阶段：先用大约 5,000 个自动构造的样本做冷启动监督训练，这些样本演示行内推理；再用可验证奖励做 RL，让模型学会在什么位置触发推理。
- RL 设置使用 GRPO，奖励把所需推理结构的格式检查和基于测试用例的二值执行正确性合并起来。
- 论文还测试了一个特殊 token 版本 Think-Anywhere*，把行内推理触发器设成一个专门的词表 token，并用现有 token embedding 加上分隔符 embedding 进行初始化。
- 默认实验使用 Qwen2.5-Coder-7B-Instruct、Skywork 数据集中的 14K 个编程问题、pass@1 评估，以及四个基准：LeetCode、LiveCodeBench、HumanEval 和 MBPP。

## 结果
- 主要结果：Think-Anywhere（Ours）的平均 pass@1 达到 **70.3**，高于 **61.0** 的基础模型、**68.4** 的标准 GRPO 基线和 **66.8** 的 CodeRL+。
- 按基准看，Think-Anywhere（Ours）在 LeetCode 上得分 **69.4**，在 LiveCodeBench 上得分 **37.2**，在 HumanEval 上得分 **91.5**，在 MBPP 上得分 **82.9**。基础模型在同样数据集上的分数是 **50.6 / 34.3 / 88.4 / 70.7**。
- 和列出的最强后训练基线 CodeRL+ 相比，Think-Anywhere 的平均 pass@1 提升了 **3.5** 分（**70.3 vs 66.8**）。
- 和 GRPO 相比，Think-Anywhere 的平均 pass@1 提升了 **1.9** 分（**70.3 vs 68.4**），在 LeetCode（**69.4 vs 67.3**）、LiveCodeBench（**37.2 vs 36.0**）、HumanEval（**91.5 vs 88.6**）和 MBPP（**82.9 vs 81.7**）上都有提升。
- 在他们的设置里，RL 很关键：Think-Anywhere（Prompting）的平均分是 **56.9**，Think-Anywhere（SFT）是 **60.6**，都低于 RL 训练版本的 **70.3**。
- 特殊 token 版本 Think-Anywhere*（Ours）的平均分达到 **70.0**，接近文本标签版本的 **70.3**。论文还说分析显示，模型倾向于在更高熵的位置插入推理，但摘要没有给出熵相关性的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29957v2](http://arxiv.org/abs/2603.29957v2)
