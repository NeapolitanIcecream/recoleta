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
- white-box-verification
- code-generation
- execution-traces
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning

## Summary
ExecVerify 用可验证的程序执行中间步骤奖励来训练代码模型，不再只模仿教师解释文本。它把“看代码猜执行”变成一个能逐步核对答案的强化学习问题，并显示这种能力还能迁移到代码生成。

## Problem
- 现有代码执行推理训练多依赖 SFT 学习教师写出的解释链，但训练时**无法显式验证中间执行步骤是否真的正确**，容易学成“文本模仿”而非语义理解。
- 训练数据通常**缺少可控难度与结构覆盖**，会混入过于简单或几乎不可解的样本，影响小模型学习真实执行过程。
- 代码执行推理能力不足会进一步拖累下游任务，如**代码生成、程序修复和语义理解**，因此这是代码智能中的关键短板。

## Approach
- 先做**约束式数据合成**：围绕 Python 内置类型、方法和控制流模式自动生成程序，并按从简单到复杂的结构约束构造多难度课程式数据。
- 对每个程序执行得到解释器 trace，再自动生成两类**白盒可验证问题**：下一条执行语句预测（control-flow）以及变量值/类型预测（data-flow）。
- 用**白盒强化学习**训练模型：奖励既看最终 I/O 是否正确，也看中间步骤问题是否答对；奖励函数把终态正确性与步骤级正确性组合起来。
- 还加入**反向 O→I 预测**，让模型根据输出找可执行输入，减少只靠正向模式匹配。
- 采用**两阶段训练**：第一阶段提升执行推理；第二阶段再用单元测试奖励做代码生成 RL，把推理能力迁移到生成功能正确的程序上。

## Results
- 在代码执行推理上，7B 基座从平均 **60.8** 提升到 **80.8**（`+ SFT + white-box RL`），比 `+ SFT + I/O RL` 的 **76.3** 更高，也超过 **Qwen2.5-Coder-32B-Instruct** 的 **77.9** 平均分。
- 细项上，`+ SFT + white-box RL` 在 **CRUXEval-O 85.6**、**LiveCodeBench-Exec 82.3**、**REval State 74.5**、**REval Path 73.0**；相比 7B base 的 **61.0 / 58.0 / 51.7 / 49.7** 有明显提升，说明对白盒中间状态学习尤其有效。
- 在代码生成上，最佳两阶段模型 `+ SFT + white-box RL + UT RL` 平均 **57.1**，高于纯 `+ UT RL` 的 **53.9**、`+ I/O RL + UT RL` 的 **54.6**、`+ SFT + I/O RL + UT RL` 的 **54.9**；论文称相对强后训练基线 **pass@1 最多提升 5.9 个点**。
- 具体生成指标包括：**HumanEval+ 84.8**、**MBPP+ 75.1**、**LiveCodeBench Hard 5.9**、**BigCodeBench Hard 25.7**；相对 7B base 的 **84.1 / 71.7 / 3.0 / 18.2** 均有提升。
- 数据构建方面，作者从 **239,992** 原始样本和 **239,466** 变异样本出发，执行过滤后保留 **201,537** 与 **191,463**，再按难度筛到 **119,358** 个训练样本；Stage I 实际使用 **30K SFT + 30K RL**。
- 消融显示两类白盒问题互补：完整版平均 **80.8**，仅 control-flow 为 **79.9**，仅 data-flow 为 **78.1**。库相关 I/O 预测上，7B base **56.0**，`SFT+I/O RL` **62.5**，`SFT+White-Box RL` **64.7**，接近 32B 的 **70.4**。

## Link
- [http://arxiv.org/abs/2603.11226v1](http://arxiv.org/abs/2603.11226v1)
