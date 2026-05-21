---
source: arxiv
url: https://arxiv.org/abs/2604.24447v1
published_at: '2026-04-27T13:12:16'
authors:
- Kaijun Zhou
- Qiwei Chen
- Da Peng
- Zhiyang Li
- Xijun Li
- Jinyu Gu
topics:
- vision-language-action
- robot-foundation-models
- on-robot-inference
- edge-accelerators
- vla-acceleration
- hardware-profiling
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Characterizing Vision-Language-Action Models across XPUs: Constraints and Acceleration for On-Robot Deployment

## Summary
## 摘要
本文测量了 Vision-Language-Action 推理在 GPU、NPU 和 XPU 上的表现，并为机器人本体使用加入两项延迟优化。主要结论是：最佳机器人加速器取决于延迟、成本和能耗，单看 GPU 峰值速度不够。

## 问题
- VLA 机器人策略必须在闭环的观察-推理-行动流程内运行；高延迟可能导致卡顿、振荡或任务失败。
- 大多数 VLA 评估使用 RTX 4090 等桌面级 GPU，这会掩盖移动机器人上的成本、能耗、内存和控制频率限制。
- 仅靠模型大小无法预测延迟：Diffusion Policy 可能比更大的 pi0 更慢，因为它使用 100 个去噪步骤，而 pi0 使用 4 个。

## 方法
- 论文为 VLA 模型-硬件组合构建排行榜，并用 CET 对其排名：成本、能耗和时间。
- 它在 RTX 4090、Jetson Thor、AGX Orin、Intel B60 Pro 和 Ascend NPU 上分析 VLA 推理，并在排名前加入 VRAM 和控制频率筛选。
- 它识别出两个反复出现的阶段：受计算限制的 VLM 骨干网络，以及受内存限制的 Action Expert。
- DP-Cache 在迭代扩散中复用稳定的中间计算，以减少重复的去噪工作。
- V-AEFusion 通过异步流水线并行，让 VLM 和 Action Expert 阶段重叠执行。

## 结果
- 对于 pi0，排行榜报告 RTX 4090 为 102.3 ms 和 2.398 kJ，Jetson Thor 为 246.0 ms 和 1.282 kJ，AGX Orin 为 920.6 ms 和 1.866 kJ，Intel B60 Pro 为 306.5 ms 和 6.363 kJ，Ascend 310P 为 818.0 ms 和 2.618 kJ。
- 对 pi0 的性能分析显示，VLM 骨干网络通常高于 90% SM 利用率，而 Action Expert 的 SM 利用率约为 20% 到 40%，延迟约为 VLM 的 2 倍。
- Roofline 分析报告称，pi0 VLM DecoderLayer 的强度接近 840 FLOPs/Byte，高于 RTX 4090 的 ridge point 330 FLOPs/Byte，因此受计算限制；Action Expert 为 64.5 FLOPs/Byte，因此在 RTX 4090、Jetson Thor 和 AGX Orin 上受内存限制。
- 编译后，pi0 在 RTX 4090 上从 102.3 ms 加速到 35.2 ms，提升 2.90x，达到 28.41 Hz；在 Jetson Thor 上从 246.0 ms 加速到 163.0 ms，提升 1.51x，达到 6.13 Hz；在 Ascend 310P 上从 818.0 ms 加速到 350.0 ms，提升 2.34x，达到 2.86 Hz。
- 在 OpenVLA 上，Speculative plus Cache 达到 1.29x 加速和 6.99 Hz，但平均 LIBERO 成功率从 76.5% 基线降至 68.5%。
- 论文称，DP-Cache 和 V-AEFusion 在 GPU 上最高达到 2.9x 加速，在边缘 NPU 上最高达到 6x 加速，任务成功率仅有小幅下降。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24447v1](https://arxiv.org/abs/2604.24447v1)
