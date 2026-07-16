---
kind: trend
trend_doc_id: 604
granularity: day
period_start: '2026-06-10T00:00:00'
period_end: '2026-06-11T00:00:00'
topics:
- vision-language-action
- robot manipulation
- contact-rich control
- world models
- multi-robot collaboration
- dexterous manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-604
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/contact-rich-control
- topic/world-models
- topic/multi-robot-collaboration
- topic/dexterous-manipulation
language_code: zh-CN
---

# Robot VLA gains are tied to contact, timing, and action priors

## 概览
这一时期的视觉-语言-动作（VLA）机器人论文重点在让策略在物理约束下正常工作。DAM-VLA、World Pilot 和 CHORUS 显示了主要方向：更快的传感器回路、面向动作的引导，以及能在真实机器人环境中部署的控制。

## 研究发现

### Contact-aware control loops
DAM-VLA 将机器人输入视为不同时钟上的信号。语言只编码一次，视觉稀疏更新，力觉和本体感觉按控制频率更新。动作头在每一步读取缓冲的潜变量，因此控制器在较慢输入等待新数据时还能持续输出动作。在 7 个真实 Franka 操作任务上，它报告的平均成功率为 95.2%，而最强的同步基线为 40.95%。

TacCoRL 把触觉 token 加入预训练的 VLA 策略，并在真实部署前先在仿真中训练接触修正。它的接触门控会在触觉读数像背景噪声时抑制这些输入，强化学习则在与真实分布对齐的模拟器中进行，并用真实轨迹上的监督锚点约束。跨 4 个真实的双臂接触密集任务，这个视觉-触觉策略的平均成功率达到 72.5%，而仅视觉策略在强化学习后为 50.0%。

#### 资料来源
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): DAM-VLA summary, asynchronous modality buffers, 100 Hz control, and real-task success rates.
- [TacCoRL: Integrating Tactile Feedback into VLA via Simulation](../Inbox/2026-06-10--taccorl-integrating-tactile-feedback-into-vla-via-simulation.md): TacCoRL summary, tactile gating, sim-real training method, and real-world success rates.

### Action and world priors for generalization
World Pilot 在 VLA 策略中加入一个冻结的 world-action 模型。一路把预测的场景演化潜变量注入感知流，另一路把预期动作轨迹送入动作生成器。在 LIBERO-Plus 的零样本分布外测试中，它报告的总成功率为 84.7%，高于 ABot-M0 的 80.5% 和 Cosmos Policy 的 79.7%。在真实机器人测试中，论文在列出的每个设置上都给出最高成功率。

APT 针对的是另一种失败模式：由机器人数据不均衡导致的指令泛化能力弱。它先在把语言遮蔽掉的视觉-动作对上训练连续动作专家，再加入语言条件。在 LIBERO-PRO 上，加入视觉语言模型微调的 APT 报告平均成功率为 27%，对比 π0.5 的 11% 和 LangForce 的 14%。在 LIBERO-PRO Spatial 上，它在位置和任务指标上都达到 62%，对比 π0.5 的 20% 和 1%。

#### 资料来源
- [World Pilot: Steering Vision-Language-Action Models with World-Action Priors](../Inbox/2026-06-10--world-pilot-steering-vision-language-action-models-with-world-action-priors.md): World Pilot method, LIBERO-Plus results, and real-robot evaluation summary.
- [APT: Action Expert Pretraining Improves Instruction Generalization of Vision-Language-Action Policies](../Inbox/2026-06-10--apt-action-expert-pretraining-improves-instruction-generalization-of-vision-language-action-policies.md): APT two-stage action-expert pretraining and instruction generalization results.

### Test-time language steering with abstention
有一篇论文保持机器人策略冻结，只学习在执行时该传给它什么语言。语言反馈策略会在重规划时提出子任务指令，然后改进头判断何时引导更可能有帮助。一个 conformal prediction 门控会在学到的引导看起来有风险时，让策略回退到原始指令。

摘要里给出的收益很大：在仿真中提升 24.7%，在 Franka 硬件上对已见环境提升 65.0%。论文还在校准假设下给出了对有害引导的假阳性保证。真正有用的是这个拒绝机制，因为同一份摘要也说了，错误的引导提示会降低任务成功率。

#### 资料来源
- [Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering](../Inbox/2026-06-10--learning-what-to-say-to-your-vla-mostly-harmless-vision-language-action-model-steering.md): Language feedback policy, conformal abstention gate, and reported simulation and hardware gains.

### One policy across teams and hands
CHORUS 对异构机器人团队微调同一个预训练 VLA 策略。每个机器人运行自己的副本，只使用本地观测和身份提示。论文报告，与从头训练的去中心化扩散策略相比，平均成功率提升 64 个百分点；在队友扰动的交接测试中，成功 17/20，而分别为每个机器人训练的 VLA 策略为 9/20。

InDex 把预训练 VLA 策略适配到高自由度灵巧手。它保留 VLA 的臂级空间行为，预测一个标量抓取意图，并为手指级动作训练一个扩散头。在每个任务 100 个示范的 robosuite 仿真中，π0.5+InDex 的平均任务成功率为 85.8%，而 π0.5 为 50.3%，Diffusion Policy 为 42.8%。

#### 资料来源
- [CHORUS: Decentralized Multi-Embodiment Collaboration with One VLA Policy](../Inbox/2026-06-10--chorus-decentralized-multi-embodiment-collaboration-with-one-vla-policy.md): CHORUS decentralized multi-robot setup and real-world success comparisons.
- [Bridging the Morphology Gap: Adapting VLA Models to Dexterous Manipulation via Intent-Conditioned Fine-Tuning](../Inbox/2026-06-10--bridging-the-morphology-gap-adapting-vla-models-to-dexterous-manipulation-via-intent-conditioned-fine-tuning.md): InDex intent-conditioned dexterous adaptation method and simulation results.
