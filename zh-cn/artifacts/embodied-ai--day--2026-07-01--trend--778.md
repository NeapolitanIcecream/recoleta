---
kind: trend
trend_doc_id: 778
granularity: day
period_start: '2026-07-01T00:00:00'
period_end: '2026-07-02T00:00:00'
topics:
- robotics
- vision-language-action models
- world models
- robot evaluation
- long-horizon manipulation
- robot safety
- tactile pretraining
- sim2real
- robot serving
run_id: materialize-outputs
aliases:
- recoleta-trend-778
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/robot-evaluation
- topic/long-horizon-manipulation
- topic/robot-safety
- topic/tactile-pretraining
- topic/sim2real
- topic/robot-serving
language_code: zh-CN
---

# 机器人学习论文让 VLA 策略承受执行压力

## Overview
机器人学主导了这一时期。最强的论文把视觉-语言-动作（VLA）策略放到 rollout 成本、长时程漂移、碰撞风险、触觉数据缺口和工厂服务等执行压力下测试。RoboWorld、FurnitureVLA 和 ROSA 给出了最清晰的实测主张。

## Clusters

### 用于评估和控制的世界模型
RoboWorld 给出了最清晰的世界模型结果。它通过 4,186 次生成 rollout 评估八个开放机器人策略，并与 RoboArena 真实世界排名达到 Pearson r=0.989、Spearman rho=0.970 的一致性。关键设计是闭环 rollout 生成，加上一个按 0–5 分评估任务进度的视觉语言模型裁判；在报告的消融实验中，这比二元成功评分提供了更多信息。

其他论文把控制连接说得更明确。ABot-M0.5 为移动操作定义了世界动作模型（WAM），按顺序预测未来视频、潜在运动和可执行机器人动作。教程论文也试图收紧术语：它把机器人世界模型定义为以动作为条件的预测器，并按预测未来如何连接到动作来归类 WAM 设计。实测证据最强的是 RoboWorld；在可用摘录中，ABot-M0.5 和教程主要澄清模型设计选择。

#### Evidence
- [RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation](../Inbox/2026-07-01--roboworld-fast-and-reliable-neural-simulators-for-generalist-robot-policy-evaluation.md): RoboWorld 摘要报告了闭环神经评估、Step Forcing、4,186 次生成 rollout，以及与 RoboArena 的排名一致性。
- [ABot-M0.5: Unified Mobility-and-Manipulation World Action Model](../Inbox/2026-07-01--abot-m0-5-unified-mobility-and-manipulation-world-action-model.md): ABot-M0.5 摘要描述了面向移动操作的未来视频、潜在动作和可执行动作预测。
- [From World Models to World Action Models: A Concise Tutorial for Robotics](../Inbox/2026-07-01--from-world-models-to-world-action-models-a-concise-tutorial-for-robotics.md): 教程摘要定义了世界模型和世界动作模型，包括用于综合的分类法。

### 长时程操作开始按任务完成、接触和安全评分
FurnitureVLA 是主要的长时程操作结果。它把 IKEA 风格的双臂装配分解为以语言为条件的子任务，并在预测 14 维双臂动作的同时预测连续子任务进度。在仿真中，LACK、KALLAX 和 IVAR 三类任务的平均完整装配成功率从单体微调的 0.48 提升到 0.80。

安全工作增加了另一项执行测试。受约束流匹配论文在去噪过程中编辑预测的 10 步末端执行器轨迹，在动作块最终确定前使用控制屏障函数约束。在 SafeLIBERO 上，它报告 82.81% 的避碰率和 81.62% 的任务成功率；无引导 π0.5 为 18.69% 和 50.88%。这种提升伴随执行变慢，结果体现安全与吞吐的权衡，不能算无成本改进。

#### Evidence
- [FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model](../Inbox/2026-07-01--furniturevla-learning-long-horizon-bimanual-furniture-assembly-with-vision-language-action-model.md): FurnitureVLA 摘要给出了子任务进度方法和仿真成功率提升。
- [Neuro-Symbolic Safety Guidance for Vision-Language-Action Models via Constrained Flow Matching](../Inbox/2026-07-01--neuro-symbolic-safety-guidance-for-vision-language-action-models-via-constrained-flow-matching.md): 安全引导摘要报告了轨迹级受约束流匹配和 SafeLIBERO 结果。

