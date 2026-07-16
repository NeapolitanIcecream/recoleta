---
kind: trend
trend_doc_id: 471
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
topics:
- vision-language-action
- robot manipulation
- real-robot evaluation
- dexterous control
- spatial reasoning
- inference efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-471
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/real-robot-evaluation
- topic/dexterous-control
- topic/spatial-reasoning
- topic/inference-efficiency
language_code: zh-CN
---

# 机器人 VLA 工作正按控制速度、任务迁移和真实机器人证据来评估

## 概览
当天的研究集中在可部署的机器人控制上。视觉-语言-动作（VLA）模型获得了更大的任务覆盖、更快的推理路径、更丰富的空间落地，以及更多真实机器人检查。Qwen-VLA 的统一化主张最广，BORA 给出了最清楚的灵巧适应结果，PhAIL 则质疑真实机器人成功率该如何衡量。

## 研究发现

### Generalist VLA policies
Qwen-VLA 是规模化和统一化的核心。它使用 Qwen3.5-4B 做视觉-语言理解，并用 DiT 流匹配动作解码器生成连续动作。模型读取机器人描述、图像和指令，然后在操作、导航和轨迹预测中预测动作块或轨迹块。报告结果覆盖 LIBERO、Simpler-WidowX、RoboTwin、R2R、RxR、ALOHA 分布外试验和 DOMINO 动态操作。

VLA-Pro 走的是模块化迁移路线。它把任务特定的 LoRA 适配器和结构化过程状态一起存储，在推理时检索相关记忆，并为当前动作块融合权重。在报告的设定里，提升幅度很大：π0.5 在 6 个保留的 UR7e 任务上的真实世界成功率从 5.8% 升到 65.0%，RoboTwin 结果在 X-VLA、RDT 和 π0.5 骨干上都有提升。

#### 资料来源
- [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](../Inbox/2026-05-28--qwen-vla-unifying-vision-language-action-modeling-across-tasks-environments-and-robot-embodiments.md): Qwen-VLA summary, architecture, training setup, and benchmark results.
- [VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models](../Inbox/2026-05-28--vla-pro-cross-task-procedural-memory-transfer-for-vision-language-action-models.md): VLA-Pro procedural memory method and transfer results.

### Real-world adaptation and human intent
BORA 关注灵巧手，接触误差会很快累积。它先离线训练一个动作条件 critic，然后在部署时冻结基础 VLA，并在有人类干预下学习一个小的残差 actor。在 5 个 Franka 机械臂加 12 自由度手部任务上，BORA-Full 的平均成功率达到 86.0%，而一致性策略基础模型只有 53.0%。在未见物体上，它达到 70.0%，同一基础模型为 27.0%。

Gaze2Act 把人眼注视当作目标选择和部件级交互的控制信号。它把第一人称视角的注视映射到机器人相机视图，在机器人观测上加入 mask 和 heatmap 提示，并在 GROOT N1.5 扩散动作头上增加一个注视分支。在 Unitree G1 类人机器人上，它在 15 个主要真实机器人任务中报告了 83.5% 的任务成功率，结果强于仅语言基线和语言约束空间基线。

#### 资料来源
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): BORA offline-to-online residual adaptation method and real-world dexterous results.
- [Gaze2Act: Gaze-Conditioned Vision-Language-Action Policies for Interactive Robot Manipulation](../Inbox/2026-05-28--gaze2act-gaze-conditioned-vision-language-action-policies-for-interactive-robot-manipulation.md): Gaze2Act gaze-conditioned policy design and Unitree G1 evaluation.

### Perception and inference efficiency
VisualThink-VLA 为物体框、边缘、运动和关系加入稀疏视觉证据 token。路由器在每个决策步骤选择证据通道，而 VLA 主干保持冻结。在 BridgeData V2 上，它报告每步 0.367 秒、89.49% 的成功率；ECoT 的结果是 85.09% 和 8.377 秒。

3DVLA 为预训练 VLA 策略加入 3D 空间记忆、以物体为中心的实例 token 和遮挡补全。它在 LIBERO-Plus 上的提升较小，但在 RoboTwin 2.0 上更广，那里 π0+3DVLA 把 Easy 成功率从 46.4% 提高到 54.5%，把 Hard 成功率从 16.3% 提高到 23.2%。

ElegantVLA 通过学习何时重新计算视觉编码器、语言模型和动作头来降低计算量。在基于 GR00T 的真实世界测试中，它报告计算量减少 2.18×，控制频率从 13.8 Hz 升到 26.3 Hz，平均成功率从 61.67% 升到 65.00%。

#### 资料来源
- [VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies](../Inbox/2026-05-28--visualthink-vla-visual-intermediate-reasoning-for-effective-and-low-latency-vision-language-action-policies.md): VisualThink-VLA visual evidence routing and latency-success results.
- [3DVLA: Enhancing Vision-Language-Action Models via 3D Spatial and Instance Understanding](../Inbox/2026-05-28--3dvla-enhancing-vision-language-action-models-via-3d-spatial-and-instance-understanding.md): 3DVLA 3D spatial and instance reasoning results on LIBERO-Plus and RoboTwin 2.0.
- [ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models](../Inbox/2026-05-28--elegantvla-learning-when-to-think-for-efficient-vision-language-action-models.md): ElegantVLA learned compute scheduling and real-world speed results.

### Evaluation, diagnosis, and confidence
这些评估论文针对的是单一成功率看不到的失败模式。PhAIL 在 Franka FR3 上测量成功所需时间分布，并把评分锚定到同一装置上的人工遥操作。在它的基准中，按 RMST 比率算，评测表现最好的 VLA 比人工参考慢大约 7 倍，而且没有任何推理模型在任何物体上超过 19% 的 Human-Relative Throughput。

VLA-Trace 检查 VLA 策略在动作解码时如何使用图像和文本。在 LIBERO-10 上，当生成时去掉图像访问，π0.5 的成功率从 93.5% 降到 0.0%；去掉文本访问时，成功率还剩 39.0%。OpenVLA 呈现出不同的依赖模式，在报告的 LIBERO 设定里，去掉文本会把成功率降到 0.0%。

VLAConf 用冻结的 VLA 特征和只做成功预测的 confidence head 增加了校准后的任务成功置信度。它面向在线失败预判，在 OpenVLA-OFT 上的推理成本明显低于 ConfidenceVLA：平均查询时间 64.9 ms，对比 712.9 ms。

#### 资料来源
- [PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology](../Inbox/2026-05-28--phail-a-real-robot-vla-benchmark-and-distributional-methodology.md): PhAIL real-robot benchmark, time-to-success evaluation, and throughput findings.
- [VLA-Trace: Diagnosing Vision-Language-Action Models through Representation and Behavior Tracing](../Inbox/2026-05-28--vla-trace-diagnosing-vision-language-action-models-through-representation-and-behavior-tracing.md): VLA-Trace modality ablation and representation-behavior diagnostics.
- [VLAConf: Calibrated Task-Success Confidence for Vision-Language-Action Models](../Inbox/2026-05-28--vlaconf-calibrated-task-success-confidence-for-vision-language-action-models.md): VLAConf confidence estimation method and latency/calibration results.
