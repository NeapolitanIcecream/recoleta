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

# 可部署机器人策略需要在线学习、显式计划和快速感知

## Overview
当天的机器人研究把 Vision-Language-Action (VLA) 策略视为需要在发布后继续改进、公开任务计划并满足控制延迟要求的系统。LWD、IVLR 和 MSACT 给出了最清晰的证据：在线 rollouts、文本-图像 trace 和空间跟踪分别对应真实或模拟环境中的成功率提升。

## Clusters

### Fleet 规模在线强化学习
LWD 在这组工作中给出了最强的真实部署结果。它从一个预训练的 VLA 策略开始，把检查点发送到共享机器人 fleet，收集自主 rollouts 和可选的人类干预，再用离线与在线 replay 的混合数据重新训练。报告的评估使用 16 台双臂机器人，覆盖 8 个操作任务，其中包括功夫茶、鸡尾酒和果汁等 3–5 分钟任务。经过几小时在线交互后，单个通用策略达到 95% 的平均成功率。

关键研究信号在于把失败试验和部分进展用作训练数据。Distributional Implicit Value Learning 对 replay 动作拟合价值分布，然后用自适应的高分位目标做时序差分学习。这个设计用于把稀疏奖励传递到长任务中，不必把每次 rollout 都变成干净的示范。

#### Evidence
- [Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies](../Inbox/2026-05-01--learning-while-deploying-fleet-scale-reinforcement-learning-for-generalist-robot-policies.md): 摘要描述了 LWD 的 fleet 部署循环、分布式 RL 方法、16 台机器人评估、8 个任务和 95% 平均成功率。

### 用于长时程操作的显式文本-图像 trace
IVLR 在执行前让机器人的任务计划可见。每个 trace 阶段把一个文本子目标与一个 RGB 关键帧配对，并从初始观测和指令中一次性生成。控制期间，缓存的 trace 会与实时相机观测结合，用于预测动作。

消融结果表明，trace 在展示之外还有实际作用。在 LIBERO-Long 上，无 trace 的成功率为 37.7%，仅文本 trace 达到 62.0%，仅视觉 trace 达到 68.4%，完整交错 trace 达到 92.4%。该方法还报告了 LIBERO 上 95.5% 的平均成功率，以及 SimplerEnv-WidowX 上 59.4% 的成功率。代价是前置规划时间：在一块 NVIDIA H20 GPU 上生成完整 trace 约需 10 秒，随后缓存执行以 10 Hz 运行。

#### Evidence
- [Thinking in Text and Images: Interleaved Vision--Language Reasoning Traces for Long-Horizon Robot Manipulation](../Inbox/2026-05-01--thinking-in-text-and-images-interleaved-vision-language-reasoning-traces-for-long-horizon-robot-manipulation.md): 摘要给出了 IVLR 的 trace 设计、训练方案、LIBERO 和 SimplerEnv 结果、消融结果以及规划延迟。

### 用于真实操作的低延迟空间注意力
同一作者组的两篇论文把空间跟踪放进紧凑的实时策略中。MSACT 在 ACT 中加入自监督 2D 注意力点跟踪，用于双臂精细操作。在覆盖 4 个任务的 400 次真实 ALOHA 试验中，它报告 53.00% 的成功率，而 ACT 为 23.25%；同时延迟保持在 45.40 ms，几乎与 ACT 的 45.34 ms 相同。

立体移动操作变体使用左右 RGB 图像、共享注意力提取和分层 LSTM 动作预测器。在 4 个真实任务中，每个任务 50 次随机试验，它报告 85.0% 的平均成功率，而 ACT 为 46.0%，Diffusion Policy 为 28.5%。干扰测试也支持这种结构化注意力设计：560 次试验的总体成功率为 76.8%，ACT 为 24.8%。

#### Evidence
- [MSACT: Multistage Spatial Alignment for Stable Low-Latency Fine Manipulation](../Inbox/2026-05-01--msact-multistage-spatial-alignment-for-stable-low-latency-fine-manipulation.md): 摘要报告了 MSACT 的注意力点方法、ALOHA 试验结果、延迟和任务级增益。
- [Stereo Multistage Spatial Attention for Real-Time Mobile Manipulation Under Visual Scale Variation and Disturbances](../Inbox/2026-05-01--stereo-multistage-spatial-attention-for-real-time-mobile-manipulation-under-visual-scale-variation-and-disturbances.md): 摘要报告了立体多阶段空间注意力、真实移动操作结果、消融结果和干扰测试。

### 用于更安全动作规划的结构化先验
VLADriver-RAG 将检索用于自动驾驶，索引语义交通图来替代原始图像。规划器检索相似的交通拓扑和交互历史，然后预测路径与速度路点。在 Bench2Drive 上，它报告 89.12 的 Driving Score 和 70.42% 的 Success Rate，高于同一基准上 ORION 的 77.74 和 54.62%。

可解释性论文为 VLA 策略增加了诊断层。Interventional Significance Score 会遮蔽视觉区域并测量动作变化；Nuisance Mass Ratio 衡量最高显著性中有多少落在与任务无关的区域。在 41 个 AGNOSTOS 任务上，NMR@10 与任务成功率的 Pearson 相关系数为 -0.77，因此较高的干扰归因对应更差的未见任务表现。

Hamiltonian world-model 论文更偏概念。它主张使用潜在相位状态、类能量动力学和以动作为条件的 rollout 来做规划。语料摘要没有报告基准数字，因此这里的价值是设计假设，而非经验证据。

#### Evidence
- [VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving](../Inbox/2026-05-01--vladriver-rag-retrieval-augmented-vision-language-action-models-for-autonomous-driving.md): 摘要给出了 VLADriver-RAG 的语义图检索方法和 Bench2Drive 结果。
- [Embodied Interpretability: Linking Causal Understanding to Generalization in Vision-Language-Action Models](../Inbox/2026-05-01--embodied-interpretability-linking-causal-understanding-to-generalization-in-vision-language-action-models.md): 摘要给出了 ISS 和 NMR 的定义，以及干扰归因与任务成功率之间 -0.77 的相关性。
- [Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling](../Inbox/2026-05-01--physically-native-world-models-a-hamiltonian-perspective-on-generative-world-modeling.md): 摘要描述了 Hamiltonian World Models，并指出缺少基准结果或直接比较。
