---
kind: trend
trend_doc_id: 318
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
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
run_id: materialize-outputs
aliases:
- recoleta-trend-318
tags:
- recoleta/trend
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

# 机器人 VLA 可靠性正在记忆、动作和发布环节接受测试

## Overview
当天的机器人研究将 Vision-Language-Action (VLA) 模型视为可部署的控制系统。ECHO 扩展长时程记忆，KeyStone 改进推理时的随机动作选择，ATAAT 表明视觉后门可以在调优后保留下来。共同测试点是：机器人策略在更长任务、新数据、不确定样本和已发布模型风险下，能否保留有用行为。

## Clusters

### VLA 记忆和技能保留
ECHO 和 ConSFT 关注一个基本部署问题：机器人策略必须记住有用经验，并在任务适配后保留旧技能。ECHO 将成功的子目标片段存入分层双曲记忆，并在控制过程中检索这些片段。在 LIBERO-Long 上，它报告的成功率为 93.5%，原版 π0 为 80.7%；在不使用 LIBERO-Long 目标记忆的情况下，跨套件泛化达到 89.31%。

ConSFT 处理监督微调中的遗忘问题。它通过停止梯度的置信度权重降低高损失转移的权重，减少模型处理不佳样本上的大幅参数更新。在使用 π0 的 LIBERO 上，它将目标任务成功率保持在 0.90，并将平均先前任务保留率提高到 0.34；标准监督微调为 0.09。

#### Evidence
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO 摘要、方法、LIBERO-Long 结果和跨套件泛化。
- [Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT](../Inbox/2026-05-09--preserving-foundational-capabilities-in-flow-matching-vlas-through-conservative-sft.md): ConSFT 摘要、损失设计，以及跨 VLA 策略的保留结果。

### 测试时动作选择和低成本规划
两篇论文在不重新训练完整机器人策略的情况下降低控制成本。KeyStone 采样多个扩散或流匹配动作块，在动作空间中对它们聚类，并执行最大簇的 medoid。在使用 GR00T N1.6 的 SimplerEnv-WidowX 上，K=4 时成功率从 50.0% 提高到 63.3%。在使用 SmolVLA 的 LIBERO 上，K=16 时成功率从 50.4% 达到 57.2%。

GC-IDM 对世界模型控制采取相关的效率路线。它冻结预训练的 LeWorldModel，并训练一个 1.5M 参数的目标条件逆动力学模型。控制器通过一次前向传播预测下一个动作，不执行 rollout 搜索。在四个基准系列中，它在 8 个设置中的 7 个匹配或超过 Cross-Entropy Method (CEM)，并将每次决策的规划成本降低约 100 到 130 倍。

#### Evidence
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): KeyStone 方法，以及 VLA 和 WAM 基准上的成功率提升。
- [Latent Geometry Beyond Search: Amortizing Planning in World Models](../Inbox/2026-05-09--latent-geometry-beyond-search-amortizing-planning-in-world-models.md): GC-IDM 方法、基准结果和规划加速数据。

### 已发布机器人策略的后门和所有权检查
这一时期的安全研究将 VLA 发布和适配视为攻击面。ATAAT 表明，攻击者可以通过分离良性任务梯度和后门梯度，在 OpenVLA 风格策略中植入视觉触发器。在 5% 投毒率下，它在使用 OpenVLA-7B 的 LIBERO-Spatial 数据投毒中报告 88.8% 的良性成功率和 83.5% 的定向攻击成功率。触发器包括视觉物体，以及打开的抽屉或戴手表的人等语义条件。

GuardVLA 将相关的后门思路用于所有权验证。它在训练期间把固定的 6 位秘密消息嵌入视觉观测，然后在审计时换入触发投影器和分类头。在使用 OpenVLA-OFT 的 LIBERO 上，水印识别置信度在 Spatial、Goal、Object 和 LIBERO-10 上接近 100%，干净模型接近零。报告的良性成功率接近干净基线。

#### Evidence
- [ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models](../Inbox/2026-05-09--ataat-adaptive-threat-aware-adversarial-tuning-framework-against-backdoor-attacks-on-vision-language-action-models.md): ATAAT 威胁模型、梯度分离方法、触发器和攻击结果。
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA 水印方法、审计机制、WIC 结果和良性成功率。

### 智能体硬件启动是机器人瓶颈
Octopus Protocol 针对机器人策略执行动作之前的工作：设备发现、驱动代码、工具暴露和修复。一个编码智能体探测操作系统设备、识别能力、生成带类型的 Model Context Protocol (MCP) 工具、编写 FastMCP 服务器，并部署 HTTP/SSE 端点。

论文报告，一条命令即可在约 10 到 15 分钟内完成硬件接入，最多生成 30 个 MCP 工具。同一份 markdown 规范可在 Windows/WSL、Apple Silicon macOS 和 Raspberry Pi 4 上运行。在带 USB 相机反馈的 SO-ARM101 6-DOF 机械臂上，MCP 客户端通过拍摄图像、移动关节、再用另一张图像检查结果，执行闭环视觉-运动控制。

#### Evidence
- [Octopus Protocol: One-Shot Hardware Discovery and Control for AI Agents via Infrastructure-as-Prompts](../Inbox/2026-05-09--octopus-protocol-one-shot-hardware-discovery-and-control-for-ai-agents-via-infrastructure-as-prompts.md): Octopus Protocol 流程、平台覆盖、硬件控制演示和集成结果。
