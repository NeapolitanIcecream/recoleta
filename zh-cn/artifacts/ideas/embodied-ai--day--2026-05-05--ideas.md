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

# 机器人策略评估门槛

## Summary
机器人团队可以把新的评估压力转化为三项具体改动：为 VLA 策略设置测试记忆和接触的发布门槛，为机器人视频预测加入行为级奖励，并为交互式世界模型比较建立共享动作输入工具链。

## 面向灵巧 VLA 发布门槛的记忆和接触测试
在手、机械臂或人形平台上部署 VLA 策略的机器人团队，应加入发布测试，单独检查三类失效模式：跟踪运动物体、记住早先交互、在遮挡下感知接触。一个小型基准可以包括传送带抓取、盒中物体选择任务，以及带触觉或关节扭矩日志的插入或可变形物体抓取。通过标准应包括任务成功率、接触事件时序、依赖记忆的选择准确率，以及目标 GPU 上的单步延迟。

RLDX-1 给出了一个具体模板。该策略加入多帧运动处理、存储过去认知特征块的记忆模块，并在独立的物理流中加入触觉或扭矩输入。报告中的最大增益出现在当前图像策略容易失败的任务上，包括 ALLEX Object-in-Box Selection 的 91.7% 成功率，以及传送带快速物体抓取超过 87.5% 的成功率。报告还把推理速度作为部署指标，将 RTX 5090 上的单步延迟从 71.2 ms 降到 43.7 ms。

### Evidence
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): 总结了 RLDX-1 的运动、记忆、触觉/扭矩输入、任务结果和延迟改进。
- [RLDX-1 Technical Report](../Inbox/2026-05-05--rldx-1-technical-report.md): 说明了动态操作、物理感知和记忆为何会让现有 VLA 失败。

## 用于机器人视频预测的行为评分奖励模型
使用机器人视频世界模型做规划的团队，应在训练和评估循环中加入按行为评分的奖励模型。有效检查很直接：对生成的 rollout 按指令遵循、操作成功、动作-结果一致性、时间一致性、接触真实感和物理遵循度评分，再把这些分数与像素指标和下游规划质量对比。小型蒸馏奖励模型比 8B judge 更适合反复训练运行。

RoboAlign-R1 展示了这种工作流。作者将 Qwen3-VL-8B-Thinking 微调成六维 judge，蒸馏为 98M 奖励模型，并将其用于 GRPO 后训练。同一篇论文还为长 rollout 加入 Sliding Window Re-encoding：解码最后一个预测帧，把它重新编码为新的上下文，然后用更短的活跃历史继续生成。报告结果显示，它的 RobotWorldBench 分数高于 iVideoGPT，六个行为维度的分数都更好，长时域像素指标也有改进，额外延迟约为 1%。

### Evidence
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): 总结了六维 judge、98M 奖励模型、GRPO 后训练、Sliding Window Re-encoding 和报告的指标。
- [RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models](../Inbox/2026-05-05--roboalign-r1-distilled-multimodal-reward-alignment-for-robot-video-world-models.md): 解释了机器人视频世界模型为何需要面向控制的动作条件动态、接触、场景演化和物理合理性。

## 用于交互式世界模型比较的共享动作输入工具链
比较文本控制、类键盘控制和相机参数模型的世界模型团队，应先构建共享的动作输入工具链，再运行排行榜。该工具链应把每个评估动作映射为文本命令、one-hot 控制，以及相机内参或外参，然后在动作响应、轨迹跟随、记忆和相机跟随上运行同一组任务。这样可以减少歧义，例如一个模型接受“move forward”，另一个模型需要低层控制 ID 或相机位姿。

iWorld-Bench 为这个工具链提供了现成规范。它定义了 27 个平移动作 ID 和 27 个旋转动作 ID，把评估集中在 81 个常见组合动作上，并构建了 4,900 个测试任务，覆盖动作控制难度、记忆和相机跟随。论文还报告了覆盖范围：四种视角、九种户外天气、五种室内照明类型和 18 个仿真器环境。这有助于找出在狭窄场景测试中通过、但在视角或条件变化后失败的模型。

### Evidence
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): 总结了 iWorld-Bench 的动作映射、任务类型、数据集规模和覆盖范围。
- [iWorld-Bench: A Benchmark for Interactive World Models with a Unified Action Generation Framework](../Inbox/2026-05-05--iworld-bench-a-benchmark-for-interactive-world-models-with-a-unified-action-generation-framework.md): 描述了文本、键盘、轨迹或相机控制输入之间缺少对齐动作定义的问题。
