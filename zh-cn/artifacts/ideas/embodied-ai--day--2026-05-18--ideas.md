---
kind: ideas
granularity: day
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-19T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- robot manipulation
- VLA models
- dexterous robotics
- world models
- robot benchmarks
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robot-manipulation
- topic/vla-models
- topic/dexterous-robotics
- topic/world-models
- topic/robot-benchmarks
language_code: zh-CN
---

# Physical Rollout Evaluation for Robot Policies

## Summary
真实机器人回放指标正在成为 VLA 和世界模型工作的有效筛选器。最直接的做法，是给遥操作灵巧数据加质量评分，在部署前测试 VLA 策略对摄像头腐蚀的鲁棒性，并在桌面任务里把场景保留和接触效用与任务完成度一起评分。

## Clip-quality scoring for noisy dexterous teleoperation datasets
采集双臂灵巧示教的机器人实验室，应在训练策略前加入按片段计算的质量分数。Dexora 给出了一个具体做法：两条 6-DoF 机械臂、两只 12-DoF 机械手、四路 RGB 视角、20 Hz 的关节状态、一个匹配的 MuJoCo 数字孪生，以及一个由离线判别器加权损失的扩散策略，低质量示教会被降权。

问题出在流程上。高 DoF 遥操作数据里有操作者差异、跟踪误差、遮挡和延迟。把所有回放都丢进训练，会把不稳定片段当成有效监督。一个小型判别器或评估器，如果能给完成度、接触稳定性、物体位姿漂移和手部跟踪置信度打分，就能把普通数据集变成可训练语料。

一个低成本的起点，是给现有遥操作数据重新打分，用有质量权重和无质量权重分别训练同一策略，再在需要手指灵活性的任务上比较物理回放，比如旋盖、写字、取书或揉面。Dexora 在灵巧任务上的结果，平均成功率 66.7%，高于 GR00T N1 的 51.7% 和 Diffusion Policy 的 6.7%，这个差距足以先在更小的本地平台上试一轮。

### Evidence
- [Dexora: Open-source VLA for High-DoF Bimanual Dexterity](../Inbox/2026-05-18--dexora-open-source-vla-for-high-dof-bimanual-dexterity.md): Dexora combines a 36-DoF dual-arm dual-hand robot, matched MuJoCo twin, 100K simulated trajectories, 10K real teleoperated episodes, and quality-weighted diffusion policy training.
- [Dexora: Open-source VLA for High-DoF Bimanual Dexterity](../Inbox/2026-05-18--dexora-open-source-vla-for-high-dof-bimanual-dexterity.md): The paper abstract describes the hybrid teleoperation interface, synthetic and real datasets, and the offline discriminator for down-weighting low-quality demonstrations.

## Camera-corruption regression tests for VLA robot policies
VLA 部署团队应在实机试验前加入摄像头腐蚀回归测试套件。StableVLA 直接说明了这个失效模式：在干净相机输入下可用的策略，遇到模糊、噪声、类天气效应和训练时没有见过的数字伪影时会失效。

实际实现并不复杂。拿团队常用的验证片段或仿真回放，施加常见视觉腐蚀的固定强度等级，然后按任务类别汇报成功率。对于使用类似 VLA-Adapter 的视觉编码器和语言策略之间桥接层的策略，可以测试一种基于 StableVLA 信息瓶颈适配器的替代视觉投影层。这个设计通过并行路径过滤噪声特征，同时保留空间细节，新增参数少于 10M，也不需要额外机器人数据。

验收测试应包含策略在正常干净输入下的分数、最差腐蚀场景，以及至少一次带有人为相机退化的真实机器人试验。StableVLA 报告的 LIBERO 5 级结果里，Object 是 70.2% 对 29.3%，Long 是 45.3% 对 26.2%；真实 Pack Doll 任务里，成功率是 50%，而 VLA-Adapter-0.5B 是 20%。

### Evidence
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): StableVLA identifies visual corruptions as a deployment failure mode and reports large LIBERO, CALVIN, and real-robot gains without extra robot data or corruption-specific augmentation.
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): The abstract states that IB-Adapter filters noisy visual inputs, adds fewer than 10M parameters, and improves over the baseline without extra data or augmentation.

## Scene-preserving and contact-utility scoring for tabletop dexterity
评估灵巧桌面机器人的团队，应在每次动作后检查桌面是否仍然可用。DexHoldem 给了一个直接模板：物理回放使用四级评分，把保留场景的成功、破坏性完成、任务失败和破坏性失败分开。这个区分很重要，因为机械手可以完成一张牌或一个筹码的动作，却把下一步决策状态弄坏。

这个评分很容易加到小型桌面任务里。定义合法结束状态、物体位移上限、筹码或部件库存检查，以及恢复触发条件。把任务完成度和场景保留分开记录。对于带触觉传感器或学习动力学的系统，再加一个接触效用检查，把触觉重建和后续动作成功率对比起来。

WorldArena 2.0 说明了为什么接触型模型需要这个额外分数。Wan2.2 在 UniVTAC 上的触觉预测质量最好，21.26 PSNR、0.746 SSIM，但在 Insert HDMI 和 Lift Bottle 两个任务上的平均成功率只有 50%。有用的评测框架应把触觉或视频质量和物理回放成功率放在一起看，因为重建干净，不代表控制证据够用。

### Evidence
- [DexHoldem: Playing Texas Hold'em with Dexterous Embodied System](../Inbox/2026-05-18--dexholdem-playing-texas-hold-em-with-dexterous-embodied-system.md): DexHoldem uses a physical rollout rubric that separates scene-preserving success from disruptive completion and reports large gaps between task completion and scene-preserving success.
- [WorldArena 2.0: Extending Embodied World Model Benchmarking on Modality, Functionality and Platform](../Inbox/2026-05-18--worldarena-2-0-extending-embodied-world-model-benchmarking-on-modality-functionality-and-platform.md): WorldArena 2.0 adds visuotactile evaluation and shows that high tactile reconstruction scores do not reliably predict task success.
