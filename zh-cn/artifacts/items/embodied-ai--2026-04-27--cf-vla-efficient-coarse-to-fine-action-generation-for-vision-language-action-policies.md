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
CF-VLA 通过两步生成让基于流的 VLA 动作采样更快：先做粗初始化，再做细修正，取代从高斯噪声开始的长迭代生成。它面向实时机器人操作，因为每增加一次动作生成步骤都会增加延迟。

## 问题
- 基于流的 VLA 策略，例如 $\pi_{0.5}$，可以建模连续、多模态的机器人动作，但需要许多推理步骤才能把高斯噪声变成有效动作。
- 低步数采样会损害动作质量，因为一条很短的轨迹既要找到动作流形，又要修正局部误差。
- 这会影响闭环机器人控制；在接触密集、长时程或双臂任务中，动作延迟可能降低成功率。

## 方法
- CF-VLA 将动作生成拆成两个阶段，NFE=2：粗阶段构建一个由动作先验引导的起点，细阶段进行一次局部修正。
- 粗阶段采样高斯噪声 $\epsilon_1$，预测端点速度的条件后验 $q_\theta(u \mid o, \epsilon_1)$，并形成 $\tilde{\epsilon}=\epsilon_1-\hat{u}$。
- 粗后验使用 KL 损失训练，目标是一个以端点速度 $u_{t_1}=\epsilon_1-a$ 为中心、方差为 $\sigma_{noise}^2I$ 的目标高斯分布。
- 细阶段在固定细化时间 $t_f$，用 MSE 损失预测从 $\tilde{\epsilon}$ 到真实动作的残差更新。
- 训练分两阶段：先用端点损失和代理细化损失进行预热，再用 $\mathcal{L}_{fine}+\lambda\mathcal{L}_{coarse}$ 进行联合训练。

## 结果
- 在 LIBERO 上使用 NFE=2 时，CF-VLA 报告的平均成功率为 96.5；相比之下，在 $\pi_{0.5}$ 架构上复现的 MIP 为 93.6，在 $\pi_0$ 架构上的 MIP 为 92.7，NFE=2 的复现 $\pi_{0.5}$ 为 94.8。
- CF-VLA 的 LIBERO 套件得分为：Spatial 98.0、Object 99.2、Goal 96.6、Long 92.0。
- 与 LIBERO 上 NFE=10 的 $\pi_{0.5}$ 相比，CF-VLA 的平均分更低，为 96.5 对 96.9；但它在 Object 上更高，为 99.2 对 98.2，同时函数评估次数为 2 次而非 10 次。
- 论文称动作采样延迟降低了 75.4%。
- 在真实机器人实验中，CF-VLA 报告的平均成功率为 83.0，比 MIP 高 19.5 个百分点，比 $\pi_{0.5}$ 高 4.0 个百分点。
- 摘录称，CF-VLA 在若干 CALVIN 和 LIBERO 指标上达到或超过 NFE=10 的 $\pi_{0.5}$ 基线，但提供的 CALVIN 表格被截断，因此这里没有可用的 CALVIN 精确数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24622v2](https://arxiv.org/abs/2604.24622v2)
