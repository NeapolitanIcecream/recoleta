---
kind: trend
trend_doc_id: 901
granularity: day
period_start: '2026-07-16T00:00:00'
period_end: '2026-07-17T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- real-time control
- robustness evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-901
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/real-time-control
- topic/robustness-evaluation
language_code: zh-CN
---

# 更长的机器人记忆与更快的预测成为实用的控制机制

## 概览
近期的每日证据将预测性监督与部署效率视为并行问题。当前论文将两者联系得更紧密：只有在控制运行时成本的前提下，更长的历史、预期运动和模拟结果才能改善控制。真实机器人和基准测试中的结果颇具潜力，但大多数结果仍局限于单独的任务套件和内部报告的评估。

## 研究发现

### 长上下文与面向未来的控制
RoboTTT 将最多 8K 个视觉运动时间步压缩为快速权重，使延迟在历史长度增加时保持不变。在三个真实机器人装配任务上，其平均完成率达到 79%，而单步基线为 42%。FoMoVLA 采取互补路径：它将紧凑的未来状态令牌与稀疏点轨迹一同训练，并在推理时移除大部分辅助模块。在 LIBERO 上，其平均成功率达到 98.8%，中位额外延迟为 9.4 ms。这些研究共同表明，时间信息可以通过紧凑的内部状态投入实际控制，而不必依赖不断增长的观测缓冲区。

#### 资料来源
- [RoboTTT: Context Scaling for Robot Policies](../Inbox/2026-07-16--robottt-context-scaling-for-robot-policies.md): 描述了 8K 时间步上下文、延迟不随上下文长度变化，以及测试时快速权重更新。
- [FoMoVLA: Bridging Visual Foresight and Motion Guidance for Vision-Language-Action Models](../Inbox/2026-07-16--fomovla-bridging-visual-foresight-and-motion-guidance-for-vision-language-action-models.md): 定义了联合未来特征预测和稀疏点跟踪，用于动作引导。

### 不阻塞控制的预测
DriftWorld 通过一次前向传播生成动作条件下的未来，速度超过每秒 30 帧；在五个基准测试中，相比扩散基线平均提速 17 倍。Reflex 同样避免了在流匹配视觉-语言-动作（VLA）策略中重复计算。其分区缓存和异步流水线将 LIBERO 上 Pi0.5 的推理时间从 135.2 ms 降至 52.4 ms，并支持稳定的 50 Hz 流式运行。两者共同说明的范围小于一般意义上的实时自主：可以重新组织迭代式生成组件，使规划和执行不再等待完整重算。

#### 资料来源
- [DriftWorld: Fast World Modeling through Drifting](../Inbox/2026-07-16--driftworld-fast-world-modeling-through-drifting.md): 报告了单次前向传播生成未来、速度超过 30 fps，以及在五个基准测试中平均提速 17 倍。
- [Reflex: Real-Time VLA Control through Streaming Inference](../Inbox/2026-07-16--reflex-real-time-vla-control-through-streaming-inference.md): 解释了与时间步无关的分区缓存和异步推理。

### 鲁棒性测试揭示隐藏的权衡
总体成功率可能掩盖脆弱行为。FLARE 使用优化的物理光照，使三个 LIBERO 测试套件上的基线成功率降至零。它还发现，广泛的颜色增强可能通过教会策略忽略颜色而显得稳健；其保留色度的防御方法在一个真实的颜色相关任务上，将正常光照下的成功率恢复到 97.5%，受攻击条件下的成功率恢复到 92.5%。另一套主动测试框架对位姿、桌面高度和视角等结构化变化进行采样。在 2,331 次真实世界评估中，与随机测试相比，它通常将刻画性能所需的试验次数减少了 20–40%。两篇论文都主张测试失败区域和保留的能力，而不只是平均任务完成率。

#### 资料来源
- [Lights, Camera, Malfunction: When Illumination Robustness Leaves VLA Models Blind to Color](../Inbox/2026-07-16--lights-camera-malfunction-when-illumination-robustness-leaves-vla-models-blind-to-color.md): 显示优化聚光灯攻击将基线任务成功率降至零，并诊断出朴素增强导致的颜色失盲。
- [Active Real-World Factor-Based Evaluation for Generalist Robot Policies](../Inbox/2026-07-16--active-real-world-factor-based-evaluation-for-generalist-robot-policies.md): 定义了基于结构化任务因素的主动评估，并报告了 2,331 次真实世界评估。

### 预测结果充当训练监督
两项研究利用生成的结果来改进策略，但不将生成器作为部署时的控制器。小米报告称，加入其开放的 380 亿参数 U0 世界模型生成的场景和视频后，π0.5 在陌生操作任务上的成功率从 36.9% 提升至 63.2%。在接触密集型操作中，一个潜在触觉预测器训练中间动作特征以预测未来触觉，随后在推理时移除；真实世界平均成功率达到 74%。两者机制不同，但都将结果建模置于学习流程中。小米的提升来自厂商报告，而触觉结果覆盖五个任务和两个 VLA 骨干网络。

#### 资料来源
- [Xiaomi Opens a 38B World Model Built to Generate Robot Data](../Inbox/2026-07-16--xiaomi-opens-a-38b-world-model-built-to-generate-robot-data.md): 报告了使用 U0 生成的训练数据，以及成功率从 36.9% 提升至 63.2%；同时指出该评估由小米自行开展。
- [Representation-Aligned Tactile Grounding for Contact-Rich Robotic Manipulation](../Inbox/2026-07-16--representation-aligned-tactile-grounding-for-contact-rich-robotic-manipulation.md): 确定将中间动作专家特征作为未来触觉监督的目标。
