---
kind: trend
trend_doc_id: 97
granularity: day
period_start: '2026-04-10T00:00:00'
period_end: '2026-04-11T00:00:00'
topics:
- robotics
- vision-language-action
- grounding
- synthetic-data
- benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-97
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/grounding
- topic/synthetic-data
- topic/benchmarks
language_code: zh-CN
---

# 机器人论文要求经过验证的 grounding 和可执行数据

## Overview
4 月 10 日的机器人论文给出了一个明确标准：系统需要验证自己正在作用的对象，数据集需要产出真正可以回放的动作。ProGAL-VLA、RoboLab 和 VAG 定下了基调。最强的论文要么直接揭示 grounding 的脆弱性，要么在规划、合成和评测周围建立更紧的闭环，让失败在部署前就暴露出来。

## Clusters

### 显式 grounding 被当作控制原语来处理
Grounding 是最清晰的技术主题。ProGAL-VLA 在语言和控制之间加入了一个显式验证步骤：它先把指令转成符号化子目标，再把这个子目标与 3D 场景实体匹配，之后才把经过验证的目标嵌入传给动作策略。效果很具体。在 LIBERO-Plus 鲁棒性测试中，它的总分是 85.5，高于 OpenVLA-OFT+ 的 79.6；在机器人扰动条件下，性能从 30.3 提升到 71.5。同一篇论文还把歧义当作核心信号处理，歧义检测的 AUROC 为 0.81，澄清行为从 0.09 提升到 0.81。RoboLab 进一步说明了这件事的重要性。它的留出式仿真基准显示，当前通用策略在大多数未见任务上仍然失败，π0.5 的总体成功率是 23.3%，在语义视觉 grounding 上只有 21.5%。

#### Evidence
- [ProGAL-VLA: Grounded Alignment through Prospective Reasoning in Vision-Language-Action Models](../Inbox/2026-04-10--progal-vla-grounded-alignment-through-prospective-reasoning-in-vision-language-action-models.md): 显式 grounding、鲁棒性和歧义指标的摘要与结果。
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md): 展示留出泛化较弱和 grounding 相关失败率的基准结果。

### 合成机器人数据的评判标准是可回放性，而不只是视觉质量
合成数据工作正在更接近可执行监督。VAG 同时生成视频和动作，而不是分阶段生成，因此合成 rollout 可以直接用来训练策略。它在 LIBERO 上报告了 79% 的动作生成成功率，并通过合成预训练把下游 VLA 的成功率从 35% 提高到 55%。V-CAGE 处理的是另一个瓶颈：长时程合成轨迹在物理上是否可用、在视觉上是否正确。它构建场景、执行操作计划、用视觉检查剔除失败的子任务，并把数据压缩到足以大规模存储的程度。结果显示，π0.5 在合成数据上微调后，四个任务的成功率从 0% 的零样本起点提升到 54%、54%、100% 和 25%；在 ALOHA-AgileX 上，加入 250 条模拟轨迹后，Sim2Real 表现从仅用 10 个真实示例时的 20% 提升到 55%。

#### Evidence
- [VAG: Dual-Stream Video-Action Generation for Embodied Data Synthesis](../Inbox/2026-04-10--vag-dual-stream-video-action-generation-for-embodied-data-synthesis.md): 联合视频-动作生成结果和下游策略收益。
- [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](../Inbox/2026-04-10--v-cage-vision-closed-loop-agentic-generation-engine-for-robotic-manipulation.md): 闭环合成数据流水线、任务结果和 Sim2Real 提升。

### 基准测试变得更严格，也更能定位问题
随着模型设计推进，评测压力也在上升。RoboLab 构建了 120 个留出任务，并记录失败事件、运动质量和措辞敏感性，暴露出标准域内基准容易漏掉的大缺口。仅仅改变指令表述，就能让同一场景中的 π0.5 从 80% 变成 0%；在一项装箱测试中，目标物体从 1 个增加到 3 个，成功率会从 70% 降到 20%。另一套灵巧操作基准 POMDAR 对机器人手也提出了类似观点：这个领域仍然缺少共享的性能定义，因此论文提出了 18 个任务，覆盖抓取和手内操作，并设置了对齐的人类与机器人试验。共同的重点是用测量找出策略或具身系统会在哪些地方失效，而不只是看它们能否通过一个范围很窄的演示。

#### Evidence
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md): 留出基准设计和具体的失败敏感性数字。
- [2D or 3D: Who Governs Salience in VLA Models? -- Tri-Stage Token Pruning Framework with Modality Salience Awareness](../Inbox/2026-04-10--2d-or-3d-who-governs-salience-in-vla-models-tri-stage-token-pruning-framework-with-modality-salience-awareness.md): 灵巧操作基准的范围，以及推动标准化性能评测的动机。
