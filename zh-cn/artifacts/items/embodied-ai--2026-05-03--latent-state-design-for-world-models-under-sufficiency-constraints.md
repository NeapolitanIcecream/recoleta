---
source: arxiv
url: https://arxiv.org/abs/2605.01694v1
published_at: '2026-05-03T03:19:42'
authors:
- Keon Woo Kim
topics:
- world-models
- latent-state
- sufficiency-constraints
- model-based-rl
- robot-planning
- counterfactual-reasoning
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Latent State Design for World Models under Sufficiency Constraints

## Summary
## 摘要
论文主张，世界模型研究应按任务要求潜在状态保留什么信息来评判。它提出一种按功能划分的分类法，并给出一套评估方案，用于检查潜在状态是否支持预测、控制、规划、记忆、具身 grounding，或反事实推理。

## 问题
- 世界模型一词用于多类系统：基于模型的强化学习、视频预测、生成式仿真、以对象为中心的建模、机器人系统，以及 VLA 规划。它们共同面对的问题是潜在状态设计，因为每类系统都需要状态保留不同的信息。
- 论文指出，按架构给方法分组会让常见比较产生误导。一个优秀的视频预测器可能无法用于控制；一个紧凑的控制状态也可能丢弃图像重建所需的细节。
- 这对具身智能体很重要，因为规划和行动需要状态在部分可观测条件下跟踪可达性、价值、干预、记忆和隐藏世界状态。

## 方法
- 论文把潜在世界模型定义为一个学习得到的状态更新系统：它把历史映射到潜在状态，记为 z_t = phi(h_t)，并学习以动作为条件的动态，记为 p_theta(z_{t+1} | z_t, a_t)。
- 它按 6 种潜在状态角色对方法分组：预测嵌入、递归信念状态、对象/因果结构、潜在动作接口、具身规划接口和记忆基底。
- 它形式化了 3 种充分性关系：在 POMDP 假设下，精确信念状态涵盖预测和控制；预测充分性不保证控制充分性；被动预测如果没有干预、动作数据、因果假设或 grounding，就无法识别反事实动态。
- 它提出沿 7 个轴评估：表征、预测、规划、可控性、因果/反事实支持、记忆和不确定性。
- 它把方法映射到一个压缩谱系上，包括重重建模型、token 压缩、表征预测、由奖励/价值塑形的模型、价值等价模型，以及因果/反事实模型。

## 结果
- 摘录没有报告新的基准准确率、回报、成功率或数据集规模数字。
- 主要的具体主张是为潜在世界模型提出 6 种角色分类，覆盖预测、信念状态、结构化、动作接口、规划接口和记忆角色。
- 论文给出 3 个命题，用来区分信念状态充分性、预测充分性、控制充分性和反事实充分性。
- 它给出一个 7 轴评估矩阵，用于诊断潜在状态保留了什么、丢弃了什么、支持了什么。
- 它列出针对 3 类常见失败模式的基准测试：用于信念状态的遮挡/重访/延迟线索测试；用于控制充分性的冻结/适应控制和稀疏奖励规划测试；用于反事实支持的保留动作替换和对象干预。
- 它的文献图谱覆盖 2018-2026 年的示例，包括 World Models、SimPLe、IRIS、GAIA-1、I-JEPA、V-JEPA 2、LeWorldModel、MuZero、EfficientZero、TD-MPC2、Causal-JEPA 和 CausalVAE-WM。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01694v1](https://arxiv.org/abs/2605.01694v1)
