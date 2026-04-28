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
这个时间窗口里的机器人工作指向三个明确的流程变化：用分阶段危险进展指标和拒绝闸门评估 VLA 安全性，在高接触任务的人形行为克隆中加入未来触觉 latent 预测，以及在视角变化和放置精度很关键的多视角操作策略里，把 3D 几何骨干当作默认候选。

## 用于 VLA 动作执行的分阶段语义安全检查
现在很容易测试一种适合 VLA 部署的实用安全闸门：对每个高风险任务记录 attempt、commit 和最终 success，再在动作执行前加一层小型拒绝层。HazardArena 提供了一个很干净的测试方式，因为安全版和危险版保留了相同的运动要求，只改变让动作变得允许或危险的语义条件。这一点对目前只看任务完成率、并把低危险 success 率当成策略安全证明的团队很重要。

论文说明了为什么这种流程会漏掉风险。在危险的 `insert outlet` 任务上，pi_0 在最终 success 只有 0.44 之前，attempt 已达到 0.93，commit 达到 0.80。机器人即使没有完成危险动作，也可能已经走到了大部分危险过程。同一个基准还表明，只用安全演示做微调，会同时提高安全任务 success 和危险任务 success。对于要交付家用或服务型操作系统的团队，近期值得做的是把语义级执行前检查和拒绝动作绑定起来，并在评估里加入分阶段日志。一个低成本验证方法是回放一小组安全/危险孪生任务，观察随着通用任务能力提升，哪些策略的危险 commit 率也在上升。

### Evidence
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): HazardArena 定义了安全/危险孪生任务、分阶段指标，以及安全任务提升与危险行为同时上升这一现象。
- [HazardArena: Evaluating Semantic Safety in Vision-Language-Action Models](../Inbox/2026-04-14--hazardarena-evaluating-semantic-safety-in-vision-language-action-models.md): 论文提出了无需训练的 Safety Option Layer，可在推理时作为护栏拦截不安全动作。

## 人形行为克隆中的未来触觉 latent 预测
做人形操作的团队可以在高接触任务上尝试一个明确的训练改动：在行为克隆时预测未来触觉 latent，并在运行时把触觉保留在策略输入中。HTD 在真实硬件上直接支持这种做法。收益主要出现在接触瞬间视觉状态不完整的任务里，包括插入、毛巾折叠、铲取和倒茶服务。

现有证据已经足够指导实现方案。HTD 接收多视角 RGB、本体感觉、手部关节力和触觉输入，再把未来触觉预测作为辅助目标加入训练。在五个真实世界任务上，它报告相对 ACT 的平均 success 提升 90.9%，并且在消融实验中，latent 触觉预测比原始触觉预测高出 30%。系统还能处理 3.5 mm 间隙的插入任务，并以 30 Hz 运行学习到的策略。对于已经在收集遥操作演示的实验室，缺的支持层往往是触觉日志和一个 latent 预测头，而不是更大的策略骨干。一个低成本检查方法是在一个插入任务或可变形物体任务上加入这个触觉辅助目标，然后比较接触失败模式，而不只看最终 success。

### Evidence
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): 摘要给出了任务集合、相对 ACT 的 90.9% 提升、latent 触觉预测的 30% 消融增益，以及部署细节。
- [Learning Versatile Humanoid Manipulation with Touch Dreaming](../Inbox/2026-04-14--learning-versatile-humanoid-manipulation-with-touch-dreaming.md): 摘要说明 HTD 在真实人形系统中将触觉与多视角视觉和本体感觉一起作为核心模态。

## 面向多视角操作策略的 3D 几何骨干
对于配备多视角相机的操作系统，近期一个很强的模型选择是同时学习控制和场景重建的 3D 几何骨干。VGA 用足够强的基准结果支持了这个判断，尤其适合那些仍在用视觉语言骨干或视频骨干处理精确放置和视角鲁棒性问题的团队。

设置很具体。VGA 使用一个预训练 3D 世界模型，输入多视角 RGB、语言和本体感觉，并训练共享骨干同时预测动作、相机参数和深度图。在 LIBERO 上，它的平均成绩是 98.1%，高于 pi_0.5 的 96.9%、OpenVLA-oft 的 97.1%、VLA-Thinker 的 97.5%、GeoAwareVLA 的 96.8% 和 GeoVLA 的 97.7%。摘录里的真实机器人结果还是定性描述，但指向了对未见相机视角更好的零样本迁移。对于正在选择骨干升级路线的团队，一个聚焦测试方法是固定下游训练流程，只替换表征栈，在那些相机位姿变化或物体朝向精度导致失败的任务上做对比。

### Evidence
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): 摘要提供了 VGA 的架构、联合训练设置、LIBERO 分数，以及与主要基线的比较。
- [Robotic Manipulation is Vision-to-Geometry Mapping ($f(v) \rightarrow G$): Vision-Geometry Backbones over Language and Video Models](../Inbox/2026-04-14--robotic-manipulation-is-vision-to-geometry-mapping-f-v-rightarrow-g-vision-geometry-backbones-over-language-and-video-models.md): 摘要摘录说明它在真实世界部署中对未见视角有更好的零样本泛化。
