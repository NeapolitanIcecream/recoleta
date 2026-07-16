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

# 机器人 VLA 的可靠性正在记忆、动作和发布环节接受检验

## 概览
当天的机器人工作把 Vision-Language-Action（VLA）模型当作可部署的控制系统。ECHO 扩展了长时程记忆，KeyStone 改进了推理时的随机动作选择，ATAAT 则表明视觉后门可以在微调后保留下来。共同的检验标准是：机器人策略在更长任务、新数据、不确定样本和已发布模型风险下，能否保住有用行为。

## 研究发现

### VLA 记忆与技能保留
ECHO 和 ConSFT 关注一个基础部署问题：机器人策略必须记住有用经验，并在任务适配后保留旧技能。ECHO 把成功的子目标片段存进分层双曲记忆，并在控制时检索这些片段。在 LIBERO-Long 上，它的成功率为 93.5%，而原始 π0 为 80.7%；在没有任何 LIBERO-Long 目标记忆的情况下，跨套件泛化达到 89.31%。

ConSFT 处理监督微调中的遗忘问题。它通过 stop-gradient 置信度权重下调高损失迁移样本的权重，减少模型在表现较差样本上的大幅参数更新。在 LIBERO 上配合 π0，它把目标任务成功率保持在 0.90，并把平均旧任务保留率提高到 0.34；标准监督微调只有 0.09。

#### 资料来源
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO summary, method, LIBERO-Long results, and cross-suite generalization.
- [Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT](../Inbox/2026-05-09--preserving-foundational-capabilities-in-flow-matching-vlas-through-conservative-sft.md): ConSFT summary, loss design, and retention results across VLA policies.

### 测试时动作选择与低成本规划
两篇论文都在不重新训练整个机器人策略的情况下降低控制成本。KeyStone 在动作空间里对多个 diffusion 或 flow-matching 动作块采样、聚类，并执行最大簇的 medoid。在使用 GR00T N1.6 的 SimplerEnv-WidowX 上，K=4 时成功率从 50.0% 提升到 63.3%。在使用 SmolVLA 的 LIBERO 上，K=16 时成功率从 50.4% 提升到 57.2%。

GC-IDM 在世界模型控制上采用类似的效率思路。它冻结一个预训练的 LeWorldModel，只训练一个 150 万参数的 goal-conditioned inverse dynamics model。控制器只需一次前向传播就能预测下一个动作，不做 rollout 搜索。在四组基准家族中，它在 8 个设置里的 7 个上达到或超过 Cross-Entropy Method（CEM），并把每次决策的规划成本削减约 100 到 130 倍。

#### 资料来源
- [Geometry Guided Self-Consistency for Physical AI](../Inbox/2026-05-09--geometry-guided-self-consistency-for-physical-ai.md): KeyStone method and success-rate gains across VLA and WAM benchmarks.
- [Latent Geometry Beyond Search: Amortizing Planning in World Models](../Inbox/2026-05-09--latent-geometry-beyond-search-amortizing-planning-in-world-models.md): GC-IDM method, benchmark results, and planning speedup figures.

### 已发布机器人策略的后门与所有权检查
这一时期的安全工作把 VLA 发布和适配看作攻击面。ATAAT 表明，攻击者可以通过分离正常任务梯度和后门梯度，把视觉触发器植入 OpenVLA 风格策略中。在 5% 污染率下，它在用 OpenVLA-7B 的 LIBERO-Spatial 数据投毒中报告了 88.8% 的正常成功率和 83.5% 的定向攻击成功率。触发器包括视觉物体和语义条件，例如抽屉打开或有人戴着手表。

GuardVLA 用了一个相关的后门思路来做所有权验证。它在训练时把固定的 6 位秘密消息嵌入视觉观测，然后在审计时换入触发投影器和分类头。在 LIBERO 上配合 OpenVLA-OFT，水印识别置信度在 Spatial、Goal、Object 和 LIBERO-10 上都接近 100%，而干净模型接近 0。报告的正常成功率与干净基线基本一致。

#### 资料来源
- [ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models](../Inbox/2026-05-09--ataat-adaptive-threat-aware-adversarial-tuning-framework-against-backdoor-attacks-on-vision-language-action-models.md): ATAAT threat model, gradient separation approach, triggers, and attack results.
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA watermarking method, audit mechanism, WIC results, and benign success rates.

### 把代理硬件接入当作机器人瓶颈
Octopus Protocol 处理的是机器人策略开始执行之前的工作：设备发现、驱动代码、工具暴露和修复。一个编码代理会探测操作系统设备，识别能力，生成带类型的 Model Context Protocol（MCP）工具，编写 FastMCP 服务器，并部署 HTTP/SSE 端点。

论文报告了大约 10 到 15 分钟的一键硬件接入流程，最多可生成 30 个 MCP 工具。相同的 markdown 规范可运行在 Windows/WSL、Apple Silicon macOS 和 Raspberry Pi 4 上。在一条带 USB 摄像头反馈的 SO-ARM101 6-DOF 机械臂上，MCP 客户端通过拍照、移动一个关节、再用另一张图检查结果，实现闭环视觉-运动控制。

#### 资料来源
- [Octopus Protocol: One-Shot Hardware Discovery and Control for AI Agents via Infrastructure-as-Prompts](../Inbox/2026-05-09--octopus-protocol-one-shot-hardware-discovery-and-control-for-ai-agents-via-infrastructure-as-prompts.md): Octopus Protocol pipeline, platform coverage, hardware control demo, and integration results.
