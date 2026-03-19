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
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# LiteVLA-Edge: Quantized On-Device Multimodal Control for Embedded Robotics

## Summary
LiteVLA-Edge提出了一条面向嵌入式机器人的实用部署路径：把紧凑型视觉-语言-动作模型量化后，完整运行在Jetson Orin上做本地闭环控制。论文重点不是提出新策略学习目标，而是证明低延迟、离线、ROS 2兼容的多模态控制在边缘端可行。

## Problem
- 现有VLA模型常依赖>7B参数和桌面/云端GPU，难以满足嵌入式机器人在功耗、带宽和时延上的约束。
- 早期轻量化方案虽然能上边缘设备，但推理常是秒级，只能开环执行，无法对环境变化做及时反馈。
- 这很重要，因为现场机器人、断网/GPS拒止环境、战术或移动平台都要求本地、低时延、稳定的闭环控制。

## Approach
- 使用紧凑多模态骨干 **SmolVLM-256M**，把输入图像和语言指令直接映射为结构化动作token，再反量化为机器人控制量（如`Twist`速度命令）。
- 训练上采用监督式 image-to-action 微调：先用 **FP32** + **LoRA (r=8, α=8)** 保持动作精度，再做训练后 **4-bit GGUF量化（Q4_K_M）** 以适配边缘硬件。
- 部署上基于 **llama.cpp CUDA**，将 **42层** 全部卸载到 Jetson AGX Orin GPU；同时把上下文限制为 **512**、输出最多 **12 tokens**，减少KV cache开销。
- 系统以 **ROS 2** 模块化方式连接感知-推理-执行链路，保留安全覆盖、可调试性和与低层 **100 Hz** 控制器的兼容性。

## Results
- 在 **Jetson AGX Orin / Orin NX** 上，端到端本地推理达到 **150.5 ms** 平均时延，对应 **6.64 Hz / 约6.6 Hz** 的推理频率；论文称相对先前基线约有 **~220% improvement**。
- 连续运行中的时延抖动极低：标准差报告为 **0.125 ms**（表中为 **0.13 ms**），最小 **150.4 ms**、最大 **151.0 ms**，共 **300** 次测量。
- 与文中列举系统对比：**OpenVLA (7B, RTX 4090)** 仅 **partial ~5 Hz**；**EdgeVLA (~1B, A100-40GB)** 为 **~10 Hz**；**LiteVLA-Edge (256M, Jetson AGX Orin)** 达到 **6.6 Hz** 且完全本地闭环。
- 论文声称该频率已跨过闭环视觉伺服的实用门槛（文中给出 **6–10 Hz** 为闭环视觉运动控制入口区间），使机器人可在单次人类注意窗口内响应动态变化。
- 没有提供标准机器人任务基准上的成功率、泛化率或真实操作任务分数；最强的实证结论主要是**部署可行性、低延迟、低抖动和闭环运行稳定性**。

## Link
- [http://arxiv.org/abs/2603.03380v1](http://arxiv.org/abs/2603.03380v1)
