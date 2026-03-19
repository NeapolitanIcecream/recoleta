---
source: arxiv
url: http://arxiv.org/abs/2603.07799v1
published_at: '2026-03-08T20:54:50'
authors:
- Han Yan
- Zishang Xiang
- Zeyu Zhang
- Hao Tang
topics:
- world-models
- robot-navigation
- diffusion-models
- model-predictive-control
- consistency-distillation
relevance_score: 0.31
run_id: materialize-outputs
language_code: zh-CN
---

# MWM: Mobile World Models for Action-Conditioned Consistent Prediction

## Summary
MWM 是一种面向机器人导航的移动世界模型，目标是在给定动作序列时生成更一致、更可用于规划的未来视觉预测。它通过两阶段训练和面向推理的一致性蒸馏，在更快采样下同时提升预测质量、轨迹准确性和真实部署成功率。

## Problem
- 现有导航世界模型虽然能生成“看起来真实”的未来画面，但这些画面不一定与同一动作序列在真实世界中的结果一致，长时 rollout 会逐步漂移。
- 这种动作条件不一致会直接破坏基于 MPC/CEM 的规划，因为规划器会被“看似合理但实际错误”的想象轨迹误导。
- 扩散模型部署还需要少步推理加速，但已有蒸馏方法主要保分布相似性，未显式保留多步 rollout 一致性，导致训练-推理失配。

## Approach
- 提出 **两阶段训练**：先做 structure pretraining，用教师强制学习高保真场景结构和外观；再做 **ACC (Action-Conditioned Consistency) post-training**，让模型在训练时使用自己生成的历史预测作为上下文，减少测试时的误差累积。
- ACC 的核心很简单：不只训练“下一帧长得像”，而是训练“在连续执行这些动作时，整段预测轨迹都更贴近真实观察”。
- 在后训练中冻结主干 CDiT，仅更新轻量的 AdaLN/LoRA 调制层，以尽量保住第一阶段学到的图像细节，同时修正动作条件一致性。
- 提出 **ICSD (Inference-Consistent State Distillation)**：把少步扩散蒸馏做成“与真实推理状态对齐”的一致性蒸馏，缩小训练时截断状态与实际 few-step 推理终态之间的差距。
- 规划阶段沿用基于 CEM 的 MPC，在世界模型 rollout 空间中搜索动作序列，并用终帧与目标图像的感知相似度打分。

## Results
- 在 **SCAND** 上，MWM (DDIM 5) 相比 **NWM (DDIM 5)** 的动作条件一致性显著更好：例如 **16s DreamSim 0.337 vs 0.568**，**16s LPIPS 0.495 vs 0.734**；相对论文摘要中的总体表述，DreamSim 最多降低 **20.4%**。
- 甚至相较更慢的 **NWM (DDIM 25)**，MWM (DDIM 5) 仍更优：如 **1s DreamSim 0.244 vs 0.309**，**8s LPIPS 0.459 vs 0.540**，说明在更少采样步数下也能保持更一致的 rollout。
- 视觉保真度上，在 **SCAND FID** 中，MWM (DDIM 5) 优于 NWM：**1s 80.97 vs 96.68 (NWM DDIM 25)**，**8s 85.80 vs 91.29**；摘要称整体 **FID 降低 17.5%**。
- 推理效率上，平均 rollout 时间为 **2.3s**，相比 **NWM (DDIM 25) 的 9.6s** 约快 **4.2×**，也略快于 **NWM (DDIM 5) 的 2.6s**；文中还表述为至少 **4× speedup**，且 denoising steps 从默认 **250 降到 5**（至少 **80%+** 的步数削减）。
- 导航性能上，在 **SCAND** 的目标图像导航中，MWM 达到 **ATE 1.14, RPE 0.302**，优于 **NWM 的 ATE 1.28, RPE 0.33**，对应摘要中宣称 **ATE 提升 10.9%**、**RPE 提升 8.5%**。
- 真实世界部署上，摘要宣称相对基线实现 **成功率提升 50%**，并将 **navigation error 降低 32.1%**；这是论文最强的真实机器人结果主张。

## Link
- [http://arxiv.org/abs/2603.07799v1](http://arxiv.org/abs/2603.07799v1)
