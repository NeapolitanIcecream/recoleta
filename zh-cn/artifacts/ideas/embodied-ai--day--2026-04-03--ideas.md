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

# 机器人控制瓶颈

## Summary
最清晰的实际变化点在动作接口、规划栈和推理回路。第一篇论文表明，当 VLA 策略把控制压缩为离散动作 token 时，更好的视觉编码器可能不再带来帮助，这说明在继续投入编码器之前，应该先做一个简单的动作容量审计。第二篇论文展示了分层潜在规划在仅提供目标图像的长时域机器人任务上带来的真实增益，这给世界模型团队提供了一个直接测试自动子目标的方法。第三篇论文则表明，重型 VLA 控制器可以通过分块规划加在线验证来部署，只需增加一个小型运行时检查，而不必在每一步都调用完整模型。

## 针对使用离散动作 token 的 VLA 策略进行动作通道容量审计
在为机器人感知继续投入更好的编码器之前，离散动作 token 化是一个值得先审计的具体环节。新证据表明，一条常见的升级路径会卡在动作接口上：在 LIBERO-10 上，Diffusion Policy 在 M 尺寸下把编码器从 ResNet-18 换成 SigLIP 后，成绩从 36.4% 提升到 57.6%；而 OAT 在同样升级下只从 53.8% 升到 57.4%。编码器横向比较更明显。Diffusion Policy 从 ResNet-18 的 36.4% 提升到 DINOv2 ViT-L/14 的 63.8%，而 OAT 只在一个更窄的区间内波动，换上更强的编码器时有些结果甚至还下降。

对于训练使用离散动作编码的 VLA 风格策略的团队，一个实用做法是在下一轮编码器升级前先做动作通道容量测试。固定数据集和策略规模，在一小组不同质量的编码器之间替换，观察成功率是否随编码器提升而上升。然后提高 codebook 容量，或在同一任务上与连续动作基线比较。如果编码器变强后策略表现几乎不动，瓶颈很可能在动作表示，而不在视觉栈。

这会给机器人基础模型路线图带来一个有用的采用变化，因为它把一个模糊的扩展问题变成了一个便宜的门控实验。决策也很直接：只有当控制质量会随编码器质量提升而上升时，才继续投入编码器；否则就把精力转到 tokenizer、codebook 大小或连续动作头上。

### Evidence
- [The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling](../Inbox/2026-04-03--the-compression-gap-why-discrete-tokenization-limits-vision-language-action-model-scaling.md): 说明编码器升级对连续动作带来较大增益，但对 LIBERO-10 上的离散动作 token 化只带来较小或不稳定的增益。
- [The Compression Gap: Why Discrete Tokenization Limits Vision-Language-Action Model Scaling](../Inbox/2026-04-03--the-compression-gap-why-discrete-tokenization-limits-vision-language-action-model-scaling.md): 指出在动作被离散化时，动作 tokenizer 是最紧的瓶颈，这为围绕动作通道容量进行审计提供了依据。

## 用于目标图像机器人控制的分层潜在航点规划
对于只给目标图像、但在长任务上失效的世界模型机器人，双层潜在规划器现在已经可以作为一个可接入的控制层来认真测试。HWM 报告称，它先在同一潜在空间里规划潜在宏动作，再规划原子动作，因此在真实 Franka 操作任务上带来了明显提升。在 pick-and-place 任务上，平坦规划的成功率是 0%，HWM 达到 70%。在抽屉开合任务上，成功率从 30% 提升到 70%。同一篇报告还称，图注里给出的规划成本下降约 3 倍，贡献总结里写到推理时规划成本最高可降到 4 倍。

这里的构建方式很具体：在现有学习式世界模型之上增加一个高层潜在航点规划器，然后让低层控制器专注于到达下一个潜在子目标。已经在潜在 rollout 上使用 MPC 的团队可以直接测试这个方法，不需要改任务奖励，也不需要收集新的技能库，因为该方法让两个规划器共享同一个潜在空间，并且在执行过程中持续重规划。

最先适用的用户是那些已经让世界模型在短时域上工作正常、但在多阶段操作上明显失效的研究团队和应用机器人团队。一个便宜的检查方法是，在现有目标图像基准上重新跑一次，用 oracle 子目标和自动生成的潜在子目标做比较。论文报告称，在提供 oracle 子目标时，平坦规划和 HWM 都达到 80%，这说明主要缺的部分是子目标生成。

### Evidence
- [Hierarchical Planning with Latent World Models](../Inbox/2026-04-03--hierarchical-planning-with-latent-world-models.md): 提供了真实机器人上的成功率提升、分层规划机制，以及声称的规划计算量下降。
- [Hierarchical Planning with Latent World Models](../Inbox/2026-04-03--hierarchical-planning-with-latent-world-models.md): 描述了平坦世界模型规划在长时域上的失效方式，以及分层时间抽象为何能解决这个问题。

## 面向高成本 VLA 推理的验证器门控动作分块
在每步推理成本过高的系统上，给分块式 VLA 控制加一个轻量验证器，已经接近可以进入部署测试。SV-VLA 保留大模型 VLA 作为宏规划器，让它先输出一个动作块，然后用一个小验证器根据最新观测检查每一步计划动作。当验证器的判断与计划偏差超过阈值时，系统就从当前状态重新规划。在 LIBERO 上，报告中的三个子任务平均成功率相对开环分块基线从 79.5% 提升到 90.90%。

这支持已经在提供重型操作模型服务的团队做一个具体的流程调整：把控制拆成一个低频规划进程和一个高频验证进程，并把重规划触发次数记录为运维指标。该方法兼容预训练 VLA，因为大模型保持冻结，只有验证器需要训练。

眼下的测试方法很直接。拿一个现有的分块控制器，加上一个小型图像编码器和动作距离门控，然后在同一批任务上比较三种设置：开环分块、验证器门控分块，以及在延迟允许时的逐步闭环。当前证据比前面的规划和动作接口论文更窄，因为摘录里没有给出各任务分数或延迟表，所以它更适合作为已知 VLA 系统的部署实验，而不是对所有机器人控制下一个宽泛结论。

### Evidence
- [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](../Inbox/2026-04-03--open-loop-planning-closed-loop-verification-speculative-verification-for-vla.md): 概述了验证器设计、冻结的大型 VLA 配置，以及 LIBERO 上从 79.5% 提升到 90.90% 的结果。
- [Open-Loop Planning, Closed-Loop Verification: Speculative Verification for VLA](../Inbox/2026-04-03--open-loop-planning-closed-loop-verification-speculative-verification-for-vla.md): 说明了实际运行中的问题：开环分块执行时使用过时观测会导致漂移和控制退化。
