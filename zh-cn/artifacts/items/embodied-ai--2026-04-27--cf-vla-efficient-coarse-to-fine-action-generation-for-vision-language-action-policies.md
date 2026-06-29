---
source: arxiv
url: https://arxiv.org/abs/2604.24622v2
published_at: '2026-04-27T15:51:40'
authors:
- Fan Du
- Feng Yan
- Jianxiong Wu
- Xinrun Xu
- Weiye Zhang
- Weinong Wang
- Yu Guo
- Bin Qian
- Zhihai He
- Fei Wang
- Heng Yang
topics:
- vision-language-action
- robot-foundation-model
- flow-matching
- efficient-inference
- robot-manipulation
- coarse-to-fine-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# CF-VLA: Efficient Coarse-to-Fine Action Generation for Vision-Language-Action Policies

## Summary
## 摘要
CF-VLA 通过把基于流的 VLA 动作采样从长链式迭代生成，改成两步式的粗初始化和细修正，来提升速度。它面向实时机器人操作，这类任务里每多一步动作生成都会增加延迟。

## 问题
- 基于流的 VLA 策略，例如 $\pi_{0.5}$，可以建模连续、多峰的机器人动作，但需要很多推理步才能把高斯噪声变成有效动作。
- 低步数采样会损失动作质量，因为一条短轨迹既要找到动作流形，又要修正局部误差。
- 这会影响闭环机器人控制，因为动作延迟会降低接触丰富、长时程或双臂任务的成功率。

## 方法
- CF-VLA 将动作生成拆成两个阶段，NFE=2：粗阶段构建一个受动作先验引导的起点，细阶段做一次局部修正。
- 粗阶段先采样高斯噪声 $\epsilon_1$，再预测端点速度的条件后验 $q_\theta(u \mid o, \epsilon_1)$，并构造 $\tilde{\epsilon}=\epsilon_1-\hat{u}$。
- 粗后验用 KL 损失训练，目标是一个以端点速度 $u_{t_1}=\epsilon_1-a$ 为中心、方差为 $\sigma_{noise}^2I$ 的高斯分布。
- 细阶段在固定的细化时刻 $t_f$，从 $\tilde{\epsilon}$ 预测到真实动作的残差更新，并用 MSE 损失训练。
- 训练分两阶段：先用端点和代理细化损失做预热，再联合优化 $\mathcal{L}_{fine}+\lambda\mathcal{L}_{coarse}$。

## 结果
- 在 LIBERO 上、NFE=2 时，CF-VLA 的平均成功率为 96.5。对比之下，复现的 MIP 在 $\pi_{0.5}$ 架构上是 93.6，MIP 在 $\pi_0$ 架构上是 92.7，复现的 $\pi_{0.5}$ 在 NFE=2 时是 94.8。
- CF-VLA 在 LIBERO 各子集上的分数分别是：Spatial 98.0，Object 99.2，Goal 96.6，Long 92.0。
- 与 LIBERO 上 NFE=10 的 $\pi_{0.5}$ 相比，CF-VLA 的平均分更低，96.5 对 96.9，但它在 Object 上更高，99.2 对 98.2，同时只用了 2 次函数评估而不是 10 次。
- 论文声称动作采样延迟减少了 75.4%。
- 在真实机器人实验中，CF-VLA 的平均成功率为 83.0，比 MIP 高 19.5 个百分点，比 $\pi_{0.5}$ 高 4.0 个百分点。
- 摘要说明 CF-VLA 在 CALVIN 和 LIBERO 的若干指标上与 NFE=10 的 $\pi_{0.5}$ 基线持平或更好，但给出的 CALVIN 表格被截断了，所以这里无法给出精确的 CALVIN 数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24622v2](https://arxiv.org/abs/2604.24622v2)
