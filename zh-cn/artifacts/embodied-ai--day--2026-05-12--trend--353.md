---
kind: trend
trend_doc_id: 353
granularity: day
period_start: '2026-05-12T00:00:00'
period_end: '2026-05-13T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- manipulation
- safety evaluation
- autonomous driving
run_id: materialize-outputs
aliases:
- recoleta-trend-353
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/manipulation
- topic/safety-evaluation
- topic/autonomous-driving
language_code: zh-CN
---

# 机器人 VLA 工作正在部署压力下衡量预测、动作时机和安全性

## Overview
当天的机器人论文把 Vision-Language-Action (VLA) 模型视为控制系统，需要预测性 rollout、受引导的动作解码和显式安全检查。RAW-Dream 给出了最明确的数据效率结果。GuidedVLA 改进了动作聚焦。SafeManip 显示，任务成功可能掩盖不安全执行。

## Clusters

### 用于机器人 rollout 和训练的世界模型
世界模型工作是当天的主要技术重点。RAW-Dream 在任务无关的视频世界模型中用强化学习训练 VLA 策略，然后用 Qwen3-VL 作为零样本奖励评判器。在 LIBERO 上，它的零样本世界模型把平均成功率提高到 52.3%，而 1-shot 监督微调为 43.4%；该方法使用 10 个目标演示，并且在世界模型训练中不使用目标任务 rollout。

OrbiSim 走了另一条路线。它预测显式物理状态，并从这些状态渲染像素，因此学到的模拟器可以为策略和参数优化暴露梯度。在 robosuite Push 上，它报告的轨迹误差低于 Vid2World 和 AdaWorld，长时域视频指标也优于其未分离 dynamics-vision 的版本。

WAM 综述为这类工作给出了共同定义。它把 World Action Models (WAMs) 定义为同时预测未来观测和动作的模型，并区分级联式设计和联合式设计。CoME 为扩散世界模型加入记忆视角，使用短期、长期和空间专家，使生成的未来与先前观测保持一致。

#### Evidence
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream 报告了在任务无关世界模型中的想象强化学习，以及在低目标任务数据条件下的 LIBERO 成功率提升。
- [OrbiSim: World Models as Differentiable Physics Engines for Embodied Intelligence](../Inbox/2026-05-12--orbisim-world-models-as-differentiable-physics-engines-for-embodied-intelligence.md): OrbiSim 描述了显式状态神经模拟，并报告了长时域预测和轨迹指标。
- [World Action Models: The Next Frontier in Embodied AI](../Inbox/2026-05-12--world-action-models-the-next-frontier-in-embodied-ai.md): WAM 综述定义了联合观测-动作预测目标和分类法。
- [Composition of Memory Experts for Diffusion World Models](../Inbox/2026-05-12--composition-of-memory-experts-for-diffusion-world-models.md): CoME 报告了用于扩散世界模型的记忆专家，以及 Memory Maze 指标改进。

### 动作解码获得显式任务结构
GuidedVLA 关注动作解码器本身。它把注意力头分配给对象定位、技能阶段识别和基于深度的几何信息。该方法加入零初始化的残差注意力分支，使预训练策略在训练开始时保持稳定。

报告的收益覆盖多种扰动。在 LIBERO-Plus 上，完整模型达到 75.4% 的平均成功率，高于其 π0 基座的 68.2%。消融结果也支持这一设计选择：对象头、技能头和深度头都能提高成功率，全部头一起使用时效果最好。六项真实世界任务试验显示，在域内、场景和光照设置下，平均成功率更高。

#### Evidence
- [GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization](../Inbox/2026-05-12--guidedvla-specifying-task-relevant-factors-via-plug-and-play-action-attention-specialization.md): GuidedVLA 描述了专门化的动作解码器头，并报告了 LIBERO-Plus、扰动、RoboTwin 和真实世界结果。

### 延迟和流式控制进入 VLA 评估
Premover 把用户输入时间纳入控制循环。它让冻结的 VLA 策略在完整指令尚未结束前开始行动，并用焦点图和就绪门避免过早移动。在 LIBERO 上，它把平均实际耗时从 34.0s 降到 29.4s，同时成功率几乎不变，为 95.1%，完整提示基线为 95.0%。朴素提前执行会把成功率降到 66.4%，因此该门控是结果的关键。

MindVLA-U1 把同一部署问题带入自动驾驶。它用一个视觉-语言模型骨干处理语言 token、流式记忆，并通过 flow matching 生成连续航点。在 WOD-E2E 上，它报告在两个扩散步骤下达到 8.20 RFS，并在约 10 亿参数规模下达到约 16 FPS。

#### Evidence
- [Premover: Fast Vision-Language-Action Control by Acting Before Instructions Are Complete](../Inbox/2026-05-12--premover-fast-vision-language-action-control-by-acting-before-instructions-are-complete.md): Premover 报告了焦点图就绪门，以及 LIBERO 的实际耗时和成功率结果。
- [MindVLA-U1: VLA Beats VA with Unified Streaming Architecture for Autonomous Driving](../Inbox/2026-05-12--mindvla-u1-vla-beats-va-with-unified-streaming-architecture-for-autonomous-driving.md): MindVLA-U1 报告了一个流式 VLA 驾驶模型、WOD-E2E RFS 和延迟数据。

### 安全检查把任务完成与安全执行分开
SafeManip 为操作评估加入时间安全监控器。它把 rollout 映射为符号谓词轨迹，并在有限轨迹上检查线性时序逻辑，覆盖碰撞、抓取稳定性、释放稳定性、污染、容纳和访问规则。

这一结果给基准解读提出了明确警告。在 50 个 RoboCasa365 任务和六种 VLA 策略或变体上，π0.5 相比 π0 将任务成功率从 8.1% 提高到 9.3%，但其安全违规率也从 69.7% 上升到 82.8%。论文指出，碰撞/接触和释放稳定性是主要失败来源，因此最终任务完成率不能完整衡量家务操作。

#### Evidence
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip 定义了时间安全模板，并把违规率与任务成功率分开报告。