### 感知、触觉和检索成为策略输入
触觉预训练获得了一项具体数据贡献。H-Tac 包含 160 小时、300 多个任务和超过 135,000 个 episode，信号包括触觉、动作、视觉和语言。Transferable Tactile Pre-Training 增加了一个触觉专家，在预测动作块的同时预测未来触觉读数。摘录给出了数据集规模，但所供文本没有下游成功率。

数据访问也得到实际关注。Daft 文章展示了在 Apple EgoDex 上进行逐帧搜索，使用 SigLIP-2 文本-视频嵌入加手部姿态几何。示例检索到订书机抓握、积木抬起、T 恤折叠片段等事件。这对机器人团队有用，因为精细操作失败常藏在很长且未标注的 episode 中。

认证感知时钟形成第三条面向传感器的线索。一个冻结的 3D VN-JEPA 世界模型给出漂移感知的重新感知截止时间；在三项测试中，留出区间证书违例上界低于声明的 0.15 目标。

#### Evidence
- [Human-Centric Transferable Tactile Pre-Training for Dexterous Robotic Manipulation](../Inbox/2026-07-01--human-centric-transferable-tactile-pre-training-for-dexterous-robotic-manipulation.md): TTP 摘要提供了 H-Tac 规模、触觉-动作预训练设计，以及所报告下游指标的限制。
- [Finding a Needle in the Haystack: Querying Physical AI Data with Daft](../Inbox/2026-07-01--finding-a-needle-in-the-haystack-querying-physical-ai-data-with-daft.md): Daft 摘要描述了使用文本嵌入和手部姿态几何进行逐帧 EgoDex 检索。
- [Certified World Models as Sensing Clocks: Drift-Aware Deadlines for Active Perception](../Inbox/2026-07-01--certified-world-models-as-sensing-clocks-drift-aware-deadlines-for-active-perception.md): 认证世界模型摘要报告了漂移感知的感知截止时间和留出区间违例结果。

### 部署工作瞄准域变化和共享 GPU 使用
适应和服务论文关注策略离开训练设置后的情况。DART 使用一个任务的一条目标域演示，加上一条匹配的源域演示，把 VLA 适配到新的相机、光照、传感器或具身条件。它从权重更新中提取域向量并加到基础策略上，但所供摘录不含成功率表。

BIFROST 通过共享潜在历史编码器处理 sim-to-real 迁移，该编码器用成对的跨域片段训练。在 sim-to-sim 导航中，它报告顶视图成功率为 0.68 ± 0.08，自我中心视图为 0.50 ± 0.08；较弱的直接迁移基线为 0.19 ± 0.04 和 0.03 ± 0.02。摘录声称进行了 sim-to-real 测试，但没有量化表格。

ROSA 把机器人基础模型推理作为机队调度问题处理。在八块 H200 GPU 和最多 64 个虚拟机器人上，它报告符合 SLO 的工厂生产率最高比专用服务基线高 12.06×，最高比不使用其调度器的共享服务器基线高 2.44×。

#### Evidence
- [Domain Arithmetic: One-Shot VLA Adaptation under Environmental Shifts](../Inbox/2026-07-01--domain-arithmetic-one-shot-vla-adaptation-under-environmental-shifts.md): DART 摘要描述了一次性域向量适配，并指出摘录缺少数值差距。
- [BIFROST: Bridging Invariant Feature Representation for Observation-space Sim2Real Transfer](../Inbox/2026-07-01--bifrost-bridging-invariant-feature-representation-for-observation-space-sim2real-transfer.md): BIFROST 摘要给出了成对潜在编码器方法和 sim2sim 成功率。
- [ROSA: A Robotics Foundation Model Serving System for Robot Factories](../Inbox/2026-07-01--rosa-a-robotics-foundation-model-serving-system-for-robot-factories.md): ROSA 摘要报告了共享 GPU 池调度和工厂生产率提升。
