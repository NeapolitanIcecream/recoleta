---
source: arxiv
url: https://arxiv.org/abs/2607.01088v1
published_at: '2026-07-01T15:45:08'
authors:
- Wenqi Jiang
- Jason Clemons
- Rowland O'Flaherty
- Hugo Hadfield
- Alperen Degirmenci
- Shuran Song
- Yashraj Narang
- Christos Kozyrakis
topics:
- robot-foundation-model
- robot-serving
- gpu-scheduling
- multi-robot-systems
- vision-language-action
- factory-automation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ROSA: A Robotics Foundation Model Serving System for Robot Factories

## Summary
## 摘要
Rosa 是面向机器人工厂中机器人基础模型的服务系统。它把多台机器人的模型请求路由到共享 GPU 池，并通过调度最大化符合 SLO 的动作吞吐量。

## 问题
- 机器人部署通常为每台机器人分配一个机载加速器或一台专用 GPU 服务器。机器人执行物理动作时，这会浪费 GPU 时间，也很难进行请求批处理。
- 工厂机器人需要的不只是单个动作模型：任务可能会调用 System 1 动作模型、System 2 规划器、安全模型和任务监控器，每个组件都有自己的延迟目标和调用频率目标。
- 论文认为，工厂服务应优化 SLO 约束下的加权机器人动作速率，因为更低的单请求延迟只有在改变任务进度或安全性时才有价值。

## 方法
- Rosa 为机器人集群使用共享的服务器 GPU 池，同时由机器人端计算保留高频控制和本地安全回退能力。
- 声明式任务文件指定机器人集群、模型组件、提示词、SLO、模型调用频率、重试规则，以及停止、重发、重新规划或呼叫人工等回退动作。
- 调度器使用画像数据、启发式方法和整数线性规划来选择模型放置、请求路由、批处理设置和每个任务的动作速率。
- 实现在 Ray Serve 上运行，并可调用 vLLM、PyTorch 和 JAX 后端来服务 GR00T-N1.6-3B、Qwen2.5-VL 变体等模型。

## 结果
- 在 8 块 NVIDIA H200 GPU 和最多 64 台虚拟机器人上，相比为每台机器人分配一块 GPU 或为每台机器人的每个模型分配一块 GPU 的专用服务基线，Rosa 将符合 SLO 的工厂生产率最高提高到 12.06 倍。
- 相比使用相同服务基础设施但不使用 Rosa 调度器的共享服务器基线，Rosa 将符合 SLO 的工厂动作吞吐量最高提高到 2.44 倍。
- 评测包括一台真实 Franka Panda 机器人，以及回放真实机器人观测的合成多机器人工作负载。
- 论文报告称，收益来自请求速率控制、跨模型组件的资源分配，以及由画像指导的批处理。
- 动机包括具体的硬件差距：NVIDIA B100 的内存带宽是 Jetson Thor 的 29 倍，FP8 算力是 Jetson Thor 的 3.5 倍；被引用的 Figure 02 机器人配有 2.25 kWh 电池，运行时间约 5 小时，双机载 RTX GPU 最高占用系统功耗的一半。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01088v1](https://arxiv.org/abs/2607.01088v1)
