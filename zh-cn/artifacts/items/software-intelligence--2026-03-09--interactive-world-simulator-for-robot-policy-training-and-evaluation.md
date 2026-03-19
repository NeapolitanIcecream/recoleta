---
source: arxiv
url: http://arxiv.org/abs/2603.08546v1
published_at: '2026-03-09T16:13:32'
authors:
- Yixuan Wang
- Rhythm Syed
- Fangyu Wu
- Mengchao Zhang
- Aykut Onol
- Jose Barreiros
- Hooshang Nayyeri
- Tony Dear
- Huan Zhang
- Yunzhu Li
topics:
- world-models
- robot-learning
- video-prediction
- imitation-learning
- policy-evaluation
relevance_score: 0.46
run_id: materialize-outputs
language_code: zh-CN
---

# Interactive World Simulator for Robot Policy Training and Evaluation

## Summary
该论文提出 Interactive World Simulator（IWS），一种面向机器人策略训练与评估的交互式世界模型，强调在消费级单卡上实现长时稳定、物理一致的视频级仿真。其核心价值在于用中等规模真实交互数据训练出可交互的替代环境，用于低成本生成示范数据和可复现地评测策略。

## Problem
- 现有动作条件视频预测/世界模型常常**太慢**，或在长时 rollout 中**逐步漂移失稳**，难以支持真实可用的机器人训练与评估。
- 这很重要，因为机器人模仿学习依赖大量真实示范，采集昂贵；而真实世界评测又慢、难复现、难做公平对比。
- 目标是构建一个仅基于 **RGB 图像+动作** 训练的交互式仿真器，既快又稳定，还能逼真反映真实机器人-物体交互。

## Approach
- 采用**两阶段 latent world model**：先把图像压缩到紧凑 2D latent，再只在 latent 空间预测未来，从而降低计算开销并提升长时稳定性。
- 第 1 阶段训练自编码器：用 CNN 编码器提取 latent，用**consistency-model 解码器**做高保真、少步数图像重建。
- 第 2 阶段冻结自编码器，训练一个**动作条件 latent dynamics consistency model**，根据过去 latent 和动作预测下一帧 latent；模型用 3D 卷积、FiLM 调制和时空注意力建模多模态未来。
- 推理时采用**自回归滑动窗口**生成长时视频，并向上下文注入小噪声，让模型学会容忍“自己预测自己”带来的误差累积。
- 在应用层，作者直接在世界模型内进行人类遥操作采集示范，并把生成数据无缝用于 DP、ACT、π0、π0.5 等模仿学习策略训练，同时也让策略闭环在仿真器中做可复现评测。

## Results
- **长时稳定与速度**：模型可在**单张 RTX 4090** 上以 **15 FPS** 持续交互仿真**超过 10 分钟**；论文还称 mug grasping 任务模型大小仅 **176.02 MB**，训练耗时约 **6 小时（stage 1）+ 12 小时（stage 2）**，均在单张 H200 上完成。
- **视频预测指标全面优于基线**：在 7 个任务聚合、**192 步长时预测**设置下，IWS 相比 DINO-WM/UVA/Dreamer4/Cosmos 取得更好指标：**MSE 0.005**（vs 0.028/0.023/0.012/0.019），**LPIPS 0.051**（vs 0.270/0.272/0.163/0.224），**FID 63.50**（vs 200.77/142.55/239.97/200.74），**PSNR 25.82**（vs 17.79/17.87/20.81/18.91），**SSIM 0.831**（vs 0.652/0.650/0.693/0.647），**UIQI 0.960**（vs 0.875/0.884/0.919/0.883），**FVD 243.20**（vs 1752.57/2213.29/1747.26/799.34）。
- **数据生成用于模仿学习**：作者在从 **100% 仿真数据到 100% 真实数据** 的不同混合比例下训练 DP、ACT、π0、π0.5，声称**各比例下策略表现可比**，说明世界模型生成示范与同规模真实示范质量接近；但摘录中**未给出具体成功率数字**。
- **策略评测有效性**：作者报告在多个任务和训练 checkpoint 上，**仿真器内表现与真实世界表现呈强相关**，因此可用于可扩展、可复现的策略评估；但摘录中**未给出相关系数等具体数值**。
- **数据规模与任务覆盖**：实验覆盖 **1 个 MuJoCo 任务 + 6 个真实机器人任务**，真实任务每个约 **600 个 episode × 200 steps**，涉及刚体、可变形体、关节物体、物体堆及多物体交互，表明方法适用面较广。

## Link
- [http://arxiv.org/abs/2603.08546v1](http://arxiv.org/abs/2603.08546v1)
