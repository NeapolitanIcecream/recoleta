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
## 总结
本文测量了 Vision-Language-Action 在 GPU、NPU 和 XPU 上的推理表现，并加入了两个面向机器人部署的低时延优化。其核心观点是，机器人加速器的最佳选择取决于时延、成本和能耗，而不只是峰值 GPU 速度。

## 问题
- VLA 机器人策略必须运行在闭环的 observe-infer-act 流程中；过高的时延会导致抖动、振荡或任务失败。
- 大多数 VLA 评测使用 RTX 4090 这类桌面级 GPU，掩盖了移动机器人上的成本、能耗、显存和控制频率限制。
- 模型大小并不能单独预测时延：Diffusion Policy 可能比更大的 pi0 更慢，因为它使用 100 个去噪步，而 pi0 只用 4 个。

## 方法
- 论文为 VLA 组合建立了模型-硬件排行榜，并用 CET 对它们排序：成本、能耗和时间。
- 论文在 RTX 4090、Jetson Thor、AGX Orin、Intel B60 Pro 和 Ascend NPU 上分析 VLA 推理，并在排序前加入 VRAM 和控制频率筛选条件。
- 论文识别出两个反复出现的阶段：计算受限的 VLM 骨干网络和内存受限的 Action Expert。
- DP-Cache 复用迭代扩散中的稳定中间计算，减少重复去噪工作。
- V-AEFusion 用异步流水线并行，让 VLM 和 Action Expert 阶段重叠执行。

## 结果
- 对 pi0，排行榜给出的结果是：RTX 4090 为 102.3 ms 和 2.398 kJ，Jetson Thor 为 246.0 ms 和 1.282 kJ，AGX Orin 为 920.6 ms 和 1.866 kJ，Intel B60 Pro 为 306.5 ms 和 6.363 kJ，Ascend 310P 为 818.0 ms 和 2.618 kJ。
- 对 pi0 的分析显示，VLM 骨干网络通常超过 90% 的 SM 利用率，而 Action Expert 的 SM 利用率约为 20% 到 40%，耗时约为 VLM 的 2 倍。
- Roofline 分析显示，pi0 的 VLM DecoderLayer 强度接近 840 FLOPs/Byte，高于 RTX 4090 的拐点 330 FLOPs/Byte，因此它属于计算受限；Action Expert 为 64.5 FLOPs/Byte，因此在 RTX 4090、Jetson Thor 和 AGX Orin 上都属于内存受限。
- 编译后，pi0 在 RTX 4090 上从 102.3 ms 提速到 35.2 ms，提升 2.90 倍，频率达到 28.41 Hz；在 Jetson Thor 上从 246.0 ms 提速到 163.0 ms，提升 1.51 倍，频率达到 6.13 Hz；在 Ascend 310P 上从 818.0 ms 提速到 350.0 ms，提升 2.34 倍，频率达到 2.86 Hz。
- 在 OpenVLA 上，Speculative plus Cache 达到 1.29 倍加速和 6.99 Hz，但 LIBERO 的平均成功率从 76.5% 的基线降到 68.5%。
- 论文声称，DP-Cache 和 V-AEFusion 在 GPU 上最高可达到 2.9 倍加速，在边缘 NPU 上最高可达到 6 倍加速，同时任务成功率只会小幅下降。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24447v1](https://arxiv.org/abs/2604.24447v1)
