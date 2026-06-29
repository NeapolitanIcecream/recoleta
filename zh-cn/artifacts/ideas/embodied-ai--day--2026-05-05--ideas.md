---
kind: ideas
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- VLA
- world models
- spatial reasoning
- benchmarks
- multimodal models
tags:
- recoleta/ideas
- topic/robotics
- topic/vla
- topic/world-models
- topic/spatial-reasoning
- topic/benchmarks
- topic/multimodal-models
language_code: zh-CN
---

# Robot Policy Evaluation Gates

## Summary
机器人团队可以把新的评测压力转成三项具体改动：为测试记忆和接触的 VLA 策略设置发布门槛、为机器人视频预测引入行为级奖励，以及为交互式世界模型比较建立共享的动作输入框架。

## Memory and contact tests for dexterous VLA release gates
将 VLA 策略部署到手部、机械臂或类人平台的机器人团队，应增加发布测试，分别覆盖三个失效模式：跟踪移动物体、记住先前交互、在遮挡下感知接触。一个小型基准可以包含输送带抓取、盒中选物任务，以及带触觉或关节力矩日志的插入或可变形物体抓取。通过标准应包括任务成功率、接触事件时序、依赖记忆的选择准确率，以及目标 GPU 上的每步延迟。

RLDX-1 给出了一套具体模板。该策略加入了多帧运动处理、一个保存过去认知特征块的记忆模块，以及放在单独物理流中的触觉或力矩输入。它在当前图像策略容易失败的任务上提升最大，包括 ALLEX Object-in-Box Selection 的 91.7% 成功率，以及输送带快速物体抓取的 87.5% 以上成功率。报告也把推理速度当作部署指标，将 RTX 5090 上的每步延迟从 71.2 ms 降到 43.7 ms。

### Evidence
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): Summarizes RLDX-1’s motion, memory, tactile/torque inputs, task results, and latency improvement.
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): Describes why dynamic manipulation, physical sensing, and memory create failures for existing VLAs.

## Behavior-scored reward models for robot video prediction
做规划的机器人视频世界模型团队，应在训练和评估流程里加入一个按行为打分的奖励模型。检查方法很直接：给生成的 rollout 在指令遵循、操作成功、动作-结果一致性、时间一致性、接触真实性和物理符合性上打分，再把这些分数与像素指标和下游规划质量对比。一个小型蒸馏奖励模型比 8B 判别器更适合反复训练。

RoboAlign-R1 展示了这套流程的样子。作者把 Qwen3-VL-8B-Thinking 微调成一个六维判别器，再蒸馏成一个 98M 奖励模型，并用于 GRPO 后训练。同一篇论文还加入了 Sliding Window Re-encoding，用于长 rollout：解码最后一帧，把它重新编码为新上下文，然后用更短的活动历史继续生成。报告结果是 RobotWorldBench 得分高于 iVideoGPT，六个行为维度都更好，长时程像素指标也提升了，额外延迟约 1%。

### Evidence
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): Summarizes the six-dimension judge, 98M reward model, GRPO post-training, Sliding Window Re-encoding, and reported metrics.
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): Explains why robot video world models need action-conditioned dynamics, contacts, scene evolution, and physical plausibility for control.

## Shared action-input harness for interactive world-model comparisons
对比文本控制、类似键盘控制和相机参数控制的世界模型团队，在跑排行榜前应先搭一个共享的动作输入测试框架。这个框架应把每个评测动作映射成文本命令、one-hot 控制和相机内外参，然后在动作响应、轨迹跟随、记忆和相机跟随上运行相同任务。这样可以减少歧义：一个模型接受“move forward”，另一个却需要低层控制 ID 或相机位姿。

iWorld-Bench 给出了这套框架的现成规范。它定义了 27 个平移和 27 个旋转动作 ID，把评测集中在 81 个常见组合动作上，并围绕动作控制难度、记忆和相机跟随构建了 4,900 个测试任务。论文还报告了覆盖面很广的设置，包括四种视角、九种户外天气、五种室内光照类型和 18 个模拟器环境，这有助于找出那些能通过狭窄场景测试、却会在视角或条件变化下失败的模型。

### Evidence
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): Summarizes iWorld-Bench’s action mapping, task types, dataset size, and coverage.
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): Describes the lack of aligned action definitions across text, keyboard, and trajectory or camera-control inputs.
