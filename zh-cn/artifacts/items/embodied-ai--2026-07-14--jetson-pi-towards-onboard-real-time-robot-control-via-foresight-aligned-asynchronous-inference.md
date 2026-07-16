---
source: arxiv
url: https://arxiv.org/abs/2607.12659v1
published_at: '2026-07-14T11:38:36'
authors:
- Zebin Yang
- Qi Wang
- Yunhe Wang
- Xiurui Guo
- Bo Yu
- Shaoshan Liu
- Jiafeng Xu
- Hao Dong
- Meng Li
topics:
- vision-language-action
- robot-foundation-model
- edge-inference
- asynchronous-control
- robotic-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference

## Summary
## 摘要
Jetson-PI 通过将异步动作预测与未来环境对齐，并优化边缘推理，使低功耗设备上的 VLA 控制更快。在 NVIDIA Jetson Orin 上，据报告，其控制频率最高达到朴素 PyTorch 的 8.66×、vla.cpp 的 5.41×，同时在 LIBERO 上的成功率高于 VLASH。

## 问题
- 对低功耗机载硬件而言，VLA 推理速度过慢：论文报告称，π₀.₅ 在 Jetson Orin 上每次推理约需 1.4 秒，即 0.7 Hz。
- 异步推理可以消除等待，但会基于过时的观测预测动作，从而在环境变化时造成感知—执行错位和反应延迟。
- 这一问题很重要，因为高端 GPU 会增加功耗，并可能缩短机器人的电池续航；论文报告称，与 Jetson Orin 等机载设备相比，使用 RTX 4090 会使电池续航缩短 6.0 倍。

## 方法
- 一个包含 4000 万参数的未来校正模块，根据当前表示和已提交执行的动作，预测压缩后的未来 VLM 表示。
- 动作专家利用该预测的未来表示，为推理完成时对应的时间点生成动作，而不是基于过时的观测采取行动。
- 基于置信度的调度会在预测的未来表示可靠时跳过 VLM 调用，并在置信度低于阈值时调用 VLM，同时允许动作专家更频繁地运行。
- 边缘推理系统采用 CUDA 图复用、GPU 驻留的中间缓冲区和流匹配图展开，以减少 Jetson 硬件上的通信开销和重复图启动开销。

## 结果
- 在 Jetson Orin 上，据报告，控制频率相比朴素 PyTorch 提高 8.66×，相比 vla.cpp 提高 5.41×；摘要还报告称，在 LIBERO 上，平均成功率相比 VLASH 提高 14.8%。
- 在 Orin 消融实验中，朴素 π₀.₅ 的控制频率为 0.70 Hz，总延迟为 1,420.8 ms；加入调度后，反应时间降至 674.9 ms，频率升至 1.48 Hz；加入图复用、缓冲和展开后，频率达到 6.06 Hz，总延迟为 412.9 ms。
- 在 LIBERO 上使用 π₀.₅、覆盖 Δ=1–9 的延迟设置时，未来校正在 LIBERO-Spatial、LIBERO-Object、LIBERO-Goal 和 LIBERO-10 上的平均成功率分别为 97.0%、98.0%、96.5% 和 92.2%；加入调度后，这些数值分别升至 97.4%、98.6%、96.8% 和 92.5%。
- 报告中的实验涵盖 Jetson Orin 和 Thor 上的仿真与真实机器人部署，但所提供的摘录不包括完整的 Thor 延迟表或详细的真实机器人指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.12659v1](https://arxiv.org/abs/2607.12659v1)
