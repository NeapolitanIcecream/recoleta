---
kind: ideas
granularity: day
period_start: '2026-06-23T00:00:00'
period_end: '2026-06-24T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- manipulation
- navigation
- synthetic data
- evaluation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/manipulation
- topic/navigation
- topic/synthetic-data
- topic/evaluation
language_code: zh-CN
---

# VLA 策略支持层

## Summary
机器人 VLA 团队现在可以围绕现有策略测试三类实用支持层：用于缺失操控技能的 primitive 采集循环、用于在有限真实演示下进行多相机微调的几何路径，以及用于长时程任务调试和数据过滤的步骤级评分。

## 用于缺失操控技能的部署后 primitive 采集循环
在固定工作单元中运行 VLA 的操控团队，可以为策略缺失的技能加入一个小型采集循环。流程很具体：把现有遥操作数据集切分成带名称的 primitives，让 VLM 为失败的新任务制定计划，找出缺失的 primitive 标签，用受限的低层控制器为这些 primitives 采集机器人 rollouts，用 VLM oracle 接受成功片段，然后重新训练策略，使新的 primitive 后续可以被调用。

InSight 给出了一个可执行的形态。在真实 xArm 扭转和倒水任务中，它从 50 条 pick-and-place 演示开始，加入 20 个成功采集到的 primitive episode，并报告了 92% 的扭转成功率和 96% 的倒水成功率。它还在没有端到端演示的情况下，为一个先扭转再倒水的任务串联了 14 个 primitives，并达到 80% 成功率。论文报告的采集成本低到可以做实验室试验：采集 20 个扭转 primitives 需要 23 次试验和 39.7 分钟；采集 20 个倒水 primitives 需要 31 次试验和 85.3 分钟。

同一个部署流程应在 rollouts 期间保存策略自身的 observation-action-consequence 三元组。Reflective VLA 说明了这类日志的作用：三元组通过已执行动作的可见结果暴露相机几何、校准误差和执行偏差。在 LIBERO-Plus 上，Reflective VLA 报告的平均成功率为 87.7%，匹配的反应式基线为 82.3%；列出的最大增益来自 Robot 偏移，72.9% 对 50.0%。一个低成本检查是：在一个缺失 primitive 和一个相机或机器人偏移上运行该循环，然后测量重新训练后的策略是否在提升新 primitive 的同时保留旧的 pick-and-place 技能。

### Evidence
- [InSight: Self-Guided Skill Acquisition via Steerable VLAs](../Inbox/2026-06-23--insight-self-guided-skill-acquisition-via-steerable-vlas.md): InSight 描述了 primitive 分割、由 VLM 引导的缺失 primitive 采集、真实 xArm 扭转和倒水结果、长时程组合以及采集时间。
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA 描述了 observation-action-consequence 三元组，并报告了在机器人、相机和校准偏移下的增益。

## 用于 VLA 微调的校准感知视觉 tokens 和 2D waypoint 监督
拥有已校准多相机操控设备的团队，可以在采集大得多的动作数据集之前先测试一个几何插件。构建方式很明确：把相机感知的视觉 token 模块接到 VLA 上，加入来自内参的射线嵌入，加入来自内参和外参的投影位置编码，在动作路径之前融合多视角，并用点图或教师监督训练新增的几何路径。对于合成机器人视频，把生成数据送入 2D 末端执行器 waypoint 头，并只用真实演示训练动作头。

G3VLA 支持这个流程中的相机校准部分。它保留预训练 VLA backbone、动作空间和模仿学习目标，同时加入射线嵌入、PRoPE 和跨视角融合。在使用 pi0 的 LIBERO 上，ground-truth 几何监督把平均成功率从 84.6% 提高到 88.1%，Object 和 Spatial 套件上的增益更大。报告中的真实世界倒水结果也把 OOD 成功率从 70.8-75.0% 提高到 83.3-87.5%。

GRA 支持合成视频部分。它用生成视频监督未来 2D 末端执行器 waypoint，并且只在真实机器人演示上训练动作。在三个真实 Franka pick-and-place 任务上，每个任务使用 25 条真实演示加 75 个生成视频，平均成功率达到 68.9%；真实数据等预算基线为 61.1%，pseudo-action 基线更低。一个实用的首轮测试是在一个任务上做三组消融：仅真实数据、真实数据加 pseudo-actions、真实数据加生成视频 waypoint 监督。

### Evidence
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA 记录了校准感知视觉 tokens、射线嵌入、PRoPE、跨视角融合，以及基准和真实世界倒水结果。
- [Supervise What Survives: Geometry-Guided VLA Adaptation from Synthetic Robot Videos](../Inbox/2026-06-23--supervise-what-survives-geometry-guided-vla-adaptation-from-synthetic-robot-videos.md): GRA 记录了生成视频 2D waypoint 监督、仅真实数据动作训练、Franka 任务结果，以及 pseudo-action 对比。

## 用于机器人运行复盘的步骤级任务 oracles 和视频进度分数
长时程 VLA 评测需要一个运行复盘工具，指出哪一步失败，以及轨迹中是否包含犹豫或重试行为。仿真器侧版本可以从自然语言任务指令开始，生成 `Open(fridge)`、`Pick(bottle)`、`Place(bottle, fridge)` 和 `Close(fridge)` 等原子检查，并把这些检查附加到有序或部分有序的任务序列上。数据复盘版本可以为录制视频打任务进度分，并用该分数过滤或加权质量混杂的演示。

MANGO 提供步骤定位部分。它构建可复用的原子任务库，把每个原子任务映射到仿真器函数，例如打开状态、持有状态、接触和空间关系，并使用 Generator、Assessor 和 Judge agents 来改进可执行 oracles。可用摘录报告了在 LIBERO_10 和 RoboCasa Humanoid Tabletop 上的评测；生成的 oracles 检测到的失败数量与人工编写的符号 oracles 接近，同时能识别失败的原子步骤和顺序违规。

World Value Models 提供面向缺陷数据的进度评分部分。WVM 使用预训练视频世界模型从视频和语言估计任务进度，并引入 Suboptimal-Value-Bench，其中包含跨 3 种 embodiments 和 15 个任务的 800 条人工标注轨迹。它报告的平均 Hesitation-RMSE 为 0.05，平均 Retry-VOC 为 0.78，领先列出的价值模型基线；还报告了在仿真和真实任务中，WVM 引导的 AWR 和 filtered BC 带来更好的下游策略学习。第一个有用的部署检查是为一个基准套件做回放仪表盘，显示失败的原子步骤、进度曲线，以及标记为犹豫或重试的片段。

### Evidence
- [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](../Inbox/2026-06-23--mango-automated-multi-agent-test-oracle-generation-for-vision-language-action-models.md): MANGO 记录了细粒度 oracles 的自动生成、原子任务库、仿真器检查，以及在 LIBERO_10 和 RoboCasa Humanoid Tabletop 上的失败定位。
- [World Value Models for Robotic Manipulation](../Inbox/2026-06-23--world-value-models-for-robotic-manipulation.md): WVM 记录了基于视频的任务进度评分、Suboptimal-Value-Bench、犹豫和重试指标，以及下游策略学习用途。
