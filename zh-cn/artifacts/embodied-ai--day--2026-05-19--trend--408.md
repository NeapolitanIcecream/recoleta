---
kind: trend
trend_doc_id: 408
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
topics:
- Embodied AI
- Vision-language-action models
- Robot manipulation
- World models
- Robot evaluation
- Synthetic data
run_id: materialize-outputs
aliases:
- recoleta-trend-408
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-manipulation
- topic/world-models
- topic/robot-evaluation
- topic/synthetic-data
language_code: zh-CN
---

# 具身 AI 论文把执行时可靠性变成可测量指标

## Overview
具身 AI 主导了这个时期。VLA 工作按延迟、光照、扰动和细粒度任务阶段来评估，世界模型论文则在做更长的 rollout 和更便宜的合成数据。DEFLECT、MetaFine 和 WEM 给出的信号最清楚。

## Clusters

### VLA deployment reliability
一些论文把 VLA 可靠性当作运行时问题来处理，并明确列出故障模式。DEFLECT 处理异步推理场景：机器人在下一段动作还在计算时，先执行了旧的动作块。它用新旧动作偏好进行训练，把 Kinetix 在 d=0–7 各种延迟下的成功率提高到 83.3%，在训练时未见过的高延迟 d=5–7 上成功率为 73.5%。

RoVLA 为改写指令、去噪时间步和扰动观测加入一致性损失。现有摘录里的证据更偏定性，但它的设置覆盖了 LIBERO-Plus 的多种扰动，包括布局、相机、机器人初始化、语言、光照、背景和传感器噪声。RoHIL 给出一个更窄的真实机器人案例：它对录制轨迹重新打光，并在离线状态下微调，在文中给出的锚定设置里把 USB 插入的源域成功率和偏移光照成功率都做到 1.00。

#### Evidence
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): DEFLECT method and delay-robust robot results.
- [RoVLA: Multi-Consistency Constraints for Robust Vision-Language-Action Models](../Inbox/2026-05-19--rovla-multi-consistency-constraints-for-robust-vision-language-action-models.md): RoVLA consistency training and perturbation coverage.
- [RoHIL: Robust Human-in-the-Loop Robotic Reinforcement Learning Against Illumination Variations](../Inbox/2026-05-19--rohil-robust-human-in-the-loop-robotic-reinforcement-learning-against-illumination-variations.md): RoHIL offline relighting and real-robot lighting adaptation results.

### Policy optimization focuses on the actions that change outcomes
这个时间窗里的训练论文关注哪些更新对闭环控制真正重要。PAPO-VLA 把规划动作和密集执行动作分开，再提高那些被估计为同时满足因果充分性和必要性的动作的更新权重。摘录没有给出 PAPO-VLA 的最终分数，所以能确认的贡献是动作级优势设计。

Pion 处理的是更底层的优化器失效。它指出，Muon 会在低秩 VLA 动作模块梯度和低信号的可验证奖励强化学习（RLVR）中放大带噪的小奇异方向。Pion 保留 Muon 风格的更新路径，但抑制尾部奇异方向。在 VLA-Adapter 和 LIBERO Object 上，它在 1,500 步后达到 100% 成功率，而 Muon 为 97.0%，AdamW 为 32.2%。

#### Evidence
- [PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-19--papo-vla-planning-aware-policy-optimization-for-vision-language-action-models.md): PAPO-VLA planning-aware advantage formulation.
- [Rethinking Muon Beyond Pretraining: Spectral Failures and High-Pass Remedies for VLA and RLVR](../Inbox/2026-05-19--rethinking-muon-beyond-pretraining-spectral-failures-and-high-pass-remedies-for-vla-and-rlvr.md): Pion optimizer mechanism and LIBERO Object result.

### Fine-grained evaluation exposes hidden manipulation failures
MetaFine 是这一时期最强的评估论文。它把操作任务拆成语言理解、空间感知和运动行为检查，然后用 grasp-part、align、insert、press-part、toggle-part、rotate-along 和 slide-along 这类原子技能取代单一的通过/失败分数。

报告中的差距很大。常规评估会把细粒度能力高估最多 70%。物体级抓取通常高于 95%，而最好的策略在部件级约束下只在 Grasp Part 上达到 80%，在 Press Part 上达到 68%，在 Rotate Along 上达到 12%。在语义替换测试中，5 个被评估的 VLA 在修改后的指令上都得了 0%。在 peg-in-hole 任务上，总体成功率仍接近 0，但阶段指标能显示策略在哪里失败。

#### Evidence
- [Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation](../Inbox/2026-05-19--beyond-binary-success-a-diagnostic-meta-evaluation-framework-for-fine-grained-manipulation.md): MetaFine diagnostic design and fine-grained manipulation results.

### World models are being built for longer embodied data and physics checks
世界模型工作覆盖机器人 rollout、视频物理和合成航空数据。WEM 把长时程预测拆成场景级世界状态和机器人或物体的自我状态，然后在 HTEWorld 上测试混合导航-操作任务。这个数据集包含 125K 训练片段、超过 4.5M 帧、300 条评估轨迹，以及超过 2K 条指令。

PhyWorld 对 Wan2.2-I2V-A14B 做继续视频生成和物理偏好后训练。它的结果是视频指标，不是机器人控制：VBench 上为 0.769，物理一致性基准上为 3.09。FlyMirage 把生成式场景创建用于航空视觉语言导航，生成了 500 个 3D Gaussian Splatting 场景，以及约 50,000 条动态可行的 6-DoF UAV 轨迹，按文中报告每个场景的成本约为 2 美元。

#### Evidence
- [World-Ego Modeling for Long-Horizon Evolution in Hybrid Embodied Tasks](../Inbox/2026-05-19--world-ego-modeling-for-long-horizon-evolution-in-hybrid-embodied-tasks.md): WEM world-ego split and HTEWorld scale.
- [PhyWorld: Physics-Faithful World Model for Video Generation](../Inbox/2026-05-19--phyworld-physics-faithful-world-model-for-video-generation.md): PhyWorld video continuation and physics benchmark results.
- [FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model](../Inbox/2026-05-19--flymirage-a-fully-automated-generation-pipeline-for-diverse-and-scalable-uav-flight-data-via-generative-world-model.md): FlyMirage synthetic UAV scene and trajectory generation results.
