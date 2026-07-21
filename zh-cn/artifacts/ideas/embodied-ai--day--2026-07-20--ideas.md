---
kind: ideas
granularity: day
period_start: '2026-07-20T00:00:00'
period_end: '2026-07-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- vision-language-action models
- robot memory
- 3D grounding
- world-model planning
- robustness
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-memory
- topic/3d-grounding
- topic/world-model-planning
- topic/robustness
language_code: zh-CN
---

# 具身控制的状态表示与检查

## 摘要
具身控制团队应以不同速率保留不同信息：为当前场景保留密集的空间细节，跨时间压缩为紧凑的物理记录，并使用独立刷新的状态检查执行结果。现有证据还支持通过对动作敏感的干预来评估世界模型，而不能只看生成轨迹是否合理。

## 对机器人动作完成情况进行独立的物理状态检查
机器人安全与部署团队应根据独立刷新的物理状态检查动作是否完成，而不是依赖策略的推理轨迹。POT-VLA 展示了如何让同一组按角色索引的 3D 对象记录先用于生成动作，再在执行后刷新，用于检验包含、支撑、对齐或交接关系。与 VLA 鲁棒性研究中的文本计划一致性相比，这提供了更具体的监控依据；后者在自适应攻击下的表现降至接近随机水平。

工程上的改动是：在每个动作片段之后，将对象关系，以及在具备力传感时的接触事件，作为一份小型执行契约显式提供给系统。监控器应接收新的传感器测量，而不是隐藏状态或生成的解释；当证据不确定时，应触发重新观测或恢复。一个有用的首轮测试是分别扰动视觉、力觉和策略内部信息，并在相同误报率下，将这一基于状态的检查与计划–动作一致性监控器和动作异常监控器进行比较；结果可以显示，物理落地是否提供了独立的安全信息，而不是对策略输出的另一种观察。

### 资料来源
- [Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation](../Inbox/2026-07-20--closing-the-loop-in-humanoid-vla-persistent-3d-object-tokens-for-verifiable-loco-manipulation.md): POT-VLA 在动作片段后刷新共享的 3D 对象记录，并将真实世界成功次数从 39/80 提高到 71/80。
- [Reasoning as a Double-Edged Sword: Architecture and Cross-Stage Robustness in Vision-Language-Action Models](../Inbox/2026-07-20--reasoning-as-a-double-edged-sword-architecture-and-cross-stage-robustness-in-vision-language-action-models.md): 计划–动作一致性监控器的 AUC 在自适应攻击下从 0.996 降至 0.493，且融合多个监控器并未提高防御后的成功率。
- [FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation](../Inbox/2026-07-20--fm-vla-force-based-memory-for-vision-language-action-models-in-contact-rich-manipulation.md): 八个力记忆 token 捕获了视觉上难以区分的接触历史，并在三个任务中支持了 83.3% 的平均成功率。

## 用于边缘机器人控制的密集当前帧 token 与压缩物理历史
将操作策略部署到受延迟约束的机器人上的工程师，应非对称地分配 token：为当前图像保留密集 patch，但将历史压缩为对象记录和接触记录，而不是保留过去的帧。Patch Policy 的压缩消融实验表明，将当前观测从 256 个 patch 减少到 64 个或更少会损害精确控制；FM-VLA 则显示，长时间的力觉历史可以压缩为八个 token，额外延迟仅为 3.3 ms。POT-VLA 通过持久化的按角色索引 3D 对象槽位，提供了另一种互补的紧凑历史表示。

应在结合精确对齐、遮挡和重复接触的任务上，以固定延迟将这一设计与统一的视觉 token 压缩和采样帧记忆进行比较。与决策直接相关的指标不仅是任务成功率，还包括失败类型：压缩当前帧应增加定位错误，而缺失物理历史应增加计数错误、过早完成和恢复失败。

### 资料来源
- [Patch Policy: Efficient Embodied Control via Dense Visual Representations](../Inbox/2026-07-20--patch-policy-efficient-embodied-control-via-dense-visual-representations.md): 在 Push-T 上，256 个 patch 的得分为 0.69；压缩到 64、16、4 和 1 个 patch 后，得分分别降至 0.52、0.53、0.51 和 0.48。
- [FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation](../Inbox/2026-07-20--fm-vla-force-based-memory-for-vision-language-action-models-in-contact-rich-manipulation.md): FM-VLA 将力觉历史压缩为八个 token，相比基础策略仅增加 3.3 ms 延迟，并且优于采样式视觉记忆。
- [Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation](../Inbox/2026-07-20--closing-the-loop-in-humanoid-vla-persistent-3d-object-tokens-for-verifiable-loco-manipulation.md): POT 使用八个按角色索引的 3D 对象槽位，记录位置、范围、可见性、置信度和空间关系。

## 面向潜在世界模型规划器的动作敏感反事实测试
为机器人或驾驶规划器选择世界模型的团队，应测试预测的未来是否会在动作和场景干预下正确变化，而不是只看生成轨迹是否看起来合理。SAGE 表明，规划性能很大程度上取决于哪些动作序列能够进入冻结的世界模型：移除其排序和 CEM 优化后，预测时域为 150 的 PushT 成功率从 64.7% 降至 16.0%。GeoWorldAD 使用未来几何来指导轨迹优化，但其报告的摘录没有将当前几何与预测的未来几何分离开来。另一方面，Thinking in Video 发现，即使显式因果感知能力很弱，生成器仍能产生看似合理的后续画面。

评估上的改动应是一组匹配的反事实测试：固定观测，只改变一个候选动作或一个具有因果作用的场景变量，然后评估预测的对象几何、碰撞情况和候选排序是否朝正确方向变化。在更大规模的实体机器人试验前运行这项测试，可以区分两类模型：一类能提供与动作相关的动力学信息，另一类的合理未来除了强大的候选生成器或当前场景几何之外，几乎没有额外贡献。

### 资料来源
- [SAGE: Subgoal-Conditioned Action Generation for Latent World Model Planning](../Inbox/2026-07-20--sage-subgoal-conditioned-action-generation-for-latent-world-model-planning.md): 移除世界模型排序和 CEM 优化后，预测时域为 150 的 PushT 成功率从 64.7% 降至 16.0%，表明仅生成候选方案并不足够。
- [GeoWorldAD: Geometry World Action Model for Autonomous Driving](../Inbox/2026-07-20--geoworldad-geometry-world-action-model-for-autonomous-driving.md): GeoWorldAD 预测四个未来几何片段，并在 NAVSIM v1 上报告 91.0 PDMS，但现有摘录缺少完整的当前几何与未来几何对照消融实验。
- [Thinking in Video: Can Video Generators Really Reason About the Real World?](../Inbox/2026-07-20--thinking-in-video-can-video-generators-really-reason-about-the-real-world.md): 根据论文所采用的协议，开源视频生成器在显式因果感知能力接近于零的情况下，仍生成了中等程度合理的后续画面。
