---
source: arxiv
url: http://arxiv.org/abs/2603.03380v1
published_at: '2026-03-03T03:20:52'
authors:
- Justin Williams
- Kishor Datta Gupta
- Roy George
- Mrinmoy Sarkar
topics:
- vision-language-action
- edge-robotics
- quantization
- on-device-inference
- ros2
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics

## Summary
LiteVLA-Edge提出了一条面向嵌入式机器人的实用部署路径：把紧凑型视觉-语言-动作模型量化后完整运行在Jetson Orin上，实现离线、低延迟、闭环控制。论文的重点不是提出新控制目标，而是证明本地多模态控制在边缘设备上的时序可行性与工程可复现性。

## Problem
- 现有VLA模型通常参数量大、依赖云端或桌面级GPU，难以在功耗受限、网络受限的机器人场景中本地部署。
- 早期轻量方案虽然能上边缘设备，但推理延迟常达秒级，只能开环执行，无法对动态环境快速反馈。
- 这很重要，因为机器人若不能在本地低延迟地产生动作，就难以在野外、战术、GPS受限或带宽受限环境中安全稳定运行。

## Approach
- 使用一个紧凑的SmolVLM-256M多模态骨干，将RGB图像和语言指令映射为结构化动作token，再反量化为机器人速度命令。
- 训练上采用监督式image-to-action微调，在FP32中用LoRA进行微调（rank=8, alpha=8），以保持动作精度。
- 部署上对训练后的模型做GGUF 4-bit后训练量化（Q4_K_M），以显著压缩模型并适配边缘设备内存与带宽限制。
- 推理时基于llama.cpp的CUDA后端，将42层全部卸载到Jetson AGX Orin GPU，设置n_ctx=512、最大输出12个token来降低KV-cache开销。
- 系统集成到ROS 2模块化感知-推理-执行流水线中，VLA以约6.6 Hz推理，底层控制器保持100 Hz心跳，从而兼顾语义推理与稳定执行。

## Results
- 在Jetson AGX Orin/Orin NX部署配置下，端到端平均推理延迟为**150.5 ms**，对应**6.64 Hz**推理频率；这是论文的核心定量结果。
- 延迟抖动极低：标准差约**0.125-0.13 ms**，最小**150.4 ms**，最大**151.0 ms**；作者据此声称系统具备确定性和低抖动的ROS 2闭环运行特性。
- 论文称相对先前基线达到约**220% improvement**，并把能力从多秒级开环推理推进到可用于闭环反应控制的约**150 ms**区间。
- 与表中系统对比：**LiteVLA-Edge 256M** 在 **Jetson AGX Orin** 上实现 **闭环 6.6 Hz**；**OpenVLA 7B** 依赖 **RTX 4090** 且仅 **partial ~5 Hz**；**EdgeVLA ~1B** 在 **A100-40GB** 上约 **10 Hz**。作者据此强调其在低功耗硬件上的“reasoning-to-Hz”平衡更优。
- 评测共报告**300次**总运行，并说明其中延迟统计来自热身后多轮闭环模拟；不过**没有提供任务成功率、真实机器人操作精度或标准基准数据集上的性能提升**，主要证据集中在部署时延与系统可运行性。

## Link
- [http://arxiv.org/abs/2603.03380v1](http://arxiv.org/abs/2603.03380v1)
