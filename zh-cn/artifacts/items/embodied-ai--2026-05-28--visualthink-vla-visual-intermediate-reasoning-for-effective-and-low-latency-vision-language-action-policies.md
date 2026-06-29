---
source: arxiv
url: https://arxiv.org/abs/2605.30011v1
published_at: '2026-05-28T14:36:53'
authors:
- Mingjian Gao
- Wenqiao Zhang
- Yuqian Yuan
- Yang Dai
- Binhe Yu
- Zheqi Lv
- Haoyu Zheng
- Jiaqi Zhu
- Zhiqi Ge
- Zixuan Wan
- Siliang Tang
- Yueting Zhuang
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- visual-reasoning
- robot-data-scaling
- low-latency-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies

## Summary
## 摘要
VisualThink-VLA 为 VLA 策略加入稀疏视觉证据 token，使其能进行中间视觉推理，并把动作延迟控制在亚秒级。它针对机器人控制中，文本思维链带来的延迟和较弱的视觉对齐问题。

## 问题
- 当操作需要物体对齐、空间关系、运动跟踪或长时程进度跟踪时，VLA 策略会失效。
- 文本思维链会增加多秒级的自回归延迟，这对闭环机器人控制来说太慢。
- 稠密的视觉侧输入会带来无关或冗余线索，干扰动作预测。

## 方法
- 该方法构建六个候选视觉证据通道：边界框、边缘、运动、关系、深度和分割。
- 通道筛选保留四个实际使用的通道：边界框、边缘、运动和关系；默认设置下舍弃深度和分割。
- 一个任务自适应路由器在每个决策步骤选择要使用的证据通道。
- Visual State Composer 将所选通道向量映射为可学习的视觉状态，并在动作解码前插入，同时保持 VLA 主干冻结。
- 训练使用软硬路由掩码、来自稠密 FullSoft 教师的蒸馏，以及由 754.7k 条视觉思维 VLA 指令生成的 VisualEvidence-Set 路由标签。

## 结果
- 在 BridgeData V2 上，VisualThink-VLA 报告每步 0.367 s、成功率 89.49%；ECoT 为 85.09% 和 8.377 s。论文报告延迟降低 22.8 倍。
- 与 BaseVLA 相比，它在 8 个主要基准中的 7 个上提升了成功率，包括 BridgeData V2 从 75.37% 提升到 89.49%，UT Austin MUTEX 从 41.09% 提升到 77.26%。
- 在 LIBERO 上，它在 Object、Goal、Spatial 和 Long 四项上分别报告 97.74%、97.05%、96.69% 和 95.87%，延迟在 0.345 s 到 0.421 s 之间。
- 与稠密的 FullSoft 变体相比，它在所有列出的基准上保持相近成功率，同时降低延迟；在 UT Austin MUTEX 上，成功率为 77.26% 对 77.10%，延迟为 0.451 s 对 0.551 s。
- 在主干可移植性测试中，加入 VisualThink-VLA 后，OpenVLA 的成功率提升 +16.37 个点，Octo 提升 +10.87，SmolVLA 提升 +11.95，延迟分别增加 0.050 s、0.077 s 和 0.104 s.

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30011v1](https://arxiv.org/abs/2605.30011v1)
