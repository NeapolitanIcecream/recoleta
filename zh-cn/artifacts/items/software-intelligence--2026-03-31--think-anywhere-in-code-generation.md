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
## 摘要
Think-Anywhere 把代码生成从“先集中推理一次”改成“在写代码过程中随时插入推理”。论文称，这种方式在四个代码基准上带来更好的 pass@1 结果，也让模型更容易在代码中的困难位置附近加入额外推理。

## 问题
- 标准推理型 LLM 通常会在生成代码前只思考一次。在代码任务里，很多 bug 会在实现过程中出现，此时最初的方案已经固定。
- 代码在不同 token 和代码行上的难度并不均匀。样板代码几乎不需要推理，而算法选择和边界情况需要更多推理。
- 仅靠 prompting 不能稳定地教会模型在代码生成过程中停下来思考，所以这种行为需要通过训练获得。

## 方法
- 该方法允许模型在任意 token 位置输出普通代码和用 `<thinkanywhere>...</thinkanywhere>` 标记的行内推理块，最终可执行代码则通过去掉所有推理块得到。
- 训练分两阶段：先是在约 5,000 个自动构造样本上做冷启动监督训练，示范如何插入行内推理；再用带可验证奖励的 RL，让模型学会在什么位置触发推理。
- RL 设置使用 GRPO，奖励由两部分组成：对所需推理结构的格式检查，以及基于测试用例执行结果的二元正确性判断。
- 论文还测试了一个特殊 token 变体 Think-Anywhere*，其中触发行内推理的是一个专用词表 token，它由已有 token embedding 和分隔符 embedding 初始化得到。
- 默认实验使用 Qwen2.5-Coder-7B-Instruct、Skywork 数据集中的 14K 道编程题、pass@1 评估，以及四个基准：LeetCode、LiveCodeBench、HumanEval 和 MBPP。

## 结果
- 主要结果：Think-Anywhere (Ours) 的平均 pass@1 达到 **70.3**，高于基础模型的 **61.0**、标准 GRPO 基线的 **68.4**，以及 **66.8** 的 CodeRL+。
- 按基准看，Think-Anywhere (Ours) 在 LeetCode 上是 **69.4**，在 LiveCodeBench 上是 **37.2**，在 HumanEval 上是 **91.5**，在 MBPP 上是 **82.9**。基础模型在相同数据集上的成绩分别是 **50.6 / 34.3 / 88.4 / 70.7**。
- 与列出的最强后训练基线 CodeRL+ 相比，Think-Anywhere 的平均 pass@1 提高了 **3.5 个点**（**70.3 vs 66.8**）。
- 与 GRPO 相比，Think-Anywhere 的平均 pass@1 提高了 **1.9 个点**（**70.3 vs 68.4**），并且在 LeetCode（**69.4 vs 67.3**）、LiveCodeBench（**37.2 vs 36.0**）、HumanEval（**91.5 vs 88.6**）和 MBPP（**82.9 vs 81.7**）上都有提升。
- 在他们的设置里，RL 很关键：Think-Anywhere (Prompting) 的平均分是 **56.9**，Think-Anywhere (SFT) 是 **60.6**，都低于经过 RL 训练的 **70.3**。
- 特殊 token 版本 Think-Anywhere* (Ours) 的平均分达到 **70.0**，接近文本标签版本的 **70.3**。论文还称，分析显示模型倾向于在更高熵的位置插入推理，但摘录里没有给出熵相关性的具体数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29957v2](http://arxiv.org/abs/2603.29957v2)
