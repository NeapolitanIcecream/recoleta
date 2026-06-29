---
source: arxiv
url: https://arxiv.org/abs/2605.22812v1
published_at: '2026-05-21T17:57:44'
authors:
- Wenxuan Guo
- Ziyuan Li
- Meng Zhang
- Yichen Liu
- Yimeng Dong
- Chuxi Xu
- Yunfei Wei
- Ze Chen
- Erjin Zhou
- Jianjiang Feng
topics:
- vision-language-action
- gesture-grounding
- robot-manipulation
- robot-data-scaling
- sim2real
- flow-matching
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# GesVLA: Gesture-Aware Vision-Language-Action Model Embedded Representations

## Summary
## 摘要
GesVLA 是一个面向杂乱场景机器人操作的手势感知视觉-语言-动作模型。它把指向手势和语言结合起来，识别目标并生成机器人动作。

## 问题
- 只有文本的 VLA 模型在场景中有多个相似物体、用户又给出“拿起这个”或“把它放到那里”这类指令时，可能会出错。
- 手势标注的机器人数据很少，因为真实的指向视频收集成本高，而且很难标出精确的目标位置。
- 这个问题很重要，因为目标定位出错会直接导致抓取错误、放置错误，以及更慢的人机交互。

## 方法
- GesVLA 用 MediaPipe 提取手部关键点，选取指向手停下来的关键帧，并把手腕和食指关键点投影成潜在空间中的手势 token。
- 双 VLM 设计把手势-语言意图推理和在线场景感知分开，同时通过交叉注意力传递缓存的潜在状态。
- 动作专家用 flow matching 去噪采样得到的动作轨迹，在 VLM 状态和机器人状态条件下生成连续机器人动作。
- 数据引擎把合成手部动作渲染到真实 RGB-D 场景图像上，并使用 GroundingDINO 的目标框和基于深度的 3D 目标点生成精确的指向标注。
- 训练分两阶段：先在约 1.6 万个半合成手势样本上训练意图 VLM，再冻结它，训练感知 VLM 和动作专家，数据来自真实机器人示教。

## 结果
- 在真实机器人操作任务上，GesVLA 在 3 个任务中的平均成功率达到 83.3%，而纯文本 VLA 为 31.7%，MLLM + VLA 为 31.7%，几何流程 + VLA 为 41.7%，解耦的 GesVLA 为 61.7%。
- 在 Pick-and-Place Block 任务上，GesVLA 的成功率是 95.0%，纯文本 VLA 是 45.0%；在难子集上分别是 9/10 和 3/10。
- 在 Select Jelly 任务上，GesVLA 的成功率是 75.0%，纯文本 VLA 是 35.0%；在难子集上分别是 6/10 和 3/10。
- 在 Select Fruit and Vegetable 任务上，GesVLA 的成功率是 80.0%，纯文本 VLA 是 15.0%；在难子集上分别是 8/10 和 1/10。
- 在一个包含 88 个样本的真实场景意图推理测试集上，GesVLA 的意图 VLM 准确率达到 94.3%，进度分数达到 97.2%；提示后的 Qwen3.5-plus 分别是 38.6% 和 61.4%，几何流程分别是 59.1% 和 78.4%。
- 这个意图模型使用 300 个 RGB-D 场景构建的半合成数据训练，并直接在至少有 7 个物体的真实场景上评估，支持论文对手势定位 sim-to-real 的结论。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22812v1](https://arxiv.org/abs/2605.22812v1)
