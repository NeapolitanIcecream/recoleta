---
kind: ideas
granularity: day
period_start: '2026-07-22T00:00:00'
period_end: '2026-07-23T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- robot learning
- world models
- vision-language-action models
- system reliability
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robot-learning
- topic/world-models
- topic/vision-language-action-models
- topic/system-reliability
language_code: zh-CN
---

# 机器人学习正在改变显式执行接口

## 摘要
机器人部署团队可以通过保留可执行、可检查、可纠正的明确决策，让想象练习和真实世界恢复数据更有用。现有证据支持：在演练阶段使用轨迹级可行性过滤器，并在接口层进行标注，以诊断失败究竟始于目标选择、场景抽象还是控制环节。

## 持续世界模型演练中的可执行轨迹过滤
训练机器人控制器的持续模型基础强化学习团队，应先按执行可行性过滤想象出的演练轨迹，再将其克隆到策略网络中。Dream rehearsal 通过克隆高评分的想象轨迹恢复了被遗忘的行为，而在相同想象数据上进行强化学习却未能恢复；不过，该结果来自 MiniGrid，在那里物理可行性并不是限制因素。KineBench 展示了如何将生成的动作转换为 6D 末端执行器轨迹并在仿真中执行，Koopman Dreamer 则表明，长时域潜变量稳定性会影响闭环控制。

因此，对于连续控制机器人，评分步骤应结合预测回报、仿真器执行结果、运动学可行性和轨迹一致性检查。一项低成本评估是固定想象数据，在已经学会的任务上比较仅按回报选取前四分之一进行克隆与经过可行性过滤后进行克隆的效果，同时测量保留的任务成功率和仿真器拒绝率，而无需收集新的机器人数据。这样可以检验 dream rehearsal 能否迁移到离散环境之外，以及那些表面上有价值的想象轨迹是否因正确的物理原因被拒绝。

### 资料来源
- [The World Model Remembers, the Actor Forgets: Dream Rehearsal for Continual Model-Based RL](../Inbox/2026-07-22--the-world-model-remembers-the-actor-forgets-dream-rehearsal-for-continual-model-based-rl.md): 在世界模型被冻结且使用相同想象数据的情况下，监督式自模仿在 3/3 个随机种子中恢复了被遗忘的技能，而想象中的 RL 在 0/3 个随机种子中恢复了该技能。
- [KineBench: Benchmarking Embodied World Models via IDM-Free Kinematic Grounding](../Inbox/2026-07-22--kinebench-benchmarking-embodied-world-models-via-idm-free-kinematic-grounding.md): KineBench 从生成视频中提取 6D 末端执行器位姿，在 ManiSkill3 中执行这些位姿，并报告了未见轨迹上约 1.5–3 cm 的平移误差。
- [Koopman Dreamer: Spectrally Constrained Latent Dynamics for Stable World-Model Imagination](../Inbox/2026-07-22--koopman-dreamer-spectrally-constrained-latent-dynamics-for-stable-world-model-imagination.md): 受谱约束的潜变量动力学将仿真 UAV 导航的目标成功率从 53.8% 提高到 73.8%；收缩性最强的设置并不总是最佳设置。

## 零售机器人恢复数据的接口级失败标注
零售机器人部署团队应在每个动作之前，标注促成该动作的明确感知决策：选定的目标、任务场景中保留或合并的物体，以及决策不确定时的弃权状态。DEED 已经利用自主失败和人工恢复进行学习，但没有量化各个子系统分别带来了多少收益。ReferTrack 表明，受监督的索引化目标选择可以暴露识别瓶颈；LENS 则会根据执行反馈修改与任务相关的场景抽象。

加入这些接口标签后，操作员可以纠正目标选择或场景相关性，而不必把每次失败都视为无法区分的策略错误。实际比较可以复用同一批恢复片段进行两种更新：普通的端到端后训练，以及接口监督式后训练。通过统计错误目标、遗漏障碍物和后续控制失败的重复出现情况，可以判断额外标签究竟能否减少干预时间，还是只增加标注成本。

### 资料来源
- [Closing the Lab-to-Store Gap: A Data-Efficient Post-Training and Experience-Driven Learning VLA Framework for Retail Humanoids](../Inbox/2026-07-22--closing-the-lab-to-store-gap-a-data-efficient-post-training-and-experience-driven-learning-vla-framework-for-retail-humanoids.md): DEED 收集了 116 个自主 rollout 片段，其中包括 75 个失败片段，并使用人工恢复和潜空间分布监测，但没有报告组件级收益。
- [ReferTrack: Referring Then Tracking for Embodied Visual Tracking](../Inbox/2026-07-22--refertrack-referring-then-tracking-for-embodied-visual-tracking.md): ReferTrack 在预测航点之前先选择检测到的人员索引；在分心跟踪任务中，使用真实目标框的 oracle 变体成功率达到 81.5%，而完整模型为 73.3%。
- [LENS: LLM-guided Environment Simplification for Planning and Control in Clutter](../Inbox/2026-07-22--lens-llm-guided-environment-simplification-for-planning-and-control-in-clutter.md): LENS 会剪除或合并场景实体，并根据失败反馈重新询问模型；其基于模型的控制器在 45 次试验中成功 39 次，而完整场景基线在 30 次试验中成功 17 次。
