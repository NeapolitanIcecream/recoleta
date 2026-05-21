---
source: arxiv
url: https://arxiv.org/abs/2605.07931v3
published_at: '2026-05-08T16:04:43'
authors:
- Zuojin Tang
- Shengchao Yuan
- Xiaoxin Bai
- Zhiyuan Jing
- De Ma
- Gang Pan
- Bin Liu
topics:
- vision-language-action
- world-models
- robot-policy
- long-horizon-manipulation
- visual-token-compression
- latent-rollout
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy

## Summary
## 摘要
OneWM-VLA 为冻结的 $\pi_0$ VLA 添加了一个紧凑的潜在世界模块，并表明每帧一个语义视觉 token 可以支持长时程机器人控制。主要主张是，低视觉带宽加上联合潜在-动作流匹配，可以在不训练大型新骨干网络的情况下提高成功率。

## 问题
- 带世界模型的 VLA 通常会展开密集视觉特征或未来像素，随着规划时程变长，计算和内存成本会上升。
- 长时程机器人任务需要策略跟踪场景在未来动作下会如何变化；反应式 VLA 往往会累积错误。
- 论文关注受限适配设置：大部分冻结的预训练 VLA，以及较小的 LoRA 预算。

## 方法
- OneWM-VLA 使用 Adaptive Attention Pooling，将每个相机视角和每一帧压缩成一个语义潜在 token。
- 池化过程用最大响应、求和响应和学习得到的 MLP 分数对视觉 token 打分，然后用学习得到的权重合并池化输出。
- 单个流匹配模型同时生成未来潜在 token 和未来动作块，因此潜在展开和动作生成共享注意力和流时间。
- 该模型基于 $\pi_0$ 构建，包含 PaliGemma-2B 视觉-语言骨干网络、Gemma-300M 潜在-动作专家，以及 14.71M 个 LoRA 可训练参数。
- 推理时，模型同时对潜在流和动作流去噪，然后只在机器人上执行动作流。

## 结果
- 在 MetaWorld MT50 上，摘要报告平均成功率从 $\pi_0$ 的 47.9% 提高到 OneWM-VLA 的 61.3%。在表 1 中，当时程 $H=30$ 时，OneWM-VLA 达到 53.13%，相比之下 $\pi_0$ 为 37.98%，$\pi_{0.5}$ 为 26.83%。
- 在 LIBERO 上，OneWM-VLA 在 Spatial、Object、Goal 和 Long 上的平均成功率达到 98.1%。在 LIBERO-Long 上，它达到 95.6%，相比之下 $\pi_0$ 为 85.2%，$\pi_{0.5}$ 为 92.4%。
- 在干净条件下的真实 Piper 机械臂上，OneWM-VLA 在 Pick Banana、Fold Cloth 和 Pull Drawer 上的平均成功率达到 71.7%，相比之下 $\pi_0$ 为 50.0%，$\pi_{0.5}$ 为 58.3%。
- 在真实 Fold Cloth 任务上，OneWM-VLA 在干净条件下达到 60.0%，相比之下 $\pi_0$ 为 20.0%，$\pi_{0.5}$ 为 25.0%。在观测噪声下，它达到 40.0%，相比之下另外两者为 0.0% 和 10.0%。
- 论文报告了每帧 1 到 12 个 token 的带宽扫描；在匹配的训练预算下，随着 token 数量增加，成功率下降；摘录未给出具体扫描数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07931v3](https://arxiv.org/abs/2605.07931v3)
