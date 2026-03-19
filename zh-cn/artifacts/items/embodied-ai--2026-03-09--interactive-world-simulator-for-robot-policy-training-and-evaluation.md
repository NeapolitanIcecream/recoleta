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
- world-model
- robot-policy-training
- policy-evaluation
- action-conditioned-video-prediction
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Interactive World Simulator for Robot Policy Training and Evaluation

## Summary
本文提出 Interactive World Simulator（IWS），一种面向机器人策略训练与评估的交互式世界模型。它用中等规模真实机器人交互数据学习可动作条件的视频预测，并在单张消费级 GPU 上实现长时稳定交互。

## Problem
- 现有机器人世界模型往往**太慢**，常依赖重型扩散采样，难以支持实时交互与大规模数据生成。
- 现有方法还常在**长时滚动预测**中失稳，误差累积导致机器人姿态漂移、物体交互不一致，难用于可靠策略训练和评估。
- 这很重要，因为机器人模仿学习和策略迭代高度依赖大量数据与频繁评测，而真实机器人采集/评估昂贵、缓慢且难复现。

## Approach
- 核心思路是把图像先压缩到**2D 潜变量空间**，再只在潜空间里做动作条件未来预测，最后再解码回像素，从而更快更稳。
- 方法分两阶段：先训练**CNN 编码器 + consistency-model 解码器**的自编码器，获得高保真重建；再冻结自编码器，训练一个**动作条件 consistency latent dynamics model** 预测下一帧潜变量。
- 动力学模型把过去若干帧潜变量和动作作为上下文，对“最后一帧的带噪潜变量”去噪，学习多模态未来；网络实现为带 **3D conv、FiLM、时空注意力** 的结构。
- 为了支持长时 rollout，推理时采用**自回归滑动窗口**，并在训练中给上下文注入小噪声，提高模型对“自己预测作为后续输入”这种误差传播的鲁棒性。
- 该世界模型可直接用于两类应用：在模拟器内遥操作收集示范数据训练 imitation policy，以及在模拟器中对策略做可复现评测。

## Results
- **长时交互与速度**：IWS 可在**单张 RTX 4090** 上以 **15 FPS** 稳定运行，支持**超过 10 分钟**的长时交互 rollout。
- **视频预测指标优于基线**：在 7 个任务聚合、**192 steps（19.2 秒）** 的动作条件预测上，IWS 达到 **MSE 0.005±0.005**、**LPIPS 0.051±0.019**、**FID 63.50±13.78**、**PSNR 25.82±2.72**、**SSIM 0.831±0.039**、**UIQI 0.960±0.019**、**FVD 243.20±103.58**；均优于 DINO-WM、UVA、Dreamer4、Cosmos（如 FVD 基线分别为 **1752.57、2213.29、1747.26、799.34**）。
- **任务覆盖**：实验涵盖 **6 个真实任务 + 1 个模拟任务**，包括刚体、可变形物体、关节物体、物体堆及多物体交互，平台为 **ALOHA 双臂机器人**。
- **数据效率与可获得性**：真实世界每个任务约收集 **600 episodes**、每条 **200 steps**，单人约 **6 小时/任务**；模拟任务用脚本策略生成 **10,000 episodes** 随机交互数据。作者声称中等规模数据即可训练出有效交互世界模型。
- **用于策略训练**：使用世界模型生成的数据训练 **DP、ACT、π0、π0.5** 等 imitation policies，在从 **100% 模拟器数据到 100% 真实数据** 的各种混合比例下，策略表现都与同等规模真实数据训练**可比**；但摘录中**未提供具体成功率数字**。
- **用于策略评估**：作者报告在多个任务和训练 checkpoint 上，模拟器内评测与真实世界表现存在**强相关**，可作为 faithful surrogate；但摘录中**未给出相关系数等定量数值**。

## Link
- [http://arxiv.org/abs/2603.08546v1](http://arxiv.org/abs/2603.08546v1)
