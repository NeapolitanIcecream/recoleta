---
kind: trend
trend_doc_id: 255
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
topics:
- robot learning
- vision-language-action models
- reinforcement learning
- long-horizon manipulation
- spatial attention
- autonomous driving
- interpretability
- world models
run_id: materialize-outputs
aliases:
- recoleta-trend-255
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/reinforcement-learning
- topic/long-horizon-manipulation
- topic/spatial-attention
- topic/autonomous-driving
- topic/interpretability
- topic/world-models
language_code: zh-CN
---

# 可部署的机器人策略需要在线学习、明确计划和快速感知

## Overview
当天的机器人工作把 Vision-Language-Action (VLA) 策略看作必须在发布后继续改进、公开任务计划并满足控制延迟要求的系统。LWD、IVLR 和 MSACT 提供了最清楚的证据，它们把真实或仿真的成功提升和在线 rollout、文本图像 trace、空间跟踪联系在一起。

## Clusters

### Fleet-scale online reinforcement learning
LWD 在这组结果里给出了最强的真实部署表现。它先从一个预训练的 VLA 策略出发，把检查点发送到共享车队，收集自主 rollout 和可选的人类介入，再用离线与在线回放混合数据重新训练。报告中的评估用了 16 台双臂机器人，覆盖 8 个操作任务，包括 Gongfu tea、cocktails 和 fruit juice 这类需要 3–5 分钟的任务。一个通用策略在几小时在线交互后达到 95% 的平均成功率。

关键的研究信号是把失败试验和部分进展当作训练数据。Distributional Implicit Value Learning 先在回放动作上拟合一个价值分布，再把自适应的高分位目标用于时序差分学习。这个设计的目标是在长任务中传播稀疏奖励，同时不要求每次 rollout 都是完整示范。

#### Evidence
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): Summary describes LWD’s fleet deployment loop, distributional RL method, 16-robot evaluation, 8 tasks, and 95% average success.

### Explicit text-image traces for long-horizon manipulation
IVLR 让机器人的任务计划在执行前可见。每个 trace 阶段都把一个文本子目标和一个 RGB keyframe 配对，这些内容只根据初始观测和指令生成一次。控制时，缓存的 trace 会和实时相机观测结合来预测动作。

消融结果说明，这个 trace 不只是为了展示。 在 LIBERO-Long 上，没有 trace 的成功率是 37.7%，只用文本 trace 是 62.0%，只用视觉 trace 是 68.4%，完整的交错 trace 是 92.4%。方法还报告了在 LIBERO 上 95.5% 的平均成功率，在 SimplerEnv-WidowX 上是 59.4%。代价是前置规划时间：完整 trace 生成大约需要 10 秒、在一块 NVIDIA H20 GPU 上完成，然后缓存执行以 10 Hz 运行。

#### Evidence
- [Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation](../Inbox/2026-05-01--thinking-in-text-and-images-interleaved-vision-language-reasoning-traces-for-long-horizon-robot-manipulation.md): Summary gives IVLR’s trace design, training recipe, LIBERO and SimplerEnv results, ablations, and planning latency.

### Low-latency spatial attention for real manipulation
同一作者组的两篇论文把空间跟踪放进了紧凑的实时策略里。MSACT 为 ACT 加上自监督的 2D attention-point 跟踪，用于双臂精细操作。在 400 次真实 ALOHA 试验、覆盖 4 个任务的设置下，它报告 53.00% 的成功率，而 ACT 是 23.25%，同时把延迟保持在 45.40 ms，几乎和 ACT 的 45.34 ms 一样。

那个双目移动操作版本使用左右 RGB 图像、共享注意力提取和分层 LSTM 动作预测器。在 4 个真实任务上、每个任务 50 次随机试验，它报告 85.0% 的平均成功率，而 ACT 是 46.0%，Diffusion Policy 是 28.5%。扰动测试也支持这种结构化注意力设计：在 560 次试验中总体成功率为 76.8%，而 ACT 是 24.8%。

#### Evidence
- [MSACT: Multistage Spatial Alignment for Stable Low-Latency Fine Manipulation](../Inbox/2026-05-01--msact-multistage-spatial-alignment-for-stable-low-latency-fine-manipulation.md): Summary reports MSACT’s attention-point method, ALOHA trial results, latency, and task-level gains.
- [Stereo Multistage Spatial Attention for Real-Time Mobile Manipulation Under Visual Scale Variation and Disturbances](../Inbox/2026-05-01--stereo-multistage-spatial-attention-for-real-time-mobile-manipulation-under-visual-scale-variation-and-disturbances.md): Summary reports stereo multistage spatial attention, real-world mobile manipulation results, ablations, and disturbance tests.

### Structured priors for safer action planning
VLADriver-RAG 用检索处理自动驾驶，它索引的是语义交通图，而不是原始图像。规划器先检索相似的交通拓扑和交互历史，再预测路径和速度 waypoint。在 Bench2Drive 上，它报告 89.12 的 Driving Score 和 70.42% 的 Success Rate，高于同一基准上 ORION 的 77.74 和 54.62%。

那篇可解释性论文给 VLA 策略加了一层诊断。Interventional Significance Score 会遮罩视觉区域并测量动作变化；Nuisance Mass Ratio 用来衡量最高显著性有多少落在与任务无关的区域。 在 41 个 AGNOSTOS 任务上，NMR@10 和任务成功率的 Pearson 相关系数是 -0.77，这说明把注意力放在无关内容上时，未见任务上的表现会更差。

Hamiltonian world-model 论文更偏概念。它主张用潜在相位状态、类能量动力学和动作条件 rollout 来做规划。语料摘要没有给出基准数字，所以这里更像一个设计假设，而不是实证结果。

#### Evidence
- [VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving](../Inbox/2026-05-01--vladriver-rag-retrieval-augmented-vision-language-action-models-for-autonomous-driving.md): Summary gives VLADriver-RAG’s semantic graph retrieval method and Bench2Drive results.
- [Embodied Interpretability: Linking Causal Understanding to Generalization in Vision-Language-Action Models](../Inbox/2026-05-01--embodied-interpretability-linking-causal-understanding-to-generalization-in-vision-language-action-models.md): Summary gives ISS and NMR definitions plus the -0.77 correlation between nuisance attribution and task success.
- [Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling](../Inbox/2026-05-01--physically-native-world-models-a-hamiltonian-perspective-on-generative-world-modeling.md): Summary describes Hamiltonian World Models and notes the lack of benchmark results or direct comparisons.
