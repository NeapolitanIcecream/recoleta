---
source: arxiv
url: https://arxiv.org/abs/2606.24448v1
published_at: '2026-06-23T11:35:13'
authors:
- Danze Chen
- Yanzhe Chen
- Qiming Huang
- Zhijun Cao
- Chen Gao
- Mike Zheng Shou
topics:
- vision-language-action
- robot-foundation-model
- synthetic-robot-videos
- geometry-supervision
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Supervise What Survives: Geometry-Guided VLA Adaptation from Synthetic Robot Videos

## Summary
## 摘要
GRA 使用合成机器人视频中的 2D 几何监督来适配 VLA 模型，动作只用真实机器人演示训练。在三个 Franka 抓取放置任务上，相同数据预算下的成功率从 Real-only 的 61.1% 提高到 68.9%，并超过伪动作基线。

## 问题
- VLA 策略需要成对的视频-动作数据，但真实遥操作速度慢，并且依赖具体硬件。
- 人到机器人的视频生成器可以生成看起来像机器人的视频，但不能提供可靠的电机命令。
- 先前的伪动作方法用从生成像素中恢复的动作来训练动作头；论文认为这会加入控制噪声，并降低真实机器人成功率。

## 方法
- GRA 只将生成视频用于空间几何监督。
- 它使用 Grounding DINO、SAM2、HaMeR、重定向、MuJoCo 仿真和校准相机投影，从源人类视频中提取未来 2D 末端执行器路标点。
- 阶段 1 在每个任务 75 个生成视频上训练 OpenVLA-OFT 视觉主干和一个 3 层 MLP 2D 路标点头，训练 5K 步；语言模型和动作头不参与训练。
- 阶段 2 在每个任务 25 个真实演示上训练动作头 10K 步，使用 L1 增量动作损失，同时在真实帧上使用路标点损失，使视觉特征保持与末端执行器几何相关。
- 动作输出是一个包含 24 步的 7D 增量动作块；路标点时间范围为 K=8。

## 结果
- 在 3 个真实 Franka 任务上，每个任务 30 次试验，GRA 在每个任务使用 25 个真实演示和 75 个生成视频时达到 68.9% 的平均成功率；Real-only 为 61.1%，DreamGen 风格伪动作为 48.9%，MimicDreamer 风格重定向伪动作为 54.4%。
- 按任务看，GRA 在 cube→pad 上为 66.7%，在 cup→coaster 上为 56.7%，在 mango→plate 上为 83.3%；Real-only 分别为 60.0%、46.7% 和 76.7%。
- 100-demo Real-only 参考达到 75.6% 的平均成功率。GRA 将相对该参考的差距从 14.5 个百分点缩小到 6.7 个百分点，同时真实演示用量为其 1/4。
- 冻结探针诊断显示，生成到真实的迁移在增量动作上比在路标点上差得多：在阶段 1 主干上，路标点误差为 0.41σ，增量动作误差为 1.38σ。
- 教师强制动作评估报告中，GRA 的位置误差为 9.26 mm，总 L1 误差为 0.060，优于 Real-only 的 11.09 mm 和 0.090，也优于 MimicDreamer 风格方法的 13.36 mm 和 0.071。
- 在 cup→coaster 消融实验中，完整 GRA 达到 56.7% 成功率；移除阶段 1 后为 43.3%，移除路标点锚定后为 46.7%，用增量动作目标替代几何目标后为 36.7%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24448v1](https://arxiv.org/abs/2606.24448v1)
