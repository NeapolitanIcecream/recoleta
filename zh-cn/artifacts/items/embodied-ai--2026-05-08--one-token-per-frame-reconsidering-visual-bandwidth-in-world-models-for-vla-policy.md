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
OneWM-VLA 在冻结的 $\pi_0$ VLA 上加入了一个紧凑的潜变量世界模块，并表明每帧一个语义视觉 token 就能支持长时程机器人控制。核心结论是，低视觉带宽加上联合潜变量-动作 flow matching，可以在不训练大型新主干的情况下提高成功率。

## 问题
- 带有世界模型的 VLA 往往会展开稠密视觉特征或未来像素，随着规划时程变长，这会增加计算和内存开销。
- 长时程机器人任务需要策略跟踪未来动作下场景如何变化，反应式 VLA 往往会在规划过程中累积误差。
- 论文针对的是受限适配场景：大部分参数冻结的预训练 VLA，加上很小的 LoRA 预算。

## 方法
- OneWM-VLA 使用 Adaptive Attention Pooling，把每个相机视图和每一帧压缩成一个语义潜变量 token。
- 该 pooling 用最大响应、求和响应和一个可学习的 MLP 分数给视觉 token 打分，再用可学习权重组合 pooled 输出。
- 一个 flow-matching 模型同时生成未来潜变量 token 和未来动作片段，因此潜变量展开和动作生成共享 attention 和 flow time。
- 模型建立在 $\pi_0$ 之上，使用 PaliGemma-2B 视觉语言主干、Gemma-300M 潜变量-动作专家，以及 14.71M 个可训练 LoRA 参数。
- 在推理时，模型会把潜变量流和动作流一起去噪，然后只在机器人上执行动作流。

## 结果
- 在 MetaWorld MT50 上，摘要报告平均成功率从 $\pi_0$ 的 47.9% 提高到 OneWM-VLA 的 61.3%。在表 1 中，当时程 $H=30$ 时，OneWM-VLA 达到 53.13%，而 $\pi_0$ 为 37.98%，$\pi_{0.5}$ 为 26.83%。
- 在 LIBERO 上，OneWM-VLA 在 Spatial、Object、Goal 和 Long 四个设置上的平均成功率达到 98.1%。在 LIBERO-Long 上，它达到 95.6%，而 $\pi_0$ 为 85.2%，$\pi_{0.5}$ 为 92.4%。
- 在真实 Piper 机械臂上、清洁条件下，OneWM-VLA 在 Pick Banana、Fold Cloth 和 Pull Drawer 三个任务上的平均成功率达到 71.7%，而 $\pi_0$ 为 50.0%，$\pi_{0.5}$ 为 58.3%。
- 在真实 Fold Cloth 任务上，OneWM-VLA 在清洁条件下达到 60.0%，而 $\pi_0$ 为 20.0%，$\pi_{0.5}$ 为 25.0%。在观测噪声下，它达到 40.0%，而另外两者分别为 0.0% 和 10.0%。
- 论文报告了一个从每帧 1 到 12 个 token 的带宽扫掠；在匹配的训练预算下，随着 token 数增加，成功率下降。摘录没有给出这组扫掠的具体数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07931v3](https://arxiv.org/abs/2605.07931v3)
