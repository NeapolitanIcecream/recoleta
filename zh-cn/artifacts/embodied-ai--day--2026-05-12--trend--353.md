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

# 机器人 VLA 工作正在衡量部署压力下的预测、动作时机和安全性

## 概览
今天的机器人论文把 Vision-Language-Action（VLA）模型当作控制系统来处理，需要预测性 rollout、带引导的动作解码和明确的安全检查。RAW-Dream 给出了最清楚的数据效率结果。GuidedVLA 改进了动作聚焦。SafeManip 说明任务成功率可能掩盖不安全执行。

## 研究发现

### 机器人 rollout 和训练中的世界模型
世界模型工作是今天的技术核心。RAW-Dream 在一个与任务无关的视频世界模型中用强化学习训练 VLA 策略，然后用 Qwen3-VL 作为零样本奖励判别器。在 LIBERO 上，它的零样本世界模型把平均成功率提高到 52.3%，对比 1-shot 监督微调的 43.4%，而且世界模型训练只用了 10 条目标演示，没有目标轨迹回放。

OrbiSim 走的是另一条路。它预测显式物理状态，再用这些状态渲染像素，因此学习到的模拟器可以为策略和参数优化提供梯度。在 robosuite Push 上，它的轨迹误差低于 Vid2World 和 AdaWorld，长时视频指标也优于去掉动力学和视觉分离的版本。

WAM 综述给这类工作定了共同定义。它把 World Action Models（WAMs）定义为同时预测未来观测和动作的模型，然后区分级联式设计和联合式设计。CoME 给扩散世界模型补上了记忆这一维，使用短期、长期和空间专家，让生成的未来与先前观测保持一致。

#### 资料来源
- [Reinforcing VLAs in Task-Agnostic World Models](../Inbox/2026-05-12--reinforcing-vlas-in-task-agnostic-world-models.md): RAW-Dream reports imagined RL inside a task-agnostic world model and LIBERO success gains with low target-task data.
- [OrbiSim: World Models as Differentiable Physics Engines for Embodied Intelligence](../Inbox/2026-05-12--orbisim-world-models-as-differentiable-physics-engines-for-embodied-intelligence.md): OrbiSim describes explicit-state neural simulation and reports long-horizon prediction and trajectory metrics.
- [World Action Models: The Next Frontier in Embodied AI](../Inbox/2026-05-12--world-action-models-the-next-frontier-in-embodied-ai.md): The WAM survey defines the joint observation-action prediction objective and taxonomy.
- [Composition of Memory Experts for Diffusion World Models](../Inbox/2026-05-12--composition-of-memory-experts-for-diffusion-world-models.md): CoME reports memory experts for diffusion world models and Memory Maze metric improvements.

### 动作解码开始带有明确的任务结构
GuidedVLA 把重点放在动作解码器本身。它把注意力头分别分配给物体定位、技能阶段识别和基于深度的几何信息。方法在开始时通过一个零初始化的残差注意力分支保持预训练策略稳定。

报告的提升在各种扰动下都很明显。在 LIBERO-Plus 上，完整模型的平均成功率达到 75.4%，而 π0 基线是 68.2%。消融结果也支持这个设计选择：物体、技能和深度头各自都能提高成功率，全部一起使用时最好。六个任务的真实世界试验显示，在同域、场景和光照条件下，平均成功率都更高。

#### 资料来源
- [GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization](../Inbox/2026-05-12--guidedvla-specifying-task-relevant-factors-via-plug-and-play-action-attention-specialization.md): GuidedVLA describes specialized action-decoder heads and reports LIBERO-Plus, perturbation, RoboTwin, and real-world results.

### 延迟和流式控制进入 VLA 评测
Premover 把用户输入时间也算进控制回路。它让冻结的 VLA 策略在整条指令还没输入完时就开始执行，用 focus map 和 readiness gate 避免过早动作。在 LIBERO 上，它把平均墙钟时间从 34.0s 降到 29.4s，同时成功率几乎不变，完整提示基线是 95.0%，它是 95.1%。直接提前执行会把成功率降到 66.4%，这说明 gate 是结果的关键。

MindVLA-U1 把同样的部署问题带到自动驾驶里。它用一个视觉-语言模型骨干处理语言 token、流式记忆和通过 flow matching 生成连续 waypoint。在 WOD-E2E 上，它报告 8.20 RFS、两步扩散，以及大约 16 FPS，参数规模约 1B。

#### 资料来源
- [Premover: Fast Vision-Language-Action Control by Acting Before Instructions Are Complete](../Inbox/2026-05-12--premover-fast-vision-language-action-control-by-acting-before-instructions-are-complete.md): Premover reports the focus-map readiness gate and LIBERO wall-clock and success results.
- [MindVLA-U1: VLA Beats VA with Unified Streaming Architecture for Autonomous Driving](../Inbox/2026-05-12--mindvla-u1-vla-beats-va-with-unified-streaming-architecture-for-autonomous-driving.md): MindVLA-U1 reports a streaming VLA driving model, WOD-E2E RFS, and latency figures.

### 安全检查把完成度和安全执行分开
SafeManip 给操作评测加上了时间安全监测。它把 rollout 映射成符号谓词轨迹，并在有限轨迹上检查线性时序逻辑，覆盖碰撞、抓取稳定性、释放稳定性、污染、包容关系和访问规则。

这对基准解释提出了明确警告。在 50 个 RoboCasa365 任务和 6 个 VLA 策略或变体上，π0.5 的任务成功率从 π0 的 8.1% 提高到 9.3%，但安全违规率也从 69.7% 升到 82.8%。论文把碰撞/接触和释放稳定性列为主要失败来源，所以最终任务完成度不能完整反映家庭操作的质量。

#### 资料来源
- [SafeManip: A Property-Driven Benchmark for Temporal Safety Evaluation in Robotic Manipulation](../Inbox/2026-05-12--safemanip-a-property-driven-benchmark-for-temporal-safety-evaluation-in-robotic-manipulation.md): SafeManip defines temporal safety templates and reports violation rates separately from task success.
