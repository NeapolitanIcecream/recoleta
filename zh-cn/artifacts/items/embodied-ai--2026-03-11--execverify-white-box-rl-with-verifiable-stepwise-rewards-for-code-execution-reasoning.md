---
source: arxiv
url: http://arxiv.org/abs/2603.11226v1
published_at: '2026-03-11T18:49:45'
authors:
- Lingxiao Tang
- He Ye
- Zhaoyang Chu
- Muyang Ye
- Zhongxin Liu
- Xiaoxue Ren
- Lingfeng Bao
topics:
- code-reasoning
- reinforcement-learning
- white-box-rewards
- execution-traces
- code-generation
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning

## Summary
ExecVerify提出一种用于代码执行推理的白盒强化学习框架，用可验证的中间执行奖励替代单纯模仿教师解释。它还结合受约束的数据合成与两阶段训练，把执行推理能力迁移到代码生成上。

## Problem
- 现有代码推理训练多依赖SFT去模仿教师生成的解释链，但执行中的中间步骤（如下一条语句、变量值、变量类型）在训练时**无法被显式验证**。
- 这会让模型学成“像在解释”，却不一定真的理解程序如何执行，尤其对小模型更明显，并影响代码生成、程序修复等下游任务。
- 现有数据通常缺少**难度控制**，样本可能过于简单或过难，缺乏循序渐进的课程式训练。

## Approach
- 用**约束式程序合成**构建训练集：遍历Python内建类型和方法，并逐步加入方法组合约束、控制流嵌套约束，生成从简单到复杂的程序。
- 为每段程序自动合成输入、执行并过滤，先得到239,992个raw和239,466个mutated实例，执行过滤后保留201,537个raw和191,463个mutated，再通过难度筛选保留**119,358**个“对7B非平凡但可解”的样本。
- 从解释器执行轨迹中自动生成两类**可验证白盒问题**：控制流问题（预测下一条执行语句）和数据流问题（预测下一步变量值/类型）。
- 第一阶段先做短暂SFT warm-up，再做白盒RL；奖励同时考虑最终I/O正确性与中间步骤正确性，使用 \(R_{white-box}=2((1-\alpha)R^{I\rightarrow O}+\alpha R_{white})\)，文中设 \(\alpha=0.5\)。
- 第二阶段再用单元测试奖励做代码生成RL，把学到的执行推理能力迁移到生成可通过测试的代码上。

## Results
- **代码推理**：最终7B模型（SFT + white-box RL）在CRUXEval、LiveCodeBench-Exec、REval上的平均分从基础7B的**60.8**提升到**80.8**（+**20.0**），并超过Qwen2.5-Coder-32B-Instruct的**77.9**平均分。
- 具体推理指标上，7B白盒RL模型达到：CRUXEval-O **85.6**、CRUXEval-I **81.0**、LCB-Exec **82.3**、REval State **74.5**、Path **73.0**；相较基础7B分别如CRUXEval-O **61.0→85.6**、State **51.7→74.5**、Path **49.7→73.0**。
- 相比仅做I/O RL或SFT+I/O RL，白盒RL整体更强：平均分分别为**71.4**、**76.3**、**80.8**，说明中间执行奖励优于只看最终输出。
- **代码生成**：两阶段最佳7B模型（SFT + white-box RL + UT RL）在HumanEval/MBPP/LiveCodeBench/BigCodeBench上的平均分为**57.1**，高于基础7B的**51.0**，也高于纯UT RL的**53.9**。
- 论文声称其代码生成pass@1相对强后训练基线最高提升**5.9**个百分点；表中如LiveCodeBench-Hard从基础7B的**3.0**提升到**5.9**，MBPP+从**71.7**到**75.1**，BigCodeBench-Hard从**18.2**到**25.7**。
- 白盒问题消融显示控制流与数据流奖励互补：Full平均**80.8**，优于CF-only的**79.9**和DF-only的**78.1**。此外，在含库I/O预测上，7B基础模型**56.0**，SFT+I/O RL **62.5**，SFT+white-box RL **64.7**，接近32B模型的**70.4**。

## Link
- [http://arxiv.org/abs/2603.11226v1](http://arxiv.org/abs/2603.11226v1)
