---
source: arxiv
url: https://arxiv.org/abs/2606.03108v1
published_at: '2026-06-02T03:47:48'
authors:
- Guhong Chen
- Yingcheng Shi
- Yongbin Li
- Binhua Li
- Xander Xu
- Hu Wei
- Shiwen Ni
- Min Yang
- Jieping Ye
topics:
- agentic-rl
- code-intelligence
- software-engineering-agents
- autonomous-training
- llm-reinforcement-learning
- diagnostic-harness
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning

## Summary
## 总结
EvoTrainer 通过同时演化策略和决定下一步尝试什么的诊断代码来训练 LLM 智能体。它在代码仓库级 SWE 上的提升最大，SWE-9B 的 Avg@8 BC% 达到 38.16，而人工设计的 RL 设置为 33.77。

## 问题
- 智能体 RL 运行会以标量分数看不出的方式失败，例如奖励泄漏、零方差 rollout 组、行为塌缩，或误导性的高分。
- 固定的训练诊断很难在不同版本之间、随着瓶颈变化去判断该保留、剪枝还是修改某条训练分支。
- 这对代码和 SWE 智能体很重要，因为长链路的工具使用轨迹需要关于搜索、编辑、测试和奖励行为的证据；最终通过率太粗。

## 方法
- EvoTrainer 保留有版本记录的策略分支，并对奖励、数据过滤、rollout 设置、优化器选择或工具使用行为做大多是单因素干预。
- 实验中的训练器智能体用 Claude Sonnet 4.6 实现，读取指标、rollout、配置、日志和代码 diff，然后提出保留、剪枝、回滚或合并决策。
- 诊断 harness 会随时间变化，通过加入指标、分析器、回测、搜索流程，以及在当前证据无法解释结果时引入外部证据。
- 持久记忆保存版本谱系、失败案例、可复用的分析器技能和搜索轨迹，方便后续领域复用验证过的修复。
- SWE 实现使用 GRPO 风格训练，包含组相对优势、不对称的 Clip-Higher 边界、较弱的 KL 正则化、对行为敏感的奖励，以及考虑方差的组过滤。

## 结果
- 主表中，EvoTrainer 在每个报告列里都是第一行。与无 RL 相比，它在 SWE-4B 上达到 31.49 对 24.68 Avg@8 BC%（+6.81），SWE-9B 上 38.16 对 30.19（+7.97），AIME 2024 上 84.17 对 77.50（+6.67），AIME 2025 上 73.33 对 67.50（+5.83），CNMO 2024 上 81.94 对 75.00（+6.94），Coding 上 51.29 对 46.71（+4.58）。
- 与人工设计的 RL 相比，EvoTrainer 在 SWE-9B 上提升 +4.39 BC%，即 38.16 对 33.77，95% CI 为 [+2.61, +6.34]，p<0.001。
- 与人工设计的 RL 在数学任务上的比较中，论文报告整体 Avg@8 提升 +2.88，p<0.001；在 SWE-4B 和 Coding 上，它在 bootstrap CI 内与人工基线一致，p>0.1。
- 与 AutoResearch 相比，EvoTrainer 在所有展示的设置中都更高：SWE-4B 31.49 对 28.41，SWE-9B 38.16 对 33.33，AIME 2024 84.17 对 78.33，AIME 2025 73.33 对 70.42，CNMO 2024 81.94 对 78.47，Coding 51.29 对 45.51。
- 它也超过了最强的算法基线 RAGEN v2 SNR Filtering，在表中的每一列都更高，包括 SWE-9B 38.16 对 35.74 和 Coding 51.29 对 49.86。
- 评估只用了一个随机种子 seed 42 和 Avg@8，因此最强的证据来自配对检验和报告的置信区间；关于不同运行之间训练稳定性的证据较少。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03108v1](https://arxiv.org/abs/2606.03108v1)
