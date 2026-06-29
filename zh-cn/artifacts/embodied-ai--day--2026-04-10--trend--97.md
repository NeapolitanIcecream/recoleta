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

# 机器人论文要求经过验证的落地对齐和可执行数据

## Overview
4 月 10 日是机器人主题的一天，标准很清楚：系统需要验证自己正在作用的对象，数据集需要产出真正能回放的动作。ProGAL-VLA、RoboLab 和 VAG 定下了基调。最强的论文要么直接暴露脆弱的落地对齐，要么围绕规划、合成和评测建立更紧的闭环，让失败在部署前就显现出来。

## Clusters

### Explicit grounding gets treated as a control primitive
落地对齐是最清楚的技术主题。ProGAL-VLA 在语言和控制之间加了一个明确的验证步骤：它先把指令转成符号子目标，再把这个子目标和三维场景实体匹配，最后才把经过验证的目标嵌入传给动作策略。结果很具体。在 LIBERO-Plus 鲁棒性上，它的总分是 85.5，超过 OpenVLA-OFT+ 的 79.6；机器人扰动下的表现也从 30.3 提高到 71.5。论文还把歧义当作一等信号处理，歧义检测的 AUROC 为 0.81，澄清行为从 0.09 提高到 0.81。RoboLab 进一步说明了这件事的重要性。它的留出仿真基准显示，当前通用策略在大多数未见任务上仍会失败，π0.5 的总体成功率只有 23.3%，在语义视觉落地上只有 21.5%。

#### Evidence
- [ProGAL-VLA: Grounded Alignment through Prospective Reasoning in Vision-Language-Action Models](../Inbox/2026-04-10--progal-vla-grounded-alignment-through-prospective-reasoning-in-vision-language-action-models.md): Summary and results for explicit grounding, robustness, and ambiguity metrics.
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md): Benchmark results showing weak held-out generalization and grounding-related failure rates.

### Synthetic robot data is judged by replayability, not just visual quality
合成数据工作正更接近可执行监督。VAG 把视频和动作一起生成，不分阶段，所以合成 rollout 可以直接训练策略。它在 LIBERO 上的动作生成成功率是 79%，并且用合成预训练把下游 VLA 的成功率从 35% 提高到 55%。V-CAGE 处理的是另一个瓶颈：长时程合成轨迹是否真的能在物理上使用、在视觉上正确。它先建场景，再运行操作计划，用视觉检查拒绝失败子任务，还把数据压缩到足以规模化存储。在结果里，经过合成数据微调的 π0.5 在四个任务上的表现分别达到 54%、54%、100% 和 25%，从 0% 的 zero-shot 起点开始；在 ALOHA-AgileX 的 Sim2Real 上，只有 10 个真实示范时成功率是 20%，加入 250 条模拟轨迹后升到 55%。

#### Evidence
- [VAG: Dual-Stream Video-Action Generation for Embodied Data Synthesis](../Inbox/2026-04-10--vag-dual-stream-video-action-generation-for-embodied-data-synthesis.md): Joint video-action generation results and downstream policy gains.
- [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](../Inbox/2026-04-10--v-cage-vision-closed-loop-agentic-generation-engine-for-robotic-manipulation.md): Closed-loop synthetic data pipeline, task results, and Sim2Real gain.

### Benchmarks are getting harsher and more diagnostic
随着模型设计推进，评测压力也在增加。RoboLab 构建了 120 个留出任务，并记录失败事件、运动质量和措辞敏感性，暴露出标准域内基准容易漏掉的大缺口。只改一句指令，就能把同一场景里的 π0.5 从 80% 翻到 0%；在一个打包测试里，目标物体从 1 个增加到 3 个，成功率从 70% 降到 20%。另一个灵巧操作基准 POMDAR 对机器人手也给出类似结论：这个领域还没有统一的性能定义，所以论文提出了 18 个任务，覆盖抓取和手内操作，并配有人类和机器人对照实验。共同重点是测出策略或本体在哪儿失效，而不只是看它能不能通过一个狭窄演示。

#### Evidence
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md): Held-out benchmark design and concrete failure sensitivity numbers.
- [2D or 3D: Who Governs Salience in VLA Models? -- Tri-Stage Token Pruning Framework with Modality Salience Awareness](../Inbox/2026-04-10--2d-or-3d-who-governs-salience-in-vla-models-tri-stage-token-pruning-framework-with-modality-salience-awareness.md): Dexterity benchmark scope and motivation for standardized performance-based evaluation.
