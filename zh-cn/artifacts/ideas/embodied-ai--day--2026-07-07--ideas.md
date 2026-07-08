---
kind: ideas
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- world models
- 3D manipulation
- imitation learning
- dexterous manipulation
- robot planning
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/3d-manipulation
- topic/imitation-learning
- topic/dexterous-manipulation
- topic/robot-planning
language_code: zh-CN
---

# VLA 策略执行检查

## Summary
机器人策略团队可以处理三个具体压力点：基于 flow 的 VLA 控制中的 action head 延迟、链式家务技能之间薄弱的就绪检查，以及模仿学习中浪费算力的演示池。每个问题都有一条小规模实现路径，可用当前策略日志或基准 rollout 测试。

## 面向基于 flow 的 VLA 控制循环的 action-chunk 缓存
部署基于 flow 的 VLA 策略的团队，应在推理路径中加入外部 action-chunk 缓存，并在同一任务分布下测量成功率-延迟曲线。ActionCache 用紧凑的多模态键保存过去的中间 action chunk，为当前上下文检索相近的 chunk，然后直接执行，或用一到两个 flow 步进行细化。实际测试范围很小：用成功 rollout 构建缓存，设置相似度阈值以便在需要时回退到完整生成，并在重复操作任务上比较控制延迟、缓存命中率和任务成功率。

论文报告的数字值得直接做工程试验。在 VLABench 上使用 π0.5 时，完整模型达到 38.8% 成功率，action head 延迟为 18.8 ms。ActionCache 不做细化时达到 32.9% 成功率，延迟为 1.6 ms；一步版本达到 32.4%，延迟为 3.6 ms。不做检索的简单一步生成降到 6.8%，说明有效部分来自相似上下文的复用，而不只是 flow 步数减少。这适合 VLA action head 占控制循环预算较大、且重新训练 backbone 成本高的实验室。

### Evidence
- [Training-Free Acceleration for Vision-Language-Action Models with Action Caching and Refinement](../Inbox/2026-07-07--training-free-acceleration-for-vision-language-action-models-with-action-caching-and-refinement.md): 概述 ActionCache 的缓存并细化方法、无需重新训练的设置，以及在 π0.5 和 GR00T-N1.6 上的成功率-延迟结果。
- [Training-Free Acceleration for Vision-Language-Action Models with Action Caching and Refinement](../Inbox/2026-07-07--training-free-acceleration-for-vision-language-action-models-with-action-caching-and-refinement.md): 描述闭环机器人控制中，迭代式扩散或 flow 生成的 action head 延迟瓶颈。

## 面向长时程 VLA 技能库的下一技能就绪检查
把 VLA 技能组合成家务任务的机器人团队，应在评估 harness 中加入类型化技能契约和下一技能就绪检查。一次技能调用需要的不只是局部成功标签：它应携带参数、步数预算、验证器间隔、预期后置条件，以及下一项技能可以启动的条件。抓取前的导航可以包括目标可见性和手臂可达就绪状态。另一个操作步骤前的放置可以包括物体位姿和相机视角检查。

BEHAVIOR-1K 交接研究说明了为什么这层支持应进入评估。多个孤立技能在干净快照中得分很高，包括 pick_up_from 的 96.5% 和 place_on 的 100.0%，但组合任务谓词成功率被描述为接近零。在 30 次 rollout 中，平均进度为 19.5%。在一组 10 次 rollout 的轨迹中，harness 记录了 130 次失败的技能尝试，类别包括抓取控制、执行、放置、目标定位或场景搜索，以及导航就绪。一个低成本采用步骤是用多视角 VLM 每隔固定数量的模拟器步数验证现有链式 rollout，然后记录每次失败来自当前技能、交接状态，还是下一技能的启动条件。

### Evidence
- [Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition](../Inbox/2026-07-07--diagnosing-semantic-handoff-failures-in-agent-orchestrated-vision-language-action-skill-composition.md): 给出类型化契约执行 harness、验证器循环、孤立技能结果、接近零的组合成功率，以及失败计数。
- [Diagnosing Semantic Handoff Failures in Agent-Orchestrated Vision-Language-Action Skill Composition](../Inbox/2026-07-07--diagnosing-semantic-handoff-failures-in-agent-orchestrated-vision-language-action-skill-composition.md): 解释语义交接问题，并给出超出局部后置条件的下一技能就绪示例。

## VLA 模仿学习运行前的 primitive 级演示选择
在大型机器人演示池上训练 VLA 策略的团队，应在投入完整算力前运行一次 primitive 级数据选择。SIEVE 在夹爪或手部状态变化处切分轨迹，对得到的视觉-运动片段聚类，把每条轨迹表示为有序 primitive 序列，并在这些序列桶内选择中心轨迹。这给数据整理团队提供了一个具体流程：切分日志，对可复用行为单元聚类，为 primitive 转换覆盖分配选择预算，然后在选出的子集和随机子集上训练同一个策略作对照。

Bridge-V2 结果足够具体，可以做复现实验。使用 Qwen3-VL-4B-GR00T 时，SIEVE 用 50% 的演示和 25K 训练步数，在 SimplerEnv-WidowX 上达到 56.3% 平均成功率，高于完整数据训练在 50K 步数下的 51.8%。该方法针对机器人数据管线中的常见运行问题：重复轨迹、噪声动作和不均衡任务覆盖会增加计算量，同时给行为克隆提供不一致的监督。最适合先采用这套流程的是拥有大量遥操作日志且训练预算有限的团队，因为它可以在不改变 VLA 模型的情况下测试选择器。

### Evidence
- [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](../Inbox/2026-07-07--sieve-structure-aware-data-selection-for-imitation-learning-with-vla-models.md): 概述 SIEVE 的切分、聚类、medoid 选择，以及 Bridge-V2 成功率结果。
- [SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models](../Inbox/2026-07-07--sieve-structure-aware-data-selection-for-imitation-learning-with-vla-models.md): 说明大型机器人演示集中的数据质量问题，以及 50% 数据和 50% 步数可以超过完整数据训练的主张。
