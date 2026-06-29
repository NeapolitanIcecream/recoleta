---
kind: trend
trend_doc_id: 9
granularity: day
period_start: '2026-03-30T00:00:00'
period_end: '2026-03-31T00:00:00'
topics:
- robotics
- vision-language-action
- benchmarking
- world-models
- teleoperation
run_id: materialize-outputs
aliases:
- recoleta-trend-9
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/benchmarking
- topic/world-models
- topic/teleoperation
language_code: zh-CN
---

# 机器人学习工作对运行时瓶颈和脆弱评测越来越认真

## Overview
这一天的机器人论文都很务实。最强的工作同时收紧了 VLA 的执行和评测。FocusVLA 和 StreamingVLA 报告了操作质量和控制速度的提升，而 LIBERO-Para 和 ManipArena 在把措辞和真实世界设置变严格之后，让现有模型显得没那么成熟。关于世界模型、仿真和触觉遥操作的支撑性论文传达了同样的信息：更好的机器人性能依赖于从训练数据到运行时控制，全程保留与任务相关的信号。

## Clusters

### VLA papers are targeting attention quality and control latency
关于视觉-语言-动作模型的工作，重点放在执行中的具体瓶颈，而不只是更大的骨干网络。FocusVLA 通过把注意力强制集中到与任务相关的图像区域，并过滤噪声视觉通道，提升了操作表现。在 LIBERO 上，它在多权重设置下用 0.5B 模型取得 98.7% 的平均成功率，略高于几个更大的基线；消融实验也显示，把混合注意力换成级联注意力后，效果明显提升。StreamingVLA 处理的是部署延迟。它的异步流水线把观察、生成和执行重叠起来，在 AFM 下把每步动作时间从 74.5 ms 降到 33.7 ms，同时保持 97.1% 的 LIBERO 平均成功率，并把停顿间隔从 232.3 ms 降到 76.1 ms。AEO 变体把停顿间隔进一步压到 36.0 ms，但成功率降到 94.9%。

#### Evidence
- [FocusVLA: Focused Visual Utilization for Vision-Language-Action Models](../Inbox/2026-03-30--focusvla-focused-visual-utilization-for-vision-language-action-models.md): FocusVLA method and LIBERO results
- [StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation](../Inbox/2026-03-30--streamingvla-streaming-vision-language-action-model-with-action-flow-matching-and-adaptive-early-observation.md): StreamingVLA latency and halting-gap results

### Benchmarks are probing language robustness and real-world reasoning
评测工作对机器人模型真正理解了什么，要求越来越高。LIBERO-Para 表明，保留语义的改写仍然会明显打乱当前 VLA 系统：在七种设置下，当指令措辞变化时，成功率下降 22.8 到 51.9 个百分点，PRIDE 分数比原始成功率低 8.4% 到 22.0%，这说明只看二元任务完成会掩盖很多语言脆弱性。ManipArena 把实物世界里的测试面扩展了。它定义了 20 个真实任务，对每个参与者只提交一个共享实体上的端点，并加入受控的分布外试验以及匹配的真实到仿真资产。这个结论很直接：窄设置下的排行榜数字，漏掉了语言鲁棒性和真实世界推理负担。

#### Evidence
- [LIBERO-Para: A Diagnostic Benchmark and Metrics for Paraphrase Robustness in VLA Models](../Inbox/2026-03-30--libero-para-a-diagnostic-benchmark-and-metrics-for-paraphrase-robustness-in-vla-models.md): Paraphrase robustness failures and PRIDE metric
- [ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation](../Inbox/2026-03-30--maniparena-comprehensive-real-world-evaluation-of-reasoning-oriented-generalist-robot-manipulation.md): Real-world evaluation protocol and benchmark scope

### Support layers are getting more control-aware and better synchronized
世界模型和基础设施论文都在强调训练和评测环境要保留策略所需的信号。WAM 给类似 DreamerV2 的世界模型加入动作预测，让潜在状态保留对控制有用的信息。在 CALVIN 上，它的视频预测指标超过 DreamerV2，经过 PPO 微调后，策略表现提升到 92.8%，而 DiWA 是 79.8%。CARLA-Air 解决的是堆栈的另一层：仿真连接。它把 CARLA 和 AirSim 放进同一个 Unreal Engine 进程，让空中和地面智能体共享同一个物理 tick 和渲染流水线，每帧传输开销低于 0.5 ms，并支持最多 18 种同步传感器模态。两篇论文都重视保真度，但层级不同：一篇关注潜在动力学，一篇关注仿真器时序和感知。

#### Evidence
- [Enhancing Policy Learning with World-Action Model](../Inbox/2026-03-30--enhancing-policy-learning-with-world-action-model.md): WAM method and CALVIN gains
- [CARLA-Air: Fly Drones Inside a CARLA World -- A Unified Infrastructure for Air-Ground Embodied Intelligence](../Inbox/2026-03-30--carla-air-fly-drones-inside-a-carla-world-a-unified-infrastructure-for-air-ground-embodied-intelligence.md): CARLA-Air single-process design and sensor synchronization

### Teleoperation hardware is pushing toward cheaper tactile data capture
灵巧遥操作仍然是一个活跃的数据采集问题。TAG 把 21 自由度磁式手部跟踪和每个指尖 32 个执行器的触觉阵列结合起来，目标是在不依赖昂贵硬件的情况下提高接触丰富的示范质量。报告中的工程指标很强：亚度级跟踪误差、1000 秒约 0.02° 的漂移，以及在所报告设置下，比商用 Manus 手套更好的电磁干扰耐受性。论文还把成本控制在 500 美元以下，如果这些手套要走出单个实验室装置，这一点很重要。摘要节选没有给出完整的下游学习指标，所以这里的主要结论是硬件已经足够好，能更好地采集示范数据，但还不能据此认定策略质量已经提升。

#### Evidence
- [Feel Robot Feels: Tactile Feedback Array Glove for Dexterous Manipulation](../Inbox/2026-03-30--feel-robot-feels-tactile-feedback-array-glove-for-dexterous-manipulation.md): TAG hardware design, accuracy, stability, and cost
