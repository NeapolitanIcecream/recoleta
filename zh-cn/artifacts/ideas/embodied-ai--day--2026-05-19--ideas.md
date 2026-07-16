---
kind: ideas
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- Embodied AI
- Vision-language-action models
- Robot manipulation
- World models
- Robot evaluation
- Synthetic data
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-manipulation
- topic/world-models
- topic/robot-evaluation
- topic/synthetic-data
language_code: zh-CN
---

# Robot Policy Stress Testing

## 摘要
机器人团队可以通过加入阶段级操作测试、异步控制的延迟注入运行，以及带动力学约束轨迹的生成式 3DGS 飞行场景，让 VLA 可靠性更容易排查。最有价值的是评估和部署检查，因为报告中的失败都对应到具体阶段、扰动和延迟值。

## Stage-level manipulation evaluation for VLA release checks
机器人团队在评估用于精细操作的 VLA 策略时，应先加入任务图和阶段指标，再把策略用于对部件敏感的任务。MetaFine 说明了原因：按物体算的抓取分数看起来很高，但按部件算的控制会失败。报告中的最佳策略在部件级约束下，Grasp Part 达到 80%，Press Part 达到 68%，Rotate Along 达到 12%；而常规评估会把精细能力高估多达 70%。

一个实用的发布检查是把每个硬件任务拆成语言理解、空间感知和运动行为三个阶段。对于 peg-in-hole 任务，仪表板应分别显示抓取、对齐、插入和轨迹平滑度。MetaFine 在 peg-in-hole 上的结果显示，五个 VLA 的总体成功率都接近于零，但阶段指标仍能分出不同故障点：OpenVLA-OFT 在 47% 的试验中完成抓取，在 19% 中完成对齐；pi_0.5 的抓取率是 39%，对齐率是 0%。

这对模型选择和修复都很有用。MetaFine 报告称，把 pi_0.5 的 SigLIP 编码器换成多尺度交叉注意力编码器，同时冻结 VLM 主干和动作头，能把抓取成功率从 39% 提高到 67%，把对齐率从 0% 提高到 32%。这让评估团队可以直接从失败阶段定位到组件级修复。

### 资料来源
- [Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation](../Inbox/2026-05-19--beyond-binary-success-a-diagnostic-meta-evaluation-framework-for-fine-grained-manipulation.md): MetaFine reports atomic manipulation skills, perturbation tests, stage metrics, headline inflation, and component repair results.
- [Beyond Binary Success: A Diagnostic Meta-Evaluation Framework for Fine-Grained Manipulation](../Inbox/2026-05-19--beyond-binary-success-a-diagnostic-meta-evaluation-framework-for-fine-grained-manipulation.md): The paper describes the diagnostic setup and its use for finding visual encoder bottlenecks in fine-grained manipulation.

## Latency-injection tests for asynchronous VLA control
VLA 部署团队应把延迟作为仿真和硬件预检运行中的受控测试变量。DEFLECT 说明了异步推理会带来一种明确的运行时故障：机器人继续执行较旧的动作块，而模型在计算下一个动作块，所以新动作块可能基于过时的视觉信息和过时的场景状态。

这种故障可以通过延迟扫测来测量。在 Kinetix 上，当推理延迟达到 7 个控制步时，朴素异步滚动的成功率会从 89% 降到 1% 以下。DEFLECT 用离线的新旧观测动作对训练，在 d=0-7 的延迟范围上报告 83.3% 的平均成功率，在训练中未见过的高延迟 d=5-7 上成功率为 73.5%。同一篇论文还报告了真实机器人在 Conveyor-II 上的提升，其中 DEFLECT 的全任务成功率为 90.0%，VLASH 为 83.3%，pi_0.5 为 46.7%。

一个低成本的采用测试是重放现有轨迹，注入 d=0-7 的延迟，记录每个已执行动作块所用视觉观测的时间差，并按延迟区间跟踪成功率。使用 flow-matching VLA 策略的团队随后可以测试一种 DEFLECT 风格的离线后训练步骤，而不改动运行时推理路径。

### 资料来源
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): DEFLECT defines the asynchronous inference failure, the fresh-versus-stale offline training method, and delay-sweep results.
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): The abstract states the async rollout collapse and frames DEFLECT as a drop-in offline refinement for existing async VLA stacks.
- [DEFLECT: Delay-Robust Execution via Flow-matching Likelihood-Estimated Counterfactual Tuning for VLA Policies](../Inbox/2026-05-19--deflect-delay-robust-execution-via-flow-matching-likelihood-estimated-counterfactual-tuning-for-vla-policies.md): The paper gives the real-world stale-observation mechanism, including a conveyor example where execution lags behind the conditioned observation.

## Generated 3DGS scene pipeline for UAV vision-language navigation data
做空中视觉语言导航模型的团队，可以在投入大规模真实飞行采集之前先测试生成数据管线。FlyMirage 描述了一个具体流程：用 LLM 设计场景，生成 3D Gaussian Splatting 环境，渲染 RGB 和深度视图，运行开放词汇目标检测生成 3D 框，选择安全导航目标，再用 EGO-Planner 规划动力学可行的 UAV 轨迹。

报告中的规模已经足够做试点数据集。FlyMirage 包含 500 个生成的 3DGS 场景和约 50,000 条导航轨迹，动作空间为 6-DoF，并考虑动力学约束。论文报告了超过 5,000 个独特物体标签，典型场景中有 60 到 100 个物体实例，单个场景成本约 2 美元，渲染在 NVIDIA RTX 4070 上完成。

一个有用的初步检查是：在目标领域生成 20 到 50 个场景，距离筛选后检查物体框质量，并用论文中相同的安全和行进距离约束运行规划器。如果模型在生成场景上训练效果变好，但在小规模真实飞行验证集上仍然失败，问题更可能出在视觉真实性、标注质量或轨迹动力学，而不是单纯的数据集规模。

### 资料来源
- [FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model](../Inbox/2026-05-19--flymirage-a-fully-automated-generation-pipeline-for-diverse-and-scalable-uav-flight-data-via-generative-world-model.md): FlyMirage gives the automated scene-generation, annotation, target-selection, planning, filtering, scale, and cost details.
- [FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model](../Inbox/2026-05-19--flymirage-a-fully-automated-generation-pipeline-for-diverse-and-scalable-uav-flight-data-via-generative-world-model.md): The abstract describes the full aerial VLN generation pipeline with LLM scene design, 3DGS scenes, semantic acquisition, and feasible UAV trajectories.
