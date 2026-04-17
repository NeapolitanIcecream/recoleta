---
source: arxiv
url: http://arxiv.org/abs/2604.05595v1
published_at: '2026-04-07T08:43:36'
authors:
- Baoshun Tong
- Haoran He
- Ling Pan
- Yang Liu
- Liang Lin
topics:
- vision-language-action
- robot-red-teaming
- linguistic-robustness
- reinforcement-learning
- robot-safety
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Uncovering Linguistic Fragility in Vision-Language-Action Models via Diversity-Aware Red Teaming

## Summary
## 摘要
这篇论文研究视觉-语言-动作模型对看起来无害的指令改写有多脆弱。论文提出了 DAERT，这是一种基于强化学习的红队方法，用来搜索多样化的释义改写，在保持任务语义不变的同时让机器人策略失效。

## 问题
- 当人类用不同措辞表达同一个任务时，VLA 机器人策略可能会失败，这对部署安全构成风险。
- 现有自动化红队方法常常只能找到一小组重复攻击，因为以奖励最大化为目标的强化学习容易塌缩到单一模式。
- 一个有用的攻击生成器必须保持原始任务语义、保证可执行性，并且还能暴露许多不同的失败案例。

## 方法
- 论文训练了一个视觉语言模型攻击器，把任务指令改写成语义等价但更难处理的指令，并使用目标机器人策略在模拟器中的反馈进行训练。
- DAERT 加入了受 ROVER 启发的多样性感知强化学习目标。简而言之，它奖励有效的攻击，同时抑制策略把全部概率集中到一种改写模式上。
- 该方法使用隐式的 token 级 actor-critic，并结合均匀平均的后继价值，因此生成过程会分布在多个有效续写上，而不会塌缩为单一短语模板。
- 该方法在模拟器评估前用级联奖励过滤无效攻击：格式检查、与原始指令的语义相似度，以及长度上限。只有有效改写才会因导致任务失败而获得奖励。
- 实验使用 Qwen3-VL-4B 作为攻击器，在 LIBERO 上针对两个目标 VLA（$\pi_{0}$ 和 OpenVLA）进行测试，并讨论了在 CALVIN 和 SimplerEnv 上的迁移评估。

## 结果
- 在 LIBERO 上针对 $\pi_{0}$ 时，原始指令下的平均任务成功率为 93.33%，ERT 将其降到 65.50%，GRPO 降到 20.45%，DAERT 降到 5.85%。
- 在同样的 $\pi_{0}$ 设定下，DAERT 在多样性指标上也优于 GRPO：CLIP 余弦距离指标为 12.23，对比 7.05；LLM-judge 评分为 8.48，对比 4.58。
- 在 LIBERO 上，$\pi_{0}$ + DAERT 按任务套件划分的结果为：Spatial 成功率 7.4%，Object 为 8.8%，Goal 为 3.0%，Long 为 4.2%。数值越低，攻击越强，因为这意味着攻击导致了更多失败。
- 对在 LIBERO 上微调的 OpenVLA，平均成功率从原始指令下的 76.50% 降至 ERT 的 32.15%、GRPO 的 17.00%，以及 DAERT 的 6.25%。
- 论文称，DAERT 在攻击成功率上比先前方法高出 +59.7%，并且可以迁移到不同目标 VLA 和机器人领域。
- 一个诊断测试解释了作者为何将 $\pi_{0}$ 作为语言脆弱性的重点对象：在通用的“no action”指令下，$\pi_{0}$ 的平均成功率为 17.65%，而 $\pi_{0.5}$ 仍有 54.90%，这说明 $\pi_{0.5}$ 对语言的依赖更低。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05595v1](http://arxiv.org/abs/2604.05595v1)
