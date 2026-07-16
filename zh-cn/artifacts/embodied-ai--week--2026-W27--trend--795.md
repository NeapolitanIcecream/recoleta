---
kind: trend
trend_doc_id: 795
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- robot manipulation
- deployment systems
run_id: materialize-outputs
aliases:
- recoleta-trend-795
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/robot-manipulation
- topic/deployment-systems
language_code: zh-CN
---

# 机器人 VLA 进展按控制环成功来衡量

## 概览
本周机器人研究把视觉-语言-动作（VLA）策略放进真实执行约束中。最有力的证据来自能够预测动作相关变化、管理长 rollout，并让服务延迟与任务进度保持关联的模型。Bridge-WA、FurnitureVLA 和 ROSA 显示了最清楚的压力点。

## 研究发现

### 跨具身形态 VLA 训练
通用机器人策略正在训练成共享高层操作概念，同时仍能生成特定机器人的控制。ZR-0 是最清楚的例子。它在训练中使用密集具身思维链标签，覆盖场景描述、任务进度、未来计划、目标框和离散动作 token。推理时，它跳过文本生成，并通过扩散动作专家输出连续动作块。

可量化的结果很具体。ZR-0 报告在 LIBERO 上的平均成功率为 97.8%；ProcCorpus-60M 覆盖约 6000 万帧、1000 小时和超过 40 万条轨迹。同一天的趋势还把它与无奖励的测试时改进和轨迹记忆归在一起，说明策略规模正在与可执行的动作时序和状态历史绑定。

#### 资料来源
- [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](../Inbox/2026-06-29--training-vision-language-action-models-with-dense-embodied-chain-of-thought-supervision.md): ZR-0 的训练设计、数据集规模、推理路径和 LIBERO 结果。

### 用于操作的 3D 和未来变化信号
多篇论文在生成动作前加入显式物理信号。3D HAMSTER 在度量 3D 空间中预测末端执行器路径点，并将这些路径点输入点云控制策略。在 DroidSpatial-Bench 上，它在 10 cm 阈值下达到 65.5% 的 Both 准确率，高于 RoboBrain-2.5-8B 的 60.1%，也远高于通用 VLM 基线。

Bridge-WA 使用另一种控制信号。它把未来变化教师模型蒸馏为预期结果 token、变化图和运动流图，部署时移除教师模型。它报告在 VLABench 上的平均成功率为 52.8%；在干扰物、光照变化和桌布变化下，真实机器人 Dobot hard-track 平均表现强于 X-VLA。

DVG-WM 增加了视频预测证据。它把低分辨率动力学与高分辨率细化分开，并报告在 LIBERO 视频预测上的推理时间为 88.7 秒；相比之下，CogVideoX-5B 为 236.8 秒，LVP-14B 为 354.2 秒。共同模式很直接：有用的机器人预测要按接触、变化区域和规划成本来评判。

#### 资料来源
- [3D HAMSTER: Bridging Planning and Control in Hierarchical Vision Language Action Models through 3D Trajectory Guidance](../Inbox/2026-06-30--3d-hamster-bridging-planning-and-control-in-hierarchical-vision-language-action-models-through-3d-trajectory-guidance.md): 3D HAMSTER 的路径点设计和 DroidSpatial-Bench 结果。
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): Bridge-WA 的未来变化先验和基准结果。
- [DVG-WM: Disentangled Video Generation Enables Efficient Embodied World Model for Robotic Manipulation](../Inbox/2026-06-30--dvg-wm-disentangled-video-generation-enables-efficient-embodied-world-model-for-robotic-manipulation.md): DVG-WM 的视频世界模型设计、质量指标和推理时间对比。

### 长时程操作需要进度检查
长任务暴露了短程操作基准漏掉的失败模式。FurnitureVLA 面向真实尺度的双臂家具组装，包含 4 到 7 个子任务，最多 1550 个控制步。它的策略同时预测 14 维双臂动作和连续进度值，并用进度信号触发子任务切换。

收益按完整组装来衡量。在三个 IKEA 风格任务上，平均仿真成功率从单体微调 VLA 的 0.48 提升到 0.80。同一结果也显示了较弱执行设计的代价：移除后置相机设置会使平均成功率降到 0.50，离散进度预测在三个仿真家具任务上全部失败。

#### 资料来源
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): FurnitureVLA 的任务时长、进度预测方法和成功率结果。

### 工厂部署按调度问题处理
机器人基础模型也开始按已部署服务来评估。ROSA 将多台机器人的模型请求路由到共享 GPU 池，并按服务级目标合格动作吞吐量进行调度。任务文件覆盖模型组件、提示词、调用频率、重试规则，以及停止、重发、重新规划或呼叫人类等回退动作。

报告的收益来自把机器人推理当作机群工作负载处理。在 8 块 NVIDIA H200 GPU 和最多 64 台虚拟机器人条件下，相比专用服务基线，ROSA 将符合 SLO 的工厂生产率最高提高 12.06 倍。相比没有其调度器的共享服务器基线，它将合格工厂动作吞吐量最高提高 2.44 倍。这让部署证据与策略成功率一起成为研究信号的一部分。

#### 资料来源
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): ROSA 的架构、调度目标和吞吐量结果。
