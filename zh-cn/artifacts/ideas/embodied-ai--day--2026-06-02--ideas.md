---
kind: ideas
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- VLA
- robot manipulation
- geometry grounding
- world models
- test-time adaptation
- continual learning
- robot safety
tags:
- recoleta/ideas
- topic/vla
- topic/robot-manipulation
- topic/geometry-grounding
- topic/world-models
- topic/test-time-adaptation
- topic/continual-learning
- topic/robot-safety
language_code: zh-CN
---

# 面向接触感知的机器人策略控制

## 摘要
VLA 团队可以对当前机器人策略工作做三项具体改动：为精细操作加入几何条件动作解码，在 rollout 之前做一次局部 latent prompt 适配，在顺序技能训练中按操作阶段存储回放记忆。每一项改动都针对一个会在接触、布局或任务序列压力下出现的失效模式。

## 用于透明物体和插入任务的几何条件动作解码
做精细操作的机器人策略团队应该给动作解码器加上一条几何路径，并在语义识别已经不错但控制会失败的任务上测试它：透明瓶、环形零件、紧配合插入、稳定释放，以及依赖接触的对齐。

GeoAlign 给出了一种具体实现方式。它先在机器人 RGB-D 数据上对 Depth Anything V2-Small 分支做后训练，在执行时丢弃深度头，改用从 RGB 提取的几何特征。机器人状态会生成查询槽，从特征网格里选出局部几何信息，然后用这些紧凑的几何 token 作为条件输入给 flow-matching 动作解码器。这样，执行时只需要 RGB、语言和本体感觉输入，但动作头仍然能拿到局部形状线索。

可行的低成本验证方式是挑一组几何敏感物体任务。GeoAlign 在 8 个真实 ALOHA 任务上的平均成功率是 78.8%，同样设置下 RGB-only 基线是 65.0%；透明瓶成功率从 35.0% 提高到 75.0%，胶带卷插入从 40.0% 提高到 65.0%。GeoSem-WAM 在世界动作模型上也给出同样方向的结果：训练时使用未来几何和语义监督，部署时去掉稠密头，真实 Franka 成功率从 Fast-WAM 的 88.9% 提高到 95.4%。

### 资料来源
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): GeoAlign describes RGB-derived geometry features, state-guided spatial querying, and real ALOHA gains on transparent and insertion tasks.
- [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](../Inbox/2026-06-02--geosem-wam-geometry-and-semantic-aware-world-action-models.md): GeoSem-WAM reports training-time geometry and semantic supervision with deployment-time action prediction and real Franka gains.

## 在新工作区中对冻结的 VLA 策略进行 latent prompt 适配
在冻结的 VLA 策略用于新工作区之前，可以先加一个短的适应步骤。机器人在目标环境里收集交互数据，保持策略骨干不变，只用一个自监督的状态对齐损失来更新学习到的 latent prompt token。这个损失预测末端执行器位置和夹爪状态。

TTT-VLA 是最先可以照着做的具体案例。它在训练时把 latent prompt 加入策略条件输入，然后在测试时用当前环境的数据去适配这个 prompt。在 SimplerEnv 的 WidowX 单本体任务上，π0.5 的平均成功率从 51.1% 提高到 63.5%，加入状态对齐的 latent prompt 后提高到 67.4%，再经过测试时 prompt 优化后仍是 67.4%。这个方法在 Google Robot 的视觉匹配上也把成功率从 67.5% 提高到 72.4%。

这个方案最适合那些已经信任基础策略，但在相机、光照、物体摆放或本体变化后会失效的团队。论文里报告的算力开销较高，列出的实验需要 8 张 NVIDIA H100 GPU 上 15 到 30 分钟，所以实际上的第一步检查应该是离线回放或仿真实验，测一测只更新 prompt 能不能修正少量重复出现的决策错误，同时不改策略权重。

### 资料来源
- [TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models](../Inbox/2026-06-02--ttt-vla-test-time-latent-prompt-optimization-for-vision-language-action-models.md): TTT-VLA describes frozen-backbone latent prompt optimization with a self-supervised state-grounding loss and reports SimplerEnv gains.
- [TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models](../Inbox/2026-06-02--ttt-vla-test-time-latent-prompt-optimization-for-vision-language-action-models.md): The paper states that test-time optimization updates only the latent prompt using data from the current environment.

## 用于顺序操作技能训练的阶段感知回放缓冲区
对一串操作技能做微调的 VLA 策略团队，应该按子技能阶段存储回放数据，而不只是按轨迹或任务存。实际问题很直接：像抓取这种短暂但接触密集的阶段，如果回放帧按统一比例抽样，得到的样本会太少，尽管这些帧决定整项任务能不能成功。

PHASER 会把轨迹切成接近、抓取、搬运这类阶段，给每个阶段分配相同的帧预算，并把回放导向那些很可能和当前阶段冲突的旧阶段。这个路由会用语言相似度、视觉相似度和动作差异来打分，分数只在任务切换时计算一次。Auto-PC 可以通过动作信号的变点检测，再加上 VLM 语义验证，提出阶段边界，从而减少人工标注的需求。

最先可以做的实现，是在现有微调流水线外面改一个缓冲区：把示范切成阶段，每个阶段预留相同内存，然后在一个顺序 LIBERO 风格套件上和统一经验回放比较。PHASER 在 OpenVLA-OFT-7B 上的 LIBERO-Long 平均成功率是 85.8%，标准经验回放是 54.6%。同一篇论文还报告了在 QwenGR00T-3B 和 QwenOFT-3B 上的大幅提升，所以在改策略架构之前，先测试缓冲区设计是值得的。

### 资料来源
- [PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models](../Inbox/2026-06-02--phaser-phase-aware-and-semantic-experience-replay-for-vision-language-action-models.md): PHASER describes phase-aware storage, replay routing, Auto-PC phase discovery, and gains over standard experience replay.
- [PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models](../Inbox/2026-06-02--phaser-phase-aware-and-semantic-experience-replay-for-vision-language-action-models.md): The paper explains why uniform replay under-samples short but critical manipulation phases.
