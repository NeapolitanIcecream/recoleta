---
source: arxiv
url: https://arxiv.org/abs/2607.04927v1
published_at: '2026-07-06T10:57:01'
authors:
- Jian Zhu
- Jianjun Zhang
- Taiyi Su
- Tianbin Liu
- Zhangyuan Wang
- Kai Xie
- Zitai Huang
- Chong Ma
- Youzhang He
- Tianjian Wang
- Hanyang Wang
- Weihao Ding
- Yi Xu
topics:
- world-action-model
- vision-language-action
- robot-foundation-policy
- deformable-manipulation
- real-time-robot-control
- subtask-planning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DSWAM: A Dual-System World Action Foundation Model for Fine-Grained Robot Manipulation

## Summary
## 摘要
DSWAM 将 World Action Model 执行器与可选的视觉-语言子任务规划器配对，用于细粒度机器人操作。论文称，在匹配的 VLA 基线对比中，它在真实折叠任务上的执行表现更强，并在广泛的仿真双臂任务中取得较高成功率。

## 问题
- WAM 机器人策略可以建模物理场景变化，但通常缺少显式语言接口，难以把粗粒度家务指令转成可执行子任务。
- 当论文使用不同机器人、数据、任务和成功判定规则时，VLA 与 WAM 的机器人结果很难比较。
- 这个问题很重要，因为家务操作常常同时需要接触丰富的执行能力和简单的任务分解，尤其是在处理可变形物体和多步骤目标时。

## 方法
- System 1 是默认 WAM 执行器。它接收多视角 RGB 图像、语言和本体感知信息，然后预测连续的双臂动作块。
- System 2 是基于 Rynnbrain4B 风格模型的视觉-语言规划器。它查看以 1 Hz 采样的最近 5 帧和全局提示，然后输出下一个可执行子任务或 `done`。
- 执行器使用动作预测和视频协同训练，并采用 flow-matching 损失，因此未来视觉 token 会在训练期间提供物理动态信息。
- 推理时，执行器直接预测动作，不生成未来视频，从而降低延迟，并避免控制依赖生成帧。
- 部署时加入实时分块、异步执行和 TensorRT BF16 加速，使策略查询不会中断机器人控制。

## 结果
- 在匹配的 DeMaVLA 真实世界折叠基准上，DSWAM 将平均成功率从 92.5% 提高到 96.3%，并将平均完成时间从 2'18" 降到 1'44"。该对比中禁用了 System 2 规划器。
- 折叠基准使用 ALOHA 风格双臂机器人，覆盖 4 类衣物、每类 2 个实例、每个实例 10 次试验，并与 DeMaVLA 使用相同平台、数据、任务协议和成功标准。
- 在 RoboTwin 2.0 上，DSWAM 报告其在干净任务上的平均成功率为 92.38%，在 50 个双臂操作任务中、随机物体姿态和场景布局下的平均成功率为 91.90%。
- 在 System 2 分拣研究中，子任务监督通过提高成功率和减少 rollout 错误来改善真实世界执行稳定性，但摘录未提供具体分拣数字。
- 论文报告称，BF16 TensorRT 与 PyTorch 的结果接近，同时降低了策略查询延迟，但摘录未给出延迟数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04927v1](https://arxiv.org/abs/2607.04927v1)
