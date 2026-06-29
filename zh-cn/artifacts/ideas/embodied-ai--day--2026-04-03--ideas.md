---
kind: ideas
granularity: day
period_start: '2026-04-03T00:00:00'
period_end: '2026-04-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied-control
- robotics
- world-models
- vision-language-action
- sim-to-real
tags:
- recoleta/ideas
- topic/embodied-control
- topic/robotics
- topic/world-models
- topic/vision-language-action
- topic/sim-to-real
language_code: zh-CN
---

# Robot control bottlenecks

## Summary
最清楚的实用变化出现在动作接口、规划栈和推理循环三个地方。一篇论文表明，当 VLA 策略把控制压缩成离散动作 token 时，更好的视觉编码器会停止带来收益，这说明在继续做编码器之前，先做一次简单的动作容量审计更合适。另一篇展示了在只有目标图像的长时程机器人任务上，层级潜在规划能带来真实收益，这给 world model 团队一个直接测试自动 subgoal 的办法。第三篇说明，重型 VLA 控制器可以用分块规划加在线验证来部署，在每一步之外加一个小型运行时检查，而不是每步都调用完整模型。

## Action-channel capacity audit for VLA policies with discrete action tokens
离散动作分词是在继续投入更好的机器人感知之前，应该先检查的一个具体环节。新的证据显示，一条常见的升级路径会在动作接口处卡住：在 LIBERO-10 上，Diffusion Policy 在 M 规模下把编码器从 ResNet-18 换成 SigLIP 后，成功率从 36.4% 提升到 57.6%；OAT 在同样升级下只从 53.8% 提升到 57.4%。编码器扫面更明显。Diffusion Policy 从 ResNet-18 的 36.4% 上升到 DINOv2 ViT-L/14 的 63.8%，而 OAT 只在较窄区间内波动，甚至在一些更强的编码器上下降。

对于训练带离散动作代码的 VLA 风格策略的团队，实用做法是在下一轮编码器刷新之前先做动作通道容量测试。保持数据集和策略规模不变，在一小组编码器质量上做替换，观察成功率是否随编码器提升而变化。然后增加 codebook 容量，或者在同一任务上对比连续动作基线。如果编码器变强后策略几乎不变，瓶颈多半在动作表示，而不是视觉部分。

这对机器人基础模型路线图是一个有用的落地调整，因为它把一个含糊的扩缩问题变成了一个低成本的门槛实验。判断很直接：只有当控制质量随着编码器质量一起上升时，才继续投入编码器；否则把精力转向 tokenizer、codebook 大小，或者连续动作头。

### Evidence
- [The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling](../Inbox/2026-04-03--the-compression-gap-why-discrete-tokenization-limits-vision-language-action-model-scaling.md): Shows that encoder upgrades give large gains for continuous actions but small or inconsistent gains for discrete action tokenization on LIBERO-10.
- [The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling](../Inbox/2026-04-03--the-compression-gap-why-discrete-tokenization-limits-vision-language-action-model-scaling.md): States the action tokenizer is the tightest bottleneck when actions are discretized, grounding the proposed audit around action-channel capacity.

## Hierarchical latent waypoint planning for goal-image robot control
对于只给目标图像、在长任务上失败的世界模型机器人，两层潜在规划器现在可以作为一个可用的控制插件。HWM 在真实 Franka 操作上给出了明显提升：它先在同一潜在空间里用高层 latent macro-action，再用低层 primitive action。取放任务上，平面规划的成功率是 0%，HWM 达到 70%。抽屉开关任务上，成功率从 30% 升到 70%。同一报告还说，规划成本在图注里下降了大约 3 倍，在贡献总结里最高降到 4 倍。

这里的做法很具体：在已有的学习型 world model 上加一个高层 latent waypoint planner，然后让低层控制器只负责到达下一个 latent subgoal。已经在 latent rollout 上用 MPC 的团队可以直接测试这一点，不需要改任务奖励，也不需要收集新的技能库，因为方法把两个规划器放在同一个潜在空间里，并且在执行时重新规划。

最先适合尝试的是已经有短时域 world model、但在多阶段操作上会崩掉的研究团队和应用机器人团队。一个低成本检查办法，是把当前的 goal-image 基准再跑一遍，分别使用 oracle subgoal 和自动 latent subgoal 做对比。论文在提供 oracle subgoal 时，平面规划和 HWM 都达到 80%，这说明 subgoal 生成才是主要缺口。

### Evidence
- [Hierarchical Planning with Latent World Models](../Inbox/2026-04-03--hierarchical-planning-with-latent-world-models.md): Provides the real-robot success gains, the hierarchical planning mechanism, and the claimed reduction in planning compute.
- [Hierarchical Planning with Latent World Models](../Inbox/2026-04-03--hierarchical-planning-with-latent-world-models.md): Describes the long-horizon failure mode of flat world-model planning and why hierarchical temporal abstraction addresses it.

## Verifier-gated action chunking for high-cost VLA inference
把轻量验证器接到分块式 VLA 控制上，适合在每步推理成本太高的系统里做部署测试。SV-VLA 把大型 VLA 保留为宏规划器，让它输出一个动作块，然后用小验证器在最新观测上检查每一步计划。验证器一旦和计划的差异超过阈值，系统就从当前状态重新规划。LIBERO 上，报告的三项子任务平均成功率从开放环分块基线的 79.5% 升到 90.90%。

这支持一种明确的工作流改动：对于已经在服务重型操作模型的团队，把控制拆成低频规划进程和高频验证进程，再把重新规划触发次数作为运维指标记录下来。这个方法兼容预训练 VLA，因为大模型保持冻结，只训练验证器。

直接测试也很清楚。拿现有的分块控制器，加一个小型图像编码器和动作距离门控，在同一任务上比较三种设置：开放环分块、验证器门控分块，以及在延迟允许时的逐步闭环。现有证据比规划和动作接口两篇论文更窄，因为摘要里没有每任务分数或延迟表，所以更适合作为已知 VLA 栈的部署实验，而不是对所有机器人控制都成立的广泛判断。

### Evidence
- [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](../Inbox/2026-04-03--open-loop-planning-closed-loop-verification-speculative-verification-for-vla.md): Summarizes the verifier design, the frozen heavy VLA setup, and the reported LIBERO gain from 79.5% to 90.90%.
- [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](../Inbox/2026-04-03--open-loop-planning-closed-loop-verification-speculative-verification-for-vla.md): Grounds the operational problem: stale observations during open-loop chunk execution cause drift and degraded control.
