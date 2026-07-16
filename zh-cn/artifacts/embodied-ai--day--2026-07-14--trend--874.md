---
kind: trend
trend_doc_id: 874
granularity: day
period_start: '2026-07-14T00:00:00'
period_end: '2026-07-15T00:00:00'
topics:
- "\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "\u673A\u5668\u4EBA\u5B66\u4E60"
- "\u9AD8\u6548\u63A8\u7406"
- "\u5408\u6210\u6570\u636E"
- "\u52A8\u4F5C\u8868\u5F81"
run_id: materialize-outputs
aliases:
- recoleta-trend-874
tags:
- recoleta/trend
- "topic/\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "topic/\u673A\u5668\u4EBA\u5B66\u4E60"
- "topic/\u9AD8\u6548\u63A8\u7406"
- "topic/\u5408\u6210\u6570\u636E"
- "topic/\u52A8\u4F5C\u8868\u5F81"
language_code: zh-CN
---

# VLA 部署工作同时针对延迟、连续性和稀缺交互数据

## 概览
当天的证据将近期对高效机器人学习的关注延伸到了部署环节。视觉-语言-动作（VLA）系统正在围绕推理、控制连续性和数据采集进行优化，而不只是依靠模型规模扩展。现有结果涵盖仿真和有限的真实机器人测试，因此其在广泛实际环境中的可靠性仍未得到证明。

## 研究发现

### 实时 VLA 控制
三篇论文分别针对控制延迟的不同来源。去除时间冗余的方法缓存稳定的视觉令牌，并将流采样压缩为两步；在 LIBERO 上达到 8.2 FPS，平均成功率为 93.8%，而原始策略为 94.4%。Jetson-PI 则预测未来表征，以纠正异步推理中的过时观测；系统优化将 Jetson Orin 的控制频率从 0.70 Hz 提升至 6.06 Hz。ChunkFlow 通过边界感知训练和重叠融合补充原始速度，在 LIBERO-Long 上报告 93.4% 的成功率和 4.43 ms 的推理延迟。综合来看，实用的 VLA 控制取决于视觉感知复用、动作生成、硬件调度和动作块执行之间的协同。

#### 资料来源
- [Reducing Temporal Redundancy for Efficient Vision-Language-Action Inference](../Inbox/2026-07-14--reducing-temporal-redundancy-for-efficient-vision-language-action-inference.md): 报告了两步采样、8.2 FPS，以及 LIBERO 上的成功率和延迟对比。
- [Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference](../Inbox/2026-07-14--jetson-pi-towards-onboard-real-time-robot-control-via-foresight-aligned-asynchronous-inference.md): 报告了面向未来对齐的异步推理方法和 Jetson Orin 的频率消融结果。
- [ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning](../Inbox/2026-07-14--chunkflow-towards-continuity-consistent-chunked-policy-learning.md): 报告了边界感知的动作块执行、LIBERO-Long 成功率、连续性指标和延迟。

### 每次交互带来更多学习价值
数据稀缺这一信号仍在延续，但现在出现了主动制造多样性的机制，而不只是增加示范数量。WANDA 将一次 RGBD 示范转换为重建和生成的 3D 场景中的多条轨迹；在仿真中达到 75.6% 的平均成功率，接近使用约 40–60 次示范训练的基线。ExToken 利用行为聚类使强化学习 rollout 多样化：256 次 rollout 达到 93.4% 的成功率，而匹配基线为 90.3%，且性能接近其 512 次 rollout 的设置。FlowWAM 提供了另一条路径：从无动作标注视频中提取的光流，将 RoboTwin Clean 的成功率从 82.40% 提升至 92.94%。

#### 资料来源
- [Worlds in One Demo: A Synthetic Data Engine for Learning Open-World Mobile Manipulation](../Inbox/2026-07-14--worlds-in-one-demo-a-synthetic-data-engine-for-learning-open-world-mobile-manipulation.md): 详细说明了从一次示范生成数据的方法，以及相对于依赖大量示范训练的方案所取得的 75.6% 仿真结果。
- [ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning](../Inbox/2026-07-14--extoken-structured-exploration-for-efficient-vision-language-action-reinforcement-fine-tuning.md): 展示了结构化行为探索如何达到更大 rollout 预算下的性能。
- [FlowWAM: Optical Flow as a Unified Action Representation for World Action Models](../Inbox/2026-07-14--flowwam-optical-flow-as-a-unified-action-representation-for-world-action-models.md): 量化了通过光流利用无动作标注视频进行预训练所带来的收益。

### 与控制对齐的场景和运动表征
明确的表征设计仍然是效率提升的重要补充。VistaVLA 将语义特征建立在 3D Gaussian 基元上，再将约 100,000 个基元压缩为供策略使用的 64 个令牌。该方法在七项真实世界任务中的平均成功率提升了 22.8 个百分点，但对大幅位置变化的处理仍然困难。FlowWAM 将动作表示为光流视频，使一个预训练视频架构能够同时支持控制和未来预测；在 RoboTwin Clean 和 Random 上分别达到 92.94% 和 92.14% 的成功率。共同结果并不是表明研究普遍转向 3D 或视频表征，而是表明：当表征的坐标系和时间结构与控制问题相匹配时，表征设计才会带来帮助。

#### 资料来源
- [VistaVLA: Geometry- and Semantic-Aware 3D Gaussian-Grounded VLA for Robotic Manipulation](../Inbox/2026-07-14--vistavla-geometry-and-semantic-aware-3d-gaussian-grounded-vla-for-robotic-manipulation.md): 报告了 99% 的令牌压缩、真实世界收益，以及在大幅位置变化下有限的鲁棒性。
- [FlowWAM: Optical Flow as a Unified Action Representation for World Action Models](../Inbox/2026-07-14--flowwam-optical-flow-as-a-unified-action-representation-for-world-action-models.md): 将光流用作原生视频动作表征，并报告了策略和世界模型基准结果。
