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

## Summary
机器人学习的工作正在更直接地处理部署最容易出问题的几个环节：控制器时序、指令鲁棒性和真实物理评测。近期最清晰的变化包括：能够测量停顿间隙的异步 VLA 运行时、面向指令跟随策略的释义测试门槛，以及在本体和任务条件上保持一致的共享真实世界评测流程。

## 通过停顿间隙监控实现异步 VLA 执行
在真实硬件上部署 VLA 策略的机器人团队，现在有充分理由先做一次运行时改造，调整执行调度，再考虑模型规模。StreamingVLA 表明，在 LIBERO 上将观测、动作生成和执行重叠后，单步动作耗时可从 74.5 ms 降到 33.7 ms，同时平均成功率保持在 97.1%。其自适应提前观测路径把停顿间隙从 232.3 ms 降到 36.0 ms，成功率为 94.9%；对于主要因走走停停而失败、而不是因策略本身太弱而失败的机器人，这个取舍可以接受。落地方式也很明确：把停顿间隙和单步动作耗时列为一等部署指标，然后加入异步推理执行器，在生成出单步动作后立刻执行，并且只在预测显著性较低时提前刷新观测。一个低成本检查方法是：在一个对接触敏感的任务上回放你当前的控制器，测量失败的主要原因是否是动作簇之间的停顿，而不是动作本身错误。如果是，流式执行器比重新训练一个更大的策略更直接。

### Evidence
- [StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation](../Inbox/2026-03-30--streamingvla-streaming-vision-language-action-model-with-action-flow-matching-and-adaptive-early-observation.md): StreamingVLA 报告称，在 LIBERO 成功率同为 97.1% 的情况下，单步动作耗时从 74.5 ms 降到 33.7 ms，并且通过 AFM 和 AEO 显著缩短了停顿间隙。

## 面向机器人指令跟随的释义验收测试
机器人评测流程在宣称指令跟随稳定之前，需要先加入一个释义测试集。LIBERO-Para 只改写命令措辞，就在七种 VLA 配置上测到了 22.8 到 51.9 个百分点的成功率下降。PRIDE 也比原始成功率低 8.4% 到 22.0%，说明二元完成分数漏掉了很大一部分语言脆弱性。实际流程改动很简单：为每个生产任务保留一套固定的释义库，按动作措辞变化和对象指代变化拆分，并同时报告任务成功率与一个对更难改写赋予更高权重的鲁棒性分数。对象侧尤其需要重点检查，因为仅常见名称替换这一项，就会带来 19.8 到 51.0 个百分点的下降。对少量内部演示数据做微调的团队，可以把它当作外场测试前的验收门槛，尤其适用于仓储和家庭场景，因为操作人员很少会严格重复训练时的表述。

### Evidence
- [LIBERO-Para: A Diagnostic Benchmark and Metrics for Paraphrase Robustness in VLA Models](../Inbox/2026-03-30--libero-para-a-diagnostic-benchmark-and-metrics-for-paraphrase-robustness-in-vla-models.md): LIBERO-Para 单独测量释义鲁棒性，报告了 22.8 到 51.9 个百分点的成功率下降；PRIDE 低于原始成功率，而且对象名称变化会造成特别大的失败。

## 通过单一提交的机器人策略端点进行远程真实世界评测
共享的真实世界评测平台已经开始具备作为通用操作模型外部测试服务的实用性。ManipArena 固定了机器人本体，收集了 20 个物理任务和 10,812 条专家轨迹，并要求每个参与方为所有任务提交同一个模型端点。它的试验结构把同分布域内测试、分布内偏移测试和语义 OOD 测试分开，并在受控光照和封闭测试间条件下执行。对于已经在仿真中做基准测试、但在客户试点或论文结论前还需要一次可比较的真实物理测试的实验室和创业团队，这提供了一条明确的采用路径。这里真正值得建设的不是另一个模拟器，而是一套远程评测流程：一个冻结端点、配套的任务资产，以及包含低层电机信号和相机视频流的标准日志。它的直接价值是让不同模型和实验室的失败报告可以横向比较，尤其适用于那些在 LIBERO 上表现不错、但还没有经过真实延迟、接触噪声或更长移动操作任务检验的系统。

### Evidence
- [ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation](../Inbox/2026-03-30--maniparena-comprehensive-real-world-evaluation-of-reasoning-oriented-generalist-robot-manipulation.md): ManipArena 描述了一个标准化的真实世界基准：共享单一本体、每个参与方只提交一个端点、包含 20 个任务、分层的 OOD 试验，以及丰富的传感器诊断数据。
