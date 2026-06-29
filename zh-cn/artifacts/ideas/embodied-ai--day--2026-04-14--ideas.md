---
kind: ideas
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vla-safety
- humanoid-manipulation
- tactile-sensing
- 3d-geometry
tags:
- recoleta/ideas
- topic/robotics
- topic/vla-safety
- topic/humanoid-manipulation
- topic/tactile-sensing
- topic/3d-geometry
language_code: zh-CN
---

# 具身操作控制

## Summary
这段时间的机器人工作指向三个具体的流程变化：用分阶段的危险进程和拒绝门来评估 VLA 安全，在接触密集任务的人形机器人行为克隆中加入未来触觉潜变量预测，并在多视角操作策略里把 3D 几何骨干当作默认候选，尤其是在视角变化和放置精度很重要的时候。

## Stage-wise semantic safety checks for VLA action execution
现在可以直接测试一个实用的 VLA 部署安全门：用 attempt、commit 和最终 success 给每个高风险任务打分，然后在动作执行前加一层小型拒绝层。HazardArena 提供了一个清晰的测试方式，因为安全版和危险版保留相同的运动要求，只改变让动作被允许或变危险的语义条件。这对现在还依赖任务完成率、并以为较低的危险成功率就说明策略安全的团队很重要。

论文说明了为什么这种流程会漏掉风险。在危险的 `insert outlet` 任务上，pi_0 在最终成功 0.44 之前，attempt 已到 0.93，commit 已到 0.80。机器人即使没有完成危险动作，也可能已经进入大半。这个基准还显示，只用安全演示做微调，安全成功和危险成功会一起上升。对做家用或服务机器人操作的团队来说，近期该做的是把语义前置检查和拒绝动作连起来，并在评估里记录分阶段指标。一个成本较低的验证方法，是回放少量安全和危险的成对任务，看看当总体技能提升时，危险 commit 率是否也上升。

### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): HazardArena defines safe/unsafe twin tasks, stage-wise metrics, and the reported coupling between safe-task gains and unsafe behavior.
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): The paper introduces the training-free Safety Option Layer as an inference-time guard for blocking unsafe actions.

## Future tactile latent prediction in humanoid behavior cloning
做人形机器人操作的团队可以试一个明确的训练改动，特别是在接触密集的任务上：在行为克隆时预测未来的触觉潜变量，并在运行时把触觉保留在策略输入里。HTD 给出了一个直接的真实硬件案例。它的收益出现在接触瞬间视觉状态不完整的任务上，包括插入、叠毛巾、舀取和端茶。

证据已经足够具体，可以用来安排实现。HTD 同时接收多视角 RGB、本体感觉、手关节力和触觉输入，并把未来触觉预测作为辅助目标。它在五个真实世界任务上报告了相对 ACT 平均成功率提升 90.9%，而且在消融中，潜变量触觉预测比原始触觉预测高 30%。系统还能处理 3.5 mm 的插入力间隙，已学习策略以 30 Hz 运行。对已经在采集遥操作演示的实验室来说，缺的通常是触觉日志和潜变量预测头，而不是更大的策略骨干。一个成本较低的检查方法，是在一个插入或可变形物体任务上加入这个辅助触觉目标，然后比较接触失败模式，而不只是终点成功率。

### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): The summary gives the task set, the 90.9% relative gain over ACT, the 30% ablation gain for latent tactile prediction, and deployment details.
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): The abstract states that HTD models touch as a core modality alongside multi-view vision and proprioception in a real humanoid system.

## 3D geometry backbones for multi-view manipulation policies
对于带多视角相机的操作系统，短期内很强的模型选择是一个同时学习控制和场景重建的 3D 几何骨干。VGA 用足够高的基准结果支持了这个判断，尤其适合那些仍在用视觉-语言或视频骨干处理精确放置和视角鲁棒性的团队。

设置很直接。VGA 使用预训练 3D 世界模型，输入多视角 RGB、语言和本体感觉，并训练共享骨干同时预测动作、相机参数和深度图。在 LIBERO 上，它的平均成绩是 98.1%，高于 pi_0.5 的 96.9%、OpenVLA-oft 的 97.1%、VLA-Thinker 的 97.5%、GeoAwareVLA 的 96.8% 和 GeoVLA 的 97.7%。摘要里给出的真实机器人结果是定性的，但指向对未见相机视角更好的零样本迁移。对在骨干升级之间做选择的团队来说，一个聚焦测试是冻结下游训练配方，只替换表示栈，专门在相机位姿变化或物体朝向精度决定失败的任务上比较效果。

### Evidence
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): The summary provides VGA's architecture, joint training setup, LIBERO scores, and comparisons with major baselines.
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): The abstract excerpt states better zero-shot generalization to unseen viewpoints in real-world deployments.
