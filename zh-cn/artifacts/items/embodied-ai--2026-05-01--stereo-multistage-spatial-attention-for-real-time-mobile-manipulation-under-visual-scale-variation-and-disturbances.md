---
source: arxiv
url: https://arxiv.org/abs/2605.00471v1
published_at: '2026-05-01T07:18:11'
authors:
- Xianbo Cai
- Hideyuki Ichiwara
- Hyogo Hiruma
- Masaki Yoshikawa
- Hiroshi Ito
- Tetsuya Ogata
topics:
- mobile-manipulation
- stereo-vision
- spatial-attention
- imitation-learning
- recurrent-policy
- visual-disturbance
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Stereo Multistage Spatial Attention for Real-Time Mobile Manipulation Under Visual Scale Variation and Disturbances

## Summary
## 摘要
Stereo Multistage Spatial Attention 通过跟踪双目图像中的任务相关点，并将这些点输入循环动作预测器，在相机视角变化下提升了真实环境中的移动操作表现。在 4 个机器人任务中，该方法在相同的 10 Hz 控制设置下报告的成功率高于 ACT、Diffusion Policy、π0 和 SmolVLA。

## 问题
- 移动机械臂使用机载相机，因此机器人移动时，物体的大小、位置和可见性会变化。这些尺度变化可能让基于视觉的动作预测变得不稳定。
- 基于规则的视觉伺服和特征跟踪需要可靠的物体模型、特征或姿态估计；在遮挡、光照变化和纹理不足时，这些条件可能失效。
- 大型模仿学习模型和 VLA 模型可能需要更多数据和计算资源，超出小型机载实时控制器的承受范围。

## 方法
- 该方法输入左、右 RGB 图像和机器人电机状态，然后预测下一个机器人电机命令和下一个注意力点位置。
- 双目多阶段空间注意力模块从每张图像中提取 6 个任务相关注意力点。它使用 3 个 CNN 阶段，将每个阶段与输入图像的关键特征进行比较，对注意力图取平均，并使用温度为 0.001 的 soft-argmax。
- 左、右图像流之间的权重共享促使两个视角关注匹配的物体或机器人部件。
- 分层 LSTM 分别在低层 LSTM 中处理左侧注意力点、右侧注意力点和机器人状态，然后在高层 LSTM 中合并它们的单元状态，用于闭环运动预测。
- 训练使用关节状态预测损失、权重为 0.1 的运动平滑项，以及双向注意力点预测损失；该损失系数从 0.0001 升至 0.1。

## 结果
- 在 4 个真实环境任务中，每个任务进行 50 次随机试验，完整的双目 MSA 模型达到 85.0% 的平均成功率，99% CI 为 77.4 到 90.4。基线结果为：ACT 46.0%，Diffusion Policy 28.5%，π0 3.5B 29.0%，SmolVLA 0.45B 12.5%。
- 所提方法在各最终任务上的成功率为：Place Coffee 72.0%，Open Microwave 98.0%，Take Kettle 92.0%，Retrieve Clothing 78.0%。
- 消融实验显示，双目 MSA 设计对结果有影响：双目 MSA 的平均成功率为 85.0%，双目单阶段空间注意力为 37.5%，单目 MSA 为 33.0%。
- 在 560 次视觉干扰测试中，所提方法的总体成功率为 76.8%，ACT 为 24.8%，ACT 加提取的注意力点为 39.6%。
- 在干扰条件下，该方法在 Open Microwave 任务中取得的成功率为：有视觉干扰物时 100.0%，低光照时 86.7%，未见过背景时 93.3%。ACT 在相同 Open Microwave 条件下的得分分别为 6.7%、26.7% 和 3.3%。
- 数据集每个任务使用 54 条成功示范，序列长度为 15 s、频率为 10 Hz，双目 RGB 图像尺寸为 3×128×256×2，机器人包含 9-DoF 右臂和 4-DoF 移动底盘。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00471v1](https://arxiv.org/abs/2605.00471v1)
