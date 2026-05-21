---
kind: ideas
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- Vision-Language-Action
- robot manipulation
- long-horizon memory
- fine-tuning retention
- inference-time action selection
- world models
- robot security
- model ownership
- hardware agents
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/long-horizon-memory
- topic/fine-tuning-retention
- topic/inference-time-action-selection
- topic/world-models
- topic/robot-security
- topic/model-ownership
- topic/hardware-agents
language_code: zh-CN
---

# 可操作的 VLA 策略检查

## Summary
机器人 VLA 部署工作已经具体到可以在现有栈中测试：用多样本选择包装随机动作生成，在微调期间测量保留技能，并审计已发布策略中的视觉后门和所有权信号。有用的检查项都很小且便于操作：成功率、延迟、先前任务保留率、定向攻击成功率和水印识别置信度。

## 随机机器人动作块的推理时 medoid 选择
运行扩散或流匹配机器人策略的团队可以加一个包装层：针对同一观察和指令采样多个动作块，在动作空间中对这些动作块聚类，并执行最大簇的 medoid。这个改动可以直接部署，因为它不需要重新训练策略，也不需要训练单独的评分器。

KeyStone 是具体模板。它批量处理 K 个采样动作块，对展平后的动作轨迹使用 L2 距离，并选择一个真实采样到的动作块，从而避免在不同运动模式之间求平均。报告中的收益足以支持本地 A/B 测试：GR00T N1.6 在 SimplerEnv-WidowX 上的成功率在 K=4 时从 50.0% 升至 63.3%，SmolVLA 在 LIBERO 上的成功率在 K=16 时从 50.4% 升至 57.2%。机器人团队可以记录单样本失败案例，用 K in {4, 8, 16} 重放相同任务，并且只在新增延迟符合控制循环要求时接受这个包装层。

### Evidence
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): KeyStone 采样多个扩散或流匹配动作块，在动作空间中对它们聚类，并报告了 VLA 和 WAM 基准上的成功率提升。
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): 论文称，候选动作块是在共享模型上下文中并行抽取的，并且不使用额外模型来选择。

## VLA 微调任务中的先前任务保留检查
将 VLA 适配到窄范围演示集的机器人团队，应把先前任务保留率作为必需的训练指标。一个实用的训练任务可以为空间推理、物体操作和顺序操作保留一个小型固定评估集，然后在接受适配后的策略之前，比较普通 SFT 和置信度加权损失。

ConSFT 为这项检查提供了低成本机制。它用停止梯度的置信度权重降低高损失转移的权重，并在训练中退火温度，因此低置信度样本产生更小的更新。在使用 π0 的 LIBERO 上，它的目标任务成功率与普通 SFT 同为 0.90，并将平均先前任务保留率从 0.09 提高到 0.34。ECHO 给长期任务提供了一个相关的运行时检查：存储成功的子目标片段，在控制过程中检索它们，并将长任务成功率与只使用当前观察的基线比较。在 LIBERO-Long 上，ECHO 报告的成功率为 93.5%，普通 π0 为 80.7%。

### Evidence
- [Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT](../Inbox/2026-05-09--preserving-foundational-capabilities-in-flow-matching-vlas-through-conservative-sft.md): ConSFT 报告了一种置信度加权的监督微调损失，可以在让目标任务成功率接近普通 SFT 的同时提高先前任务保留率。
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO 将成功的子目标片段存入分层记忆，并报告了高于普通 π0 的 LIBERO-Long 成功率。

## 已发布 VLA 策略的视觉后门和水印审计
发布、微调或购买 VLA 机器人策略的组织需要一个发布门禁，用来测试视觉触发器和模型所有权证据。这个门禁应包括正常任务成功率、定向触发器试验，以及一项不需要危险机器人动作的独立所有权检查。

ATAAT 说明了为什么正常任务测试不够。在使用 OpenVLA-7B 的 LIBERO-Spatial 数据投毒中，投毒率为 5% 时，它报告的正常成功率为 88.8%，定向攻击成功率为 83.5%。触发器集合包括可见物体，也包括语义场景条件，例如打开的抽屉或戴手表的人。GuardVLA 给出了一项具体的所有权侧测试：在训练期间把固定的 6-bit 秘密消息嵌入视觉观察，然后在审计时换入触发器投影器和分类头。在使用 OpenVLA-OFT 的 LIBERO 上，Spatial、Goal、Object 和 LIBERO-10 的水印识别置信度接近 100%，而干净模型接近零。

### Evidence
- [ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models](../Inbox/2026-05-09--ataat-adaptive-threat-aware-adversarial-tuning-framework-against-backdoor-attacks-on-vision-language-action-models.md): ATAAT 报告称，在低比例投毒下，它能在保留正常成功率的同时取得较高的定向攻击成功率，并支持视觉和语义触发器。
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA 描述了一种水印审计方法，使用固定的 6-bit 秘密消息，并在测试的 LIBERO 设置上取得接近 100% 的水印识别置信度。
