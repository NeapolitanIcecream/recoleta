---
source: arxiv
url: https://arxiv.org/abs/2604.27792v2
published_at: '2026-04-30T12:34:44'
authors:
- MotuBrain Team
- Chendong Xiang
- Fan Bao
- Haitian Liu
- Hengkai Tan
- Hongzhe Bi
- James Li
- Jiabao Liu
- Jingrui Pang
- Kiro Jing
- Louis Liu
- Mengchen Cai
- Rongxu Cui
- Ruowen Zhao
- Runqing Wang
- Shuhe Huang
- Yao Feng
- Yinze Rong
- Zeyuan Wang
- Jun Zhu
topics:
- world-action-model
- vision-language-action
- robot-foundation-model
- real-time-robot-control
- multiview-manipulation
- robot-data-scaling
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# MotuBrain: An Advanced World Action Model for Robot Control

## Summary
## 摘要
MotuBrain 是一个统一的世界行动模型，用一个基于扩散的模型同时预测机器人动作和未来视觉状态。它面向实时机器人控制，把视频、动作和语言流结合起来，并支持多视角输入和更快的推理栈。

## 问题
- 视觉-语言-动作策略往往直接把图像和指令映射到动作，因此可能忽略精细的时间动态，而这些动态对精确操作很重要。
- 两阶段的视频生成加逆动力学系统会先积累视频预测误差，再推断动作，这会降低控制精度。
- 大型世界行动模型推理速度慢，而机器人控制器需要低延迟的动作更新，尤其是在长时程和灵巧任务中。

## 方法
- 核心机制是一个 UniDiffuser 风格的联合模型，处理两个连续输出：未来视频潜变量和动作 token。同一个模型可以作为策略、世界模型、视频生成器、逆动力学模型，或联合视频-动作预测器运行。
- MotuBrain 使用三个 Transformer 流，分别处理文本、视频和动作。视频流和动作流学习流匹配目标，文本通过注意力同时条件化这两个流。
- 它使用 H-bridge 注意力：完整的视频-动作联合注意力只出现在 Transformer 层中间的 50%，而底部 25% 和顶部 25% 使用分开的模态注意力来降低成本。
- 多视角输入先按摄像头用 Vidu VAE 编码，再在 token 层级结合视角相关的 3D RoPE 空间偏移。这支持不同的摄像头布局，而不需要改动骨干网络。
- 训练按顺序使用大规模视频数据、第一人称和机器人数据，再到目标形态数据。动作使用相对末端执行器坐标，每个末端执行器动作有 10 个维度，包括位置、6D 旋转和夹爪状态。

## 结果
- 在 RoboTwin 2.0 上，MotuBrain 在干净设置下的平均成功率为 95.8%，在随机化设置下为 96.1%。
- RoboTwin 2.0 的随机化得分超过 95%，作者用这一点作为模型能处理视觉和任务变化的证据。
- 在 WorldArena 上，论文声称它在比较对象中取得了最高的 EWMScore，但摘要没有给出具体数值。
- 推理栈把端到端延迟从 4.90 秒降到 0.09 秒，把频率从 0.20 Hz 提升到 11.11 Hz，相比朴素基线快 54.4 倍。
- 步数减少把扩散采样从 50 步降到 30 步；作者报告说在优化整个栈后，RoboTwin 2.0 的成功率变化不到 1 个百分点。
- 论文声称，该模型可以用 50 到 100 条同一形态的轨迹适应新的类人形态，并且在不额外加入 VLM 规划器、双系统分解、外部记忆或重试专用数据的情况下，完成长时程和灵巧操作任务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27792v2](https://arxiv.org/abs/2604.27792v2)
