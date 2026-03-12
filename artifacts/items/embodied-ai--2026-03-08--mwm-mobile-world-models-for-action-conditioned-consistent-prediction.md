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
- world-model
- mobile-robot-navigation
- diffusion-model
- model-predictive-control
- consistency-distillation
relevance_score: 0.88
run_id: materialize-outputs
---

# MWM: Mobile World Models for Action-Conditioned Consistent Prediction

## Summary
MWM 是一个用于移动机器人导航的世界模型，重点解决“预测画面看起来合理，但与动作导致的真实轨迹不一致”的问题。它通过一致性后训练和面向推理的一致性蒸馏，让少步扩散推理仍能支持更可靠的规划。

## Problem
- 现有导航世界模型虽然能生成逼真的未来图像，但**未必与给定动作序列对应的真实未来一致**；多步 rollout 时误差会累积，误导 MPC 规划。
- 机器人在线部署需要**快速推理**，但常见少步扩散/蒸馏方法主要保分布相似性，**不显式保 rollout 一致性**，导致训练-推理不匹配。
- 这个问题重要，因为导航规划依赖 imagined trajectories；如果终点预测位置偏了，机器人会选错动作，直接影响成功率与安全性。

## Approach
- 提出两阶段训练：**Stage I 结构预训练**先用 teacher forcing 学习场景结构、几何和外观；**Stage II 的 ACC 后训练**再让模型在自回归 rollout 中使用自己的预测作为上下文，专门减少误差累积。
- ACC 的核心很简单：训练时不总喂真实上一帧，而是让模型“看自己生成的历史”，再用多帧 **LPIPS 感知损失**去拉近预测轨迹与真实观测轨迹。
- 为避免破坏第一阶段学到的高保真生成，后训练时**冻结主干 CDiT**，只更新注入动作/时间步信息的轻量 **AdaLN/LoRA** 层。
- 提出 **ICSD (Inference-Consistent State Distillation)**：把少步扩散蒸馏从“匹配输出分布”改成“保持动作条件一致性”，并通过一个与推理端点更一致的状态来缩小截断去噪带来的训练-推理差距。
- 规划阶段沿用基于 **CEM 的 MPC**，在世界模型 rollout 空间中搜索动作序列，并用终帧与目标图像的 LPIPS 相似度打分。

## Results
- **动作条件一致性（SCAND）**：MWM (DDIM 5) 在所有 rollout 时长都优于 NWM。比如 **16s DreamSim 0.337 vs 0.373 (NWM DDIM 25) vs 0.568 (NWM DDIM 5)**；**16s LPIPS 0.495 vs 0.569 vs 0.734**。作者概括为 DreamSim **降低 20.4%**。
- **视觉质量（SCAND FID）**：MWM (DDIM 5) 在多个 horizon 上也优于更慢的 NWM (DDIM 25)，如 **1s: 80.97 vs 96.68**，**8s: 85.80 vs 91.29**，**16s: 93.12 vs 93.63**；相对 NWM 的总体主张是 **FID 降低 17.5%**。
- **推理效率**：平均 rollout 时间 **2.3s**（MWM DDIM 5）vs **9.6s**（NWM DDIM 25）vs **2.6s**（NWM DDIM 5），即相对主基线至少 **4× 加速**，并把去噪步数从 25/250 级别压到 **5 步**。
- **导航性能（SCAND）**：MWM 达到 **ATE 1.14、RPE 0.302**，优于 **NWM 的 1.28 / 0.33**，也优于 GNM、NoMaD 等；作者总结为 **ATE 提升 10.9%**、**RPE 提升 8.5%**。
- **真实机器人部署**：论文声称相对基线实现 **成功率相对提升 50%**，以及 **导航误差降低 32.1%**。
- **最强具体结论**：MWM 表明，少步扩散如果显式围绕“动作条件 rollout 一致性”来训练，而不只是保单帧分布逼真度，就能同时提升规划可靠性、视觉保真度和实时性。

## Link
- [http://arxiv.org/abs/2603.07799v1](http://arxiv.org/abs/2603.07799v1)
