---
kind: trend
trend_doc_id: 386
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- vision-language-action
- robot manipulation
- reinforcement learning
- affordance learning
- 3D planning
- interpretability
- autonomous driving safety
run_id: materialize-outputs
aliases:
- recoleta-trend-386
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/reinforcement-learning
- topic/affordance-learning
- topic/3d-planning
- topic/interpretability
- topic/autonomous-driving-safety
language_code: zh-CN
---

# 机器人 VLA 论文要求接触感知控制和行为级验证

## 概览
这一时期的视觉-语言-动作（VLA）机器人工作都围绕执行展开。DyGRO-VLA 在强化学习中保护多任务策略。AffordVLA 在不加运行时模块的情况下学习接触区域。RoboFlow4D 为闭环控制加入快速 3D 运动计划。

## 研究发现

### Multi-task VLA control and contact grounding
DyGRO-VLA 将强化学习视为对基础机器人策略的受控编辑。它冻结基础 VLA，只训练路由的残差专家，加入 delta action chunks。在 LIBERO 上，它报告平均成功率 97.1%，比离线基础模型高 4.4 个百分点，在 LIBERO-Long 上高 9.8 个百分点。

AffordVLA 处理的是另一类失效：策略可能选对物体，却碰到错的部位。它在训练时把中间 VLA 视觉 token 与冻结的可供性教师对齐，推理时移除教师。论文报告，在 RoboTwin 上，Easy 比之前最好的基线高 20.5%，Hard 高 12.8%。

#### 资料来源
- [DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization](../Inbox/2026-05-17--dygro-vla-cross-task-scaling-of-vision-language-action-models-via-dynamic-grouped-residual-optimization.md): DyGRO-VLA method and reported LIBERO, LIBERO-Long, and RoboTwin2 results.
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA training setup, affordance teacher removal at inference, and RoboTwin gains.

### 3D planning signals for closed-loop manipulation
RoboFlow4D 把预测的 3D 夹爪流当作策略可跟踪的显式计划。它的慢快循环先规划低频轨迹，再让动作策略执行更高频的 chunks。论文报告，配合 Diffusion Policy 时，LIBERO 提升 6.2 个百分点；配合 DiT policy 时提升 4.0 个百分点，规划延迟不到一秒。

Visual Sculpting 在可变形操作里用了同样的思路。它在密集的 512×512 深度图和空间深度梯度上规划，然后在少量动作后用模型预测控制重新规划。系统生成了超过 100 个动作的长时程黏土序列，在报告的留出测试中，视觉损失改善了泡沫和面团的形变指标。

#### 资料来源
- [RoboFlow4D: A Lightweight Flow World Model Toward Real-Time Flow-Guided Robotic Manipulation](../Inbox/2026-05-17--roboflow4d-a-lightweight-flow-world-model-toward-real-time-flow-guided-robotic-manipulation.md): RoboFlow4D 3D flow planning method, slow-fast control, benchmark gains, and latency claim.
- [Visual Sculpting: Visually-Aligned Planning Representations for Long-Horizon Robot Clay Sculpting](../Inbox/2026-05-17--visual-sculpting-visually-aligned-planning-representations-for-long-horizon-robot-clay-sculpting.md): Visual Sculpting dense depth representation, MPC loop, deformation results, and long-horizon runs.

### Behavior-level checks for VLA interpretability and safety
Event-Grounded Sparse Autoencoders 把稀疏自编码器（SAE）改造成适配机器人策略的形式，通过把特征锚定到重复出现的 rollout 事件上。流程会提取末端执行器关键帧，按视觉和机器人状态线索聚类，再通过闭环干预测试特征。在 OpenVLA 第 31 层，把事件对齐特征置零后，成功率从 70.0% 降到 48.8%，比窗口均值、任务均值或 random-alive 排名的影响都更大。

这篇驾驶安全论文测试 Chain-of-Causation（CoC）解释是否与 Alpamayo-R1-10B 中的场景和轨迹一致。带障碍物上下文的推理里，整体 reasoning fidelity 为 42.5%。研究还报告了 94 次漏检行人、53.3% 的低 reasoning-action consistency，以及 37.9% 的“应该停车”案例实际上继续前进。

#### 资料来源
- [Event-Grounded Sparse Autoencoders for Vision-Language-Action Policies](../Inbox/2026-05-17--event-grounded-sparse-autoencoders-for-vision-language-action-policies.md): Event-grounded SAE pipeline and closed-loop intervention results.
- [Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation](../Inbox/2026-05-17--is-vla-reasoning-faithful-probing-safety-of-chain-of-causation.md): VLA driving reasoning-fidelity evaluation, pedestrian misses, and reasoning-action mismatch results.
