---
kind: ideas
granularity: day
period_start: '2026-03-30T00:00:00'
period_end: '2026-03-31T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- benchmarking
- world-models
- teleoperation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/benchmarking
- topic/world-models
- topic/teleoperation
language_code: zh-CN
---

# 部署可靠性基准

## 摘要
机器人学习工作正在更接近部署里真正会出问题的地方：控制器时序、指令鲁棒性和物理评测。最近最明确的变化是一个测量停顿间隙的异步 VLA 运行时、一个给指令跟随策略用的改写测试门槛，以及一个固定机器人本体和任务条件的共享真实世界评测流程。

## 带停顿间隙监测的异步 VLA 执行
部署 VLA 策略到真实硬件的机器人团队，现在可以先做一次运行时改造，再去调整模型大小。StreamingVLA 表明，把观测、动作生成和执行并行起来，可以把 LIBERO 上的每步动作耗时从 74.5 ms 降到 33.7 ms，同时把平均成功率保持在 97.1%。它的自适应提前观测路径把停顿间隙从 232.3 ms 降到 36.0 ms，成功率为 94.9%，对那些主要受停走式运动影响、而不是策略本身太弱的机器人来说，这是一个可用的权衡。实现方式也很直接：把停顿间隙和每步动作耗时设为部署中的一级指标，再加一个异步推理执行器，让单步动作一生成就能执行，并且只在预测到低显著性时提前刷新观测。一个成本不高的检查方法是，把当前控制器回放到一个对接触敏感的任务上，看看失败是否主要来自动作块之间的暂停，而不是错误动作。如果是，流式执行器比重新训练更大的策略更直接。

### 资料来源
- [StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation](../Inbox/2026-03-30--streamingvla-streaming-vision-language-action-model-with-action-flow-matching-and-adaptive-early-observation.md): StreamingVLA reports 74.5 ms to 33.7 ms time-per-action improvement at the same 97.1% LIBERO success, and large halting-gap reductions with AFM and AEO.

## 机器人指令跟随的改写验收测试
机器人评测流程在宣称指令跟随稳定之前，需要先有一个改写测试集。LIBERO-Para 只改命令措辞，就在七种 VLA 配置上看到 22.8 到 51.9 个百分点的成功率下降。PRIDE 也比原始成功率低 8.4% 到 22.0%，说明二元完成分数漏掉了很多语言脆弱性。实际流程改动很简单：为每个线上任务保留一个固定的改写库，把它分成动作措辞变化和对象指代变化两部分，并同时报告任务成功率和一个对更难改写加权更高的鲁棒性分数。对象侧尤其需要关注，因为仅仅替换常见名称就会带来 19.8 到 51.0 个百分点的下降。对在少量内部演示上微调的团队来说，这可以在外场测试前当作验收门槛，尤其适合仓储和家用任务，因为这些场景里操作员很少会完全重复训练时的说法。

### 资料来源
- [LIBERO-Para: A Diagnostic Benchmark and Metrics for Paraphrase Robustness in VLA Models](../Inbox/2026-03-30--libero-para-a-diagnostic-benchmark-and-metrics-for-paraphrase-robustness-in-vla-models.md): LIBERO-Para isolates paraphrase robustness and reports 22.8 to 51.9 point success drops, with PRIDE below raw success and object-name changes causing especially large failures.

## 单一提交机器人策略端点的远程真实世界评测
共享的真实世界评测装置已经实用到可以当作通用操作模型的外部测试服务。ManipArena 固定了机器人本体，收集了 20 个物理任务和 10,812 条专家轨迹，并要求每个参与者为所有任务提交一个模型端点。它的试验结构把域内运行、分布内但有偏移的运行，以及语义 OOD 运行分开，同时使用受控光照和封闭测试间条件。这个设置适合那些已经在仿真里做基准测试的实验室和创业团队，在客户试点或论文宣称前，先做一次可比的物理测试。这里真正有用的不是另一个模拟器，而是一套远程评测流程：一个固定端点、匹配的任务资产，以及同时包含低层电机信号和相机流的标准日志。它的直接价值是能在模型和实验室之间给出可比的失败报告，尤其适合那些在 LIBERO 上表现不错、但还没经历真实延迟、接触噪声或更长移动操作回合的系统。

### 资料来源
- [ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation](../Inbox/2026-03-30--maniparena-comprehensive-real-world-evaluation-of-reasoning-oriented-generalist-robot-manipulation.md): ManipArena describes a standardized real-world benchmark with one shared embodiment, one submitted endpoint per participant, 20 tasks, stratified OOD trials, and rich sensor diagnostics.
