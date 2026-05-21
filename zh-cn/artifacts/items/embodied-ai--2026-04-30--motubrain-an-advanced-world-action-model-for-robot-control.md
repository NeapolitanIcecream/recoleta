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
MotuBrain 是一个统一的世界动作模型，用一个基于扩散的模型预测机器人动作和未来视觉状态。它通过结合视频、动作和语言流，支持多视角输入，并使用更快的推理栈，面向实时机器人控制。

## 问题
- 视觉-语言-动作策略通常把图像和指令直接映射到动作，因此可能遗漏精细操作所需的细粒度时间动态。
- 两阶段的视频生成加逆动力学系统可能在推断动作前累积视频预测误差，从而降低控制准确率。
- 大型世界动作模型的推理速度慢。机器人控制器在长程任务和灵巧操作任务中需要低延迟的动作更新，这一点会带来影响。

## 方法
- 核心机制是一个 UniDiffuser 风格的联合模型，覆盖两类连续输出：未来视频潜变量和动作 token。同一个模型可以作为策略、世界模型、视频生成器、逆动力学模型，或视频-动作联合预测器运行。
- MotuBrain 使用三个 Transformer 流处理文本、视频和动作。视频流和动作流学习流匹配目标，文本通过注意力为两个流提供条件。
- 它使用 H-bridge attention：完整的视频-动作联合注意力只出现在 Transformer 层的中间 50%，底部 25% 和顶部 25% 使用分离的模态注意力，以降低成本。
- 多视角输入按摄像头用 Vidu VAE 编码，然后通过带视角相关 3D RoPE 空间偏移的 token 级连接合并。这支持不同摄像头布局，而无需改变主干网络。
- 训练依次使用广泛视频数据、第一人称和机器人数据，再使用目标具身数据。动作使用相对末端执行器坐标，每个末端执行器动作有 10 个维度，包括位置、6D 旋转和夹爪状态。

## 结果
- 在 RoboTwin 2.0 上，MotuBrain 报告在 clean 设置中的平均成功率为 95.8%，在 randomized 设置中为 96.1%。
- randomized RoboTwin 2.0 分数高于 95%，作者用这一结果说明模型能够处理视觉和任务变化。
- 在 WorldArena 上，论文称其 EWMScore 是对比集合中已报告的最高值，但摘录未提供具体 EWMScore 数值。
- 推理栈把端到端延迟从 4.90 s 降到 0.09 s，并把频率从 0.20 Hz 提高到 11.11 Hz，相比朴素基线加速 54.4 倍。
- 步数减少把扩散采样从 50 步降到 30 步；作者报告，在使用优化栈后，RoboTwin 2.0 上的成功率变化低于 1 个百分点。
- 论文称，该模型能够用 50-100 条同具身轨迹适配新的人形具身，并且无需额外 VLM 规划器、双系统分解、外部记忆或重试专用数据，就能解决长程和灵巧操作任务。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.27792v2](https://arxiv.org/abs/2604.27792v2)
