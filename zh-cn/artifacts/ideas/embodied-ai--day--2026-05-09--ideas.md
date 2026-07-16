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

# Operational VLA Policy Checks

## 摘要
机器人 VLA 部署工作已经具体到可以在现有栈里直接测试：给随机动作生成加多样本选择，微调时测保留技能，发布时审计视觉后门和所有权信号。可用的检查很具体：成功率、延迟、旧任务保留率、定向攻击成功率和水印识别置信度。

## Inference-time medoid selection for stochastic robot action chunks
运行扩散或 flow-matching 机器人策略的团队，可以加一层包装器：对同一观察和指令采样多个动作块，在动作空间里把这些块聚类，然后执行最大簇的 medoid。这是一个可直接部署的改动，因为它不需要重新训练策略，也不需要训练单独的评分器。

KeyStone 是具体模板。它把采样得到的 K 个动作块批量处理，用展开后的动作轨迹做 L2 距离，选择一个实际采样到的动作块，这样就避免了在不同动作模式之间取平均。报告中的提升已经足够支持一次本地 A/B 测试：GR00T N1.6 在 SimplerEnv-WidowX 上、K=4 时，成功率从 50.0% 提升到 63.3%；SmolVLA 在 LIBERO 上、K=16 时，成功率从 50.4% 提升到 57.2%。机器人团队可以先记录单样本失败案例，再用 K 取 {4, 8, 16} 重放同一批任务，只有在额外延迟符合控制回路时才采用这个包装器。

### 资料来源
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): KeyStone samples multiple diffusion or flow-matching action chunks, clusters them in action space, and reports success gains across VLA and WAM benchmarks.
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): The paper states that candidate chunks are drawn in parallel from a shared model context and selected without an additional model.

## Prior-task retention checks in VLA fine-tuning jobs
把 VLA 调整到窄演示集的机器人团队，应把旧任务保留率当作必测训练指标。实际训练时，可以保留一小组固定评测集，覆盖空间推理、物体处理和顺序操作，然后在接受新策略前，把普通 SFT 和带置信度加权的损失做对比。

ConSFT 给出了一个低成本的检查方式。它用 stop-gradient 的置信度权重下调高损失转移，并在训练中退火温度，所以低置信度样本产生的更新更小。在 LIBERO 和 π0 上，它把目标任务成功率保持在 0.90，同时把平均旧任务保留率从 0.09 提高到 0.34。ECHO 给出了另一种适合长时程任务的运行时检查：保存成功的子目标片段，在控制时取回这些片段，再把长任务成功率和仅依赖当前观测的基线比较。在 LIBERO-Long 上，ECHO 的成功率是 93.5%，而 vanilla π0 是 80.7%。

### 资料来源
- [Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT](../Inbox/2026-05-09--preserving-foundational-capabilities-in-flow-matching-vlas-through-conservative-sft.md): ConSFT reports a confidence-weighted supervised fine-tuning loss that improves prior-task retention while keeping target-task success close to vanilla SFT.
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO stores successful subgoal segments in a hierarchical memory and reports higher LIBERO-Long success than vanilla π0.

## Visual backdoor and watermark audits for released VLA policies
发布、微调或采购 VLA 机器人策略的组织，需要一个发布门禁来检查视觉触发器和模型所有权证据。这个门禁应包括正常任务成功率、针对性触发测试，以及一个不需要危险机器人动作的独立所有权检查。

ATAAT 说明了为什么普通任务测试不够。在 OpenVLA-7B 的 LIBERO-Spatial 数据投毒场景中，5% 投毒率下，它报告 88.8% 的正常成功率和 83.5% 的定向攻击成功率。触发器既可以是可见物体，也可以是语义场景条件，比如打开的抽屉或戴着手表的人。GuardVLA 提供了一个具体的所有权侧测试：在训练时把固定的 6 位秘密消息嵌入视觉观测，然后在审计时换入触发投影器和分类头。在 LIBERO 和 OpenVLA-OFT 上，水印识别置信度在 Spatial、Goal、Object 和 LIBERO-10 上都接近 100%，而干净模型接近于零。

### 资料来源
- [ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models](../Inbox/2026-05-09--ataat-adaptive-threat-aware-adversarial-tuning-framework-against-backdoor-attacks-on-vision-language-action-models.md): ATAAT reports high targeted attack success under low-rate poisoning while preserving benign success, with visual and semantic triggers.
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA describes a watermark audit with a fixed 6-bit secret message and near-100% watermark identification confidence on tested LIBERO settings.
