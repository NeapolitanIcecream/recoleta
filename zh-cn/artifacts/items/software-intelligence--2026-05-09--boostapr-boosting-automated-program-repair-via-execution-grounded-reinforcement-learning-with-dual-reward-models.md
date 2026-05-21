---
source: arxiv
url: https://arxiv.org/abs/2605.09134v3
published_at: '2026-05-09T19:31:02'
authors:
- Yuanhao Li
- Hongbo Wang
- Xiaotang Shang
- Xunzhu Tang
- Yiming Cao
- Xuhong Chen
topics:
- automated-program-repair
- reinforcement-learning
- code-intelligence
- reward-modeling
- execution-feedback
- software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# BoostAPR: Boosting Automated Program Repair via Execution-Grounded Reinforcement Learning with Dual Reward Models

## Summary
## 摘要
BoostAPR 使用执行反馈和行级奖励分配来训练代码修复模型，让 PPO 学会补丁中哪些编辑有帮助。它面向真实仓库缺陷的自动程序修复，以及 Java/Python 修复基准。

## 问题
- 基于 LLM 的自动程序修复只能获得稀疏的执行反馈：补丁要么通过所有测试，要么失败，因此 RL 获得的训练信号较弱。
- 序列级奖励给整个多行 diff 一个分数，这让模型难以判断哪些编辑修好了程序，哪些编辑破坏了程序。
- 这一点会影响真实代码库中的调试和维护工作量，尤其是在 pass@1 质量是用户最直接可见结果时。

## 方法
- 基础策略是 Qwen2.5-Coder-32B-Instruct，只在 SWE-Gym 上训练。阶段 I 在 Claude 3.5 Sonnet 演示上进行监督微调，这些演示包含推理轨迹和经执行验证的补丁；生成的补丁约有 35% 通过过滤。
- 阶段 II 训练序列奖励模型 Rseq，训练数据为采样补丁和执行派生分数，分数结合了补丁应用成功、测试通过率和 diff 大小惩罚。它的损失函数结合了分数回归和成对偏好排序。
- 阶段 II 还在 unified diff 中的连续编辑行跨度上训练行奖励模型 Rline。通过测试的补丁提供正向跨度；失败补丁通过堆栈跟踪、函数级启发式方法或均匀回退提供负向或较低信用的跨度。
- 阶段 III 运行 300 步 PPO。Rseq 给出补丁级分数，Rline 将该分数分配到编辑行跨度内的 token。格式错误的 diff 会收到确定性的格式惩罚。

## 结果
- SWE-bench Verified：500 个任务上 pass@1 为 40.7%，比 17.8% 的 Qwen2.5-Coder-32B 基础模型高 22.9 个百分点，比仅使用 Rseq 的 PPO 38.3% 高 2.4 个百分点。SWE-RL 使用 70B 主干模型报告了 41.0%。
- Defects4J v2.0：在 SWE-Gym 上训练后，835 个 Java 缺陷上达到 24.8%，比 11.3% 的基础模型高 13.5 个百分点，比仅使用 Rseq 的 PPO 19.2% 高 5.6 个百分点。
- HumanEval-Java：164 个任务上达到 84.5%，比 64.0% 的基础模型高 20.5 个百分点，比仅使用 Rseq 的 PPO 79.4% 高 5.1 个百分点。
- QuixBugs：40 个缺陷上达到 95.0%，比 90.0% 的基础模型高 5.0 个百分点；相较仅使用 Rseq 的 PPO 95.0% 没有提升。
- 仅阶段 I SFT 在 SWE-bench Verified 上达到 23.4%，在 Defects4J 上达到 14.9%，在 HumanEval-Java 上达到 73.1%，在 QuixBugs 上达到 92.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09134v3](https://arxiv.org/abs/2605.09134v3)
