---
kind: trend
trend_doc_id: 198
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- robotics
- vision-language-action
- manipulation
- tactile sensing
- safety
run_id: materialize-outputs
aliases:
- recoleta-trend-198
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/manipulation
- topic/tactile-sensing
- topic/safety
language_code: zh-CN
---

# 接触时刻控制与 VLA 安全定义了这一天的机器人论文

## Overview
这一天最强的是必须在接触时刻起作用的具身控制。两篇论文都在改进操作执行：Move-Then-Operate 把接近阶段和接触阶段分开，Tube Diffusion Policy 在动作时间范围内加入逐步的视觉-触觉修正。第三篇论文用一篇关于视觉-语言-动作，也就是 VLA 系统的安全风险和防御的综述，把视角扩大到部署问题，说明部署已经成为核心研究议题的一部分。

## Clusters

### Behavioral phasing for precise manipulation
Move-Then-Operate 认为，当策略把接近动作和接触操作分开处理时，高精度操作会更好。它的双专家设计用一个专家负责移动、一个专家负责操作，由路由器按动作块选择阶段。在 8 个 RoboTwin2 任务上、每个任务 50 个示范的设置下，它报告的平均成功率是 68.88%，高于 pi_0 的 44.75%、RDT 的 35.63% 和 ACT 的 31.63%。在 Click Bell 这类接触密集任务上，提升很大，pi_0 为 44%，它达到 99%；在 Place Cans Plasticbox 上，pi_0 为 34%，它达到 79%。论文还声称，模型在少 40% 的训练步数下就达到峰值表现。

#### Evidence
- [Move-Then-Operate: Behavioral Phasing for Human-Like Robotic Manipulation](../Inbox/2026-04-26--move-then-operate-behavioral-phasing-for-human-like-robotic-manipulation.md): Summary and benchmark results for phased manipulation policy.

### Reactive visual-tactile control
Tube Diffusion Policy 关注不确定条件下的接触密集控制。它保留扩散模型来在动作块开始时生成动作，再加入一个学习到的流式反馈模块，让机器人能根据新的视觉和触觉输入在每一步修正动作。论文报告，在 Push-T 和另外三个视觉-触觉任务上，它都比之前的模仿学习基线更好；另外还有两个真实世界实验，显示它在受到扰动时反应更快。摘要没有给出精确成功率，所以这里最确定的结论是架构层面的：块内的实时修正正在被当作触觉操作的核心控制要求。

#### Evidence
- [Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation](../Inbox/2026-04-26--tube-diffusion-policy-reactive-visual-tactile-policy-learning-for-contact-rich-manipulation.md): Summary of action-tube method and reported empirical scope.

### VLA safety taxonomy and evaluation scope
安全正在被当作视觉-语言-动作模型的一等研究问题，而不是附在模型规模后面的补充项。VLA 安全综述给出了一张具体的威胁图，覆盖训练时和推理时攻击，也覆盖训练时和运行时防御。它讨论了数据投毒、后门、对抗补丁、跨模态扰动、越狱和冻结攻击等威胁，并把这些问题和六个领域中的评估与部署问题联系起来。这篇论文是综述，不是新的基准报告，但它清楚表明，这个领域现在需要共享评估和运行时防护。

#### Evidence
- [Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms](../Inbox/2026-04-26--vision-language-action-safety-threats-challenges-evaluations-and-mechanisms.md): Survey summary with taxonomy, threat classes, and deployment scope.
