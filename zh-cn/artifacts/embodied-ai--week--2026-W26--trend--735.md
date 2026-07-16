---
kind: trend
trend_doc_id: 735
granularity: week
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-29T00:00:00'
topics:
- robotics
- vision-language-action
- robot manipulation
- deployment adaptation
- robot safety
- world models
run_id: materialize-outputs
aliases:
- recoleta-trend-735
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/robot-manipulation
- topic/deployment-adaptation
- topic/robot-safety
- topic/world-models
language_code: zh-CN
---

# 机器人 VLA 可靠性正在用 rollout、标定和安全成本来衡量

## 概览
本周机器人视觉-语言-动作（VLA）研究聚焦于可在执行期间检查的策略。FORCE、ICWM 和 LIBERO-Safety 提供了主要信号：机器人论文正在把进展绑定到在线 rollout、配置标定和不安全成功指标上。

## 研究发现

### 部署适应
多篇论文把已部署机器人视为需要在任务前或任务中获取本地证据的系统。ICWM 让策略先运行一段短暂探测阶段，再把观测到的动作到图像变化作为上下文，用于在新相机视角或新机体配置下控制机器人。FORCE 用在线 rollout 通过校准过的 critic 微调 VLA 策略，并报告真实 Franka 的成功率从行为克隆下的 45.0% 提高到微调后的 98.3%，在线阶段没有人工干预。PhysReflect-VLA 加入执行时可行性检查，并在观测到状态不匹配后进行修正，在长时程任务上带来幅度较小但稳定的真实机器人收益。

#### 资料来源
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): ICWM 摘要说明了主动探测、上下文片段、LIBERO 收益，以及未见视角下的真实机器人测试。
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): FORCE 摘要给出了在线微调方法，以及仿真和真实世界成功率提升。
- [PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies](../Inbox/2026-06-25--physreflect-vla-physical-feasibility-and-self-reflective-regulation-for-reliable-vision-language-action-policies.md): PhysReflect-VLA 摘要描述了真实机器人操作任务中的运行时可行性评分和纠正式反思。

### 几何与动作结果
几何正在作为执行信号加入，而不只是视觉特征。Reflective VLA 存储观察-动作-结果三元组，让策略在推理时推断相机标定、执行偏差和机器人配置影响。G3VLA 通过射线嵌入、投影位置编码和跨视角融合，把相机内参和外参注入视觉 token，同时保留基础动作路径。两条路线指向同一个实际需求：机器人策略需要知道，在当前相机和机体条件下，自己的动作会如何改变场景。

#### 资料来源
- [Reflective VLA: In-Context Action Consequences Make VLAs Generalize](../Inbox/2026-06-23--reflective-vla-in-context-action-consequences-make-vlas-generalize.md): Reflective VLA 摘要解释了观察-动作-结果三元组，并报告了 LIBERO 分布偏移下的收益。
- [G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models](../Inbox/2026-06-23--g-3-vla-geometric-inductive-bias-for-vision-language-action-models.md): G3VLA 摘要详述了相机感知视觉 token，以及在 LIBERO、RoboCasa24、RoboTwin2.0 和真实世界倒液任务上的收益。

### 作为轨迹指标的安全
安全研究正在加入更多诊断指标。LIBERO-Safety 在 75 个任务和 19,664 条经过筛选的无碰撞演示上，测试 VLA 策略能否在没有不安全接触或不安全指令服从的情况下完成操作。ForesightSafety-VLA 将每次 rollout 评为安全成功、不安全成功、安全失败或不安全失败，再加入累计安全成本和风险暴露时间等过程指标。关键证据是，任务成功可能掩盖有风险的运动：ForesightSafety-VLA 报告最强的列出基线也存在不安全成功，而 LIBERO-Safety 显示更难的物理安全等级上成功率大幅下降。

#### 资料来源
- [LIBERO-Safety: A Comprehensive Benchmark for Physical and Semantic Safety in Vision-Language-Action Models](../Inbox/2026-06-22--libero-safety-a-comprehensive-benchmark-for-physical-and-semantic-safety-in-vision-language-action-models.md): LIBERO-Safety 摘要提供了任务数量、数据集规模、安全套件和基线失败细节。
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA 摘要给出了 rollout 结果类别、过程指标和基线不安全成功率。

### 动作数据和新技能
本周也有更多工作在降低动作监督成本，并提高其复用性。InSight 将现有演示切分为具名原语，让视觉语言模型选择缺失的原语尝试，并把成功的机器人 rollout 回灌到 VLA。它报告称，在为每项技能加入 20 个成功获取的原语 episode 后，真实 xArm 任务上的扭转成功率为 92%，倒液成功率为 96%。LA4VLA 采用数据优先路线：它从 DROID 中导出 33,116 个语言-动作 episode，并在没有图像的情况下用指令条件运动预训练策略，提升了一个 1B 参数 VLA 在仿真和真实世界任务上的表现。

#### 资料来源
- [InSight: Self-Guided Skill Acquisition via Steerable VLAs](../Inbox/2026-06-23--insight-self-guided-skill-acquisition-via-steerable-vlas.md): InSight 摘要给出了原语切分循环、目标技能获取过程和真实机器人结果。
- [LA4VLA: Learning to Act without Seeing via Language-Action Pretraining](../Inbox/2026-06-25--la4vla-learning-to-act-without-seeing-via-language-action-pretraining.md): LA4VLA 摘要描述了 33,116 个语言-动作 episode，以及混合语言-动作和 VLA 预训练带来的收益。
