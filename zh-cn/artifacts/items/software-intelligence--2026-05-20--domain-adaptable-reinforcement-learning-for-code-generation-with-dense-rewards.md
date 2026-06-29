---
source: arxiv
url: https://arxiv.org/abs/2605.21180v1
published_at: '2026-05-20T13:47:52'
authors:
- Erfan Aghadavoodi Jolfaei
- Daniel Maninger
- Abhinav Anand
- Mert Tiftikci
- Mira Mezini
topics:
- code-generation
- reinforcement-learning
- dense-rewards
- program-synthesis
- robotics-code
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Domain-Adaptable Reinforcement Learning for Code Generation with Dense Rewards

## Summary
## 总结
论文用 PPO 训练 Qwen2.5-Coder-1.5B，并使用密集的执行感知奖励，让代码 token 得到与语法、lint 检查、测试、数据流匹配或机器人模拟器结果相关的反馈。结果显示，MBPP/MBPP+ 的 pass@1 更高，RoboEval 中不可执行的机器人程序更少。

## 问题
- 代码 LLM 可能生成有语法错误、测试失败、不安全模式或违反领域约束的程序。
- 稀疏的序列级 RL 奖励会把同样的惩罚或奖励给整个输出，这会让归因变弱，尤其是在只有少数 token 导致失败时。
- 机器人代码需要额外检查，因为程序可以编译通过，但仍然会因为碰撞、目标不可达、对象使用错误或动作顺序错误而失败。

## 方法
- 该方法使用近端策略优化，对预训练的 Qwen2.5-Coder-1.5B-Instruct policy 进行微调。
- 奖励结合了来自 SynCode 风格约束的语法检查、Ruff linter 信号、相对参考模型的 KL 距离，以及可选的任务奖励。
- 对于通用 Python，任务奖励是单元测试 pass@1 和数据流图匹配。
- 对于机器人任务，任务奖励来自 RoboSim 模拟器反馈。
- 在可能时，序列级信号会映射回代码 token 或 span；如果无法精确归因，单元测试结果会分摊到生成的代码 token 上。

## 结果
- 在 MBPP 的 pass@1 上，Qwen2.5-Coder-1.5B 从 0.460 提升到 0.653，绝对提升 0.193，即 19.3 个百分点。
- 在 MBPP+ 的 pass@1 上，同一模型从 0.413 提升到 0.556，绝对提升 0.143，即 14.3 个百分点。
- 在包含 80 个任务的 RoboEval 上，经过 RL 微调后，Python 级错误从 77 降到 11。
- 在 RoboEval 上，微调后的 1.5B 模型解决的任务数从 0 提升到 14/80。
- 论文报告称，微调后不可执行的机器人代码从 100% 降到 51% 可由模拟器执行。
- 更大的 7B 基线在 RoboEval 成功数上仍然更高：Qwen2.5-Coder-7B base 为 30/80，7B Robo-Instruct 模型为 31/80，而微调后的 1.5B 模型为 14/80。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21180v1](https://arxiv.org/abs/2605.21180v1)
