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
这篇论文研究视觉-语言-动作模型对看起来无害的指令改写有多脆弱。论文提出 DAERT，这是一种基于强化学习的红队方法，搜索语义保持不变但会让机器人策略失败的多样化改写。

## 问题
- 当人类用不同措辞表达同一任务时，VLA 机器人策略会失败，这会给部署带来安全风险。
- 现有的自动红队方法往往只找到一小组重复攻击，因为以奖励最大化为目标的强化学习会塌缩到单一模式。
- 一个有用的攻击生成器必须保留原任务含义、保持可执行，同时还能暴露多种不同的失败情况。

## 方法
- 论文训练一个视觉-语言模型攻击者，把任务指令改写成语义等价但更难的指令，并用目标机器人策略在模拟器中的反馈来优化。
- DAERT 加入了一个受 ROVER 启发的、面向多样性的强化学习目标。简单说，它奖励有效攻击，同时抑制策略把所有概率集中到一种改写模式上。
- 该方法使用隐式的 token 级 actor-critic，并配合均匀平均后继价值，让生成结果分散到多个有效续写上，而不是塌缩成单一短语模板。
- 一个级联奖励会在进入模拟器评估前筛掉无效攻击：格式检查、与原始指令的语义相似度检查，以及长度上限。只有有效改写才会因为导致任务失败而获得奖励。
- 实验使用 Qwen3-VL-4B 作为攻击者，并在 LIBERO 上测试两个目标 VLA，$\pi_{0}$ 和 OpenVLA；CALVIN 和 SimplerEnv 上也讨论了迁移评估。

## 结果
- 在 LIBERO 上针对 $\pi_{0}$ 时，原始指令的平均任务成功率是 93.33%，ERT 降到 65.50%，GRPO 降到 20.45%，DAERT 降到 5.85%。
- 在同样的 $\pi_{0}$ 设置下，DAERT 的多样性分数也高于 GRPO：CLIP 余弦距离指标为 12.23 对 7.05，LLM 评审分数为 8.48 对 4.58。
- 在 LIBERO 上，$\pi_{0}$ + DAERT 的各任务套件结果分别是：Spatial 7.4%，Object 8.8%，Goal 3.0%，Long 4.2%。数值越低越强，因为攻击导致了更多失败。
- 在用 LIBERO 微调的 OpenVLA 上，平均成功率从原始指令下的 76.50% 降到 ERT 的 32.15%、GRPO 的 17.00% 和 DAERT 的 6.25%。
- 论文称 DAERT 在攻击成功率上比先前方法高 59.7%，并且能跨目标 VLA 和机器人领域迁移。
- 一个诊断测试说明作者为什么把 $\pi_{0}$ 作为语言脆弱性的重点：在通用的“no action”指令下，$\pi_{0}$ 的平均成功率是 17.65%，而 $\pi_{0.5}$ 仍然有 54.90%，这说明 $\pi_{0.5}$ 对语言的依赖更低。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05595v1](http://arxiv.org/abs/2604.05595v1)
