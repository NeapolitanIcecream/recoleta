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
BoostAPR 用执行反馈和行级奖励分配训练代码修复模型，让 PPO 学会判断补丁里哪些编辑有用。它面向真实仓库漏洞的自动程序修复，以及 Java/Python 修复基准。

## 问题
- 基于 LLM 的自动程序修复得到的执行反馈很稀疏：一个补丁要么通过所有测试，要么失败，所以强化学习拿到的训练信号很弱。
- 序列级奖励只给整段多行 diff 一个分数，难以把功劳分到真正修好或破坏程序的那些编辑上。
- 这很重要，因为更好的修复模型可以减少真实代码库里的调试和维护工作，尤其是在 pass@1 质量是主要可见结果时。

## 方法
- 基础策略是 Qwen2.5-Coder-32B-Instruct，只在 SWE-Gym 上训练。第一阶段先用 Claude 3.5 Sonnet 的示范做监督微调，示范里包含推理轨迹和经执行验证的补丁；大约 35% 的生成补丁通过过滤。
- 第二阶段训练序列奖励模型 Rseq，输入采样补丁和从执行结果导出的分数。这个分数结合了补丁应用成功率、测试通过率和 diff 大小惩罚。它的损失把分数回归和成对偏好排序结合起来。
- 第二阶段还训练行奖励模型 Rline，作用对象是统一 diff 里连续的编辑行跨度。通过的补丁提供正跨度；失败补丁从堆栈跟踪、函数级启发式规则，或统一回退规则中提供负跨度或更低权重的跨度。
- 第三阶段运行 300 步 PPO。Rseq 给出补丁级分数，Rline 把这个分数分配到编辑行跨度内部的 token。格式错误的 diff 会收到确定性的格式惩罚。

## 结果
- SWE-bench Verified：500 个任务上 pass@1 为 40.7%，比 Qwen2.5-Coder-32B 基线的 17.8% 高 22.9 个百分点，也比只用 Rseq 的 PPO 高 2.4 个百分点，后者为 38.3%。SWE-RL 用 70B 骨干模型报告了 41.0%。
- Defects4J v2.0：在 835 个 Java 漏洞上达到 24.8%，在 SWE-Gym 上训练后，比 11.3% 的基线高 13.5 个百分点，也比只用 Rseq 的 PPO 高 5.6 个百分点，后者为 19.2%。
- HumanEval-Java：在 164 个任务上达到 84.5%，比 64.0% 的基线高 20.5 个百分点，也比只用 Rseq 的 PPO 高 5.1 个百分点，后者为 79.4%。
- QuixBugs：在 40 个漏洞上达到 95.0%，比 90.0% 的基线高 5.0 个百分点，但和只用 Rseq 的 PPO 相比没有提升，后者也是 95.0%。
- 只做第一阶段 SFT 时，SWE-bench Verified 达到 23.4%，Defects4J 达到 14.9%，HumanEval-Java 达到 73.1%，QuixBugs 达到 92.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09134v3](https://arxiv.org/abs/2605.09134v3)
