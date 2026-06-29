---
source: arxiv
url: https://arxiv.org/abs/2605.00438v1
published_at: '2026-05-01T06:15:43'
authors:
- Jinkun Liu
- Haohan Chi
- Lingfeng Zhang
- Yifan Xie
- YuAn Wang
- Long Chen
- Hangjun Ye
- Xiaoshuai Hao
- Wenbo Ding
topics:
- vision-language-action
- long-horizon-manipulation
- robot-foundation-model
- multimodal-reasoning
- visual-planning
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation

## Summary
## 总结
IVLR 为机器人策略加入了一条显式的全任务轨迹：每个阶段都有一个文本子目标和一个 RGB 关键帧。模型先生成这条轨迹并缓存起来，再结合实时相机观测来选择动作。

## 问题
- 长时程操作需要正确的步骤顺序和空间目标，但很多 VLA 策略把这条计划藏在模型激活中。
- 纯文本计划可以表达顺序，却容易漏掉姿态和接触细节；视觉预测能给出几何信息，却可能缺少预期的任务顺序。
- 这在多阶段任务里很关键，因为机器人可能因为处理物体的顺序不对，或把物体放错位置而失败。

## 方法
- IVLR 使用 Show-o2 1.5B 多模态 Transformer，根据初始图像和指令生成 IVLR-Trace。
- 每个轨迹阶段都配有一段说明和一个 RGB 关键帧：说明写出子目标，关键帧展示预期的视觉状态。
- 执行时，缓存的轨迹、原始指令和当前观测输入到 ACT token 和一个 MLP 动作解码器，后者在闭环中预测连续动作。
- 由于机器人数据集没有这类轨迹，作者用 Universal Visual Decomposer 对演示进行分段，取每个分段的端点作为关键帧，并用 Qwen3-VL 给各阶段生成说明，构造伪轨迹。
- 训练时把文本的 next-token loss、视觉关键帧的 flow-matching loss 和动作的 L1 loss 结合起来，并在训练中加入轨迹噪声和遮蔽。

## 结果
- 在 LIBERO 上，IVLR 的平均成功率为 95.5%，其中 LIBERO-Long 为 92.4%。对比基线包括 VLA-0 的平均 94.7% 和 Long 的 87.6%，CoT-VLA 的平均 81.1% 和 Long 的 69.0%，以及 π0-FAST 的平均 85.5% 和 Long 的 60.2%。
- LIBERO 的轨迹消融显示，长时程任务上的主要影响很明显：没有轨迹时 Long 为 37.7%，仅文本为 62.0%，仅视觉为 68.4%，完整 IVLR 为 92.4%。
- 在 SimplerEnv-WidowX 上，IVLR 的总体成功率为 59.4%，高于 SpatialVLA 的 42.7%、RoboVLMs 的 37.5% 和 Octo-Small 的 29.5%。
- LIBERO 上的压力测试显示，基础设置下平均成功率为 95.5%，执行偏移 2 cm 后为 92.1%，文本轨迹遮蔽 30% 后为 92.2%，视觉关键帧遮蔽 30% 后为 90.0%。
- 这个方法有前置成本：完整轨迹生成在一块 NVIDIA H20 GPU 上大约需要 10 秒，之后缓存执行以 10 Hz 运行，并带有动作分块。
- 论文只报告了仿真结果；它把静态、完全可观测环境、陈旧或错误的全局计划，以及初始规划延迟列为当前限制。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00438v1](https://arxiv.org/abs/2605.00438v1)
