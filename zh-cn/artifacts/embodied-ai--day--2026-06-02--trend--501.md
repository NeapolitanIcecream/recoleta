---
kind: trend
trend_doc_id: 501
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
topics:
- VLA
- robot manipulation
- geometry grounding
- world models
- test-time adaptation
- continual learning
- robot safety
run_id: materialize-outputs
aliases:
- recoleta-trend-501
tags:
- recoleta/trend
- topic/vla
- topic/robot-manipulation
- topic/geometry-grounding
- topic/world-models
- topic/test-time-adaptation
- topic/continual-learning
- topic/robot-safety
language_code: zh-CN
---

# 机器人策略工作正被可执行的对齐能力检验

## Overview
当天的机器人论文都在处理同一个问题：如何让 Vision-Language-Action（VLA）策略在真实部署条件下稳定执行。ERVLA、GeoAlign 和 TTT-VLA 显示出最清楚的一条线索：表现取决于与机器人状态、几何和任务阶段对齐的动作相关信号。

## Clusters

### Geometry-aware action prediction
GeoAlign 和 GeoSem-WAM 都把几何当作控制信号，而不只是感知旁路。GeoAlign 从 RGB 中提取几何特征，让机器人状态查询局部空间特征，并把紧凑的几何 token 输入动作解码器。它在 LIBERO 上报告 99.0% 的平均成功率，在 8 个真实 ALOHA 任务上达到 78.8%，在透明瓶和胶带卷插入任务上提升很大。

GeoSem-WAM 把同样的压力加到 World Action Models（WAMs）上，这类模型学习用于动作的预测性潜在状态。它在未来的 RGB、几何和语义图上训练，然后在部署时移除稠密预测头。报告的真实 Franka 成功率升到 95.4%，高于 Fast-WAM 的 88.9%；LIBERO 消融结果也显示，几何和语义监督一起使用时会带来提升。

#### Evidence
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): GeoAlign summary and results for RGB-derived geometry tokens, LIBERO, SimplerEnv, and real ALOHA performance.
- [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](../Inbox/2026-06-02--geosem-wam-geometry-and-semantic-aware-world-action-models.md): GeoSem-WAM summary and results for geometry/semantic predictive supervision and real Franka gains.

### Action-grounded reasoning supervision
ERVLA 给 embodied chain-of-thought（CoT）一个很窄的角色：它只在训练时提供监督，推理时可以不输出可见文本。论文的消融结果把这一点说得很清楚。像 goal、planning、subtask 和 reasoning 这样的高层字段，如果没有预训练，单独使用只会变差或几乎没有帮助。movement 描述和 point trajectory 更有用，完整的 embodied CoT 方案在这个设置下带来 8.2 个百分点的提升。

缩放结果也很直接。在自回归 CoT-prefix 设置下，加入更大的机器人数据集会让 VLABench 在多个任务上表现下降。ERVLA 不要求在动作 token 之前先生成推理文本，并报告在 LIBERO-Plus 上平均成功率为 86.9%，在 VLABench 上为 53.2%。

#### Evidence
- [Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation](../Inbox/2026-06-02--revisiting-embodied-chain-of-thought-for-generalizable-robot-manipulation.md): ERVLA summary and ablations for embodied CoT fields, scaling behavior, and benchmark results.

### Deployment-time adaptation and phase-aware memory
有两篇论文针对策略离开原始训练设置后出现的失败。TTT-VLA 冻结 VLA 主干，只用自监督的 state-grounding 损失更新 latent prompt token。在 SimplerEnv WidowX 任务上，测试时 prompt 优化后平均成功率升到 67.4%，而 π0.5 基线是 51.1%。

PHASER 处理持续学习。它存储并重放 approach、grasp、transport 这类操作阶段，让短而接触密集的阶段得到保留。对于带 OpenVLA-OFT-7B 的 LIBERO-Long，PHASER 报告平均成功率 85.8%，标准经验回放是 54.6%。

#### Evidence
- [TTT-VLA: Test-Time Latent Prompt Optimization for Vision-Language-Action Models](../Inbox/2026-06-02--ttt-vla-test-time-latent-prompt-optimization-for-vision-language-action-models.md): TTT-VLA summary and results for frozen-backbone latent prompt optimization at deployment.
- [PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models](../Inbox/2026-06-02--phaser-phase-aware-and-semantic-experience-replay-for-vision-language-action-models.md): PHASER summary and results for phase-aware replay in continual VLA learning.

### Real-world access and safety constraints
几篇论文把评估范围从基准策略分数扩展到了更现实的条件。OpenEAI-Platform 用一条 790 美元的开源 6+1 DoF 机械臂和基于 Qwen3-VL-4B 的 VLA 策略降低了硬件门槛，策略在公开机器人和多模态数据上训练。EaDex 用一台 RGB-D 相机采集低成本的人手示范，并把这些示范重定向到三种灵巧机器人手上，配合 demonstration annealing，把自定义任务的平均成功率提高到 36.5%。

安全性证据也已经和可访问性工作一起出现。一个部分可观测的对抗补丁攻击从一段较短的已观测 rollout 前缀中学习一个固定补丁，并把它应用到任务中未见的未来部分。在 LIBERO 上，以 OpenVLA 为受害模型，K=30 时对 Object 的攻击成功率达到 90.7%，对 Long 达到 86.6%，高于这些设置下列出的基线。

#### Evidence
- [OpenEAI-Platform: An Open-source Embodied Artificial Intelligence Hardware-Software Unified Platform](../Inbox/2026-06-02--openeai-platform-an-open-source-embodied-artificial-intelligence-hardware-software-unified-platform.md): OpenEAI-Platform summary and results for low-cost open robot hardware and VLA training setup.
- [EaDex: A Cross-Embodiment Dexterous Manipulation Framework from Low-Cost Demonstrations](../Inbox/2026-06-02--eadex-a-cross-embodiment-dexterous-manipulation-framework-from-low-cost-demonstrations.md): EaDex summary and results for low-cost RGB-D demonstrations and cross-embodiment dexterous manipulation.
- [Partially Observable Adversarial Patch Attacks on Vision-Language-Action Models in Robotics](../Inbox/2026-06-02--partially-observable-adversarial-patch-attacks-on-vision-language-action-models-in-robotics.md): Adversarial patch attack summary and LIBERO attack success results under partial observability.
