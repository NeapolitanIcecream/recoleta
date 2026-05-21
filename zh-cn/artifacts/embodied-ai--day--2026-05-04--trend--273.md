---
kind: trend
trend_doc_id: 273
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
topics:
- robotics
- vision-language-action models
- robot data
- inference latency
- simulation augmentation
run_id: materialize-outputs
aliases:
- recoleta-trend-273
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/robot-data
- topic/inference-latency
- topic/simulation-augmentation
language_code: zh-CN
---

# 机器人 VLA 部署主张面临数据规模和控制延迟测试

## Overview
这一时期最强的信号是 Vision-Language-Action（VLA）机器人策略面临实际部署压力。MolmoAct2 用开放权重和机器人数据集提出可复现性主张。Latent Bridge 和异步推理基准关注策略能否在不损失任务成功率的情况下保持较高控制频率。

## Clusters

### 开放 VLA 模型和机器人数据集
MolmoAct2 是这一时期最明确面向部署的发布。论文描述了一个开放的 VLA 系统，并发布了权重、代码和训练数据。它的主干 Molmo2-ER 是一个 4B 视觉语言模型（VLM），先在 330 万样本的具身推理语料上训练，再通过动作分词器和连续动作专家连接到机器人动作。

数据发布支撑了这项主张的很大一部分。作者报告了 720 小时的双臂 YAM 数据、经过筛选且包含 38,059 个 episode 的 SO-100/101 社区数据集，以及经过筛选且包含 74,604 个成功 episode 的 DROID Franka 子集。他们还报告 Molmo2-ER 在 13 个具身推理基准上的平均表现为 63.8%，比 Molmo2 提高 17 个百分点。提供的摘录称，MolmoAct2 在仿真和真实世界基准上超过了强基线，但没有给出底层任务成功率。

#### Evidence
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): 摘要列出了 MolmoAct2 的组件、发布资产、数据集和报告的基准结果。

### 用于 VLA 训练数据的仿真视频转换
Seeing Realism from Simulation 通过把仿真机器人视频转换为更逼真的训练视频，同时保留动作轨迹，来处理数据瓶颈。该流水线为仿真视频生成说明文字，改写场景描述以改变外观，使用深度作为几何条件，并用 Cosmos-Transfer 2.5 生成逼真视频。核心集采样器按动作预测损失和视觉多样性选择样本，因此该方法不用增强每一条轨迹。

当评估加入视觉或语言变化时，收益最大。在 RoboTwin 2.0 上，RDT-1B 在 Hard 单任务设置中提高 10.0 个百分点，在使用 10% 增强核心集的 32 任务多任务设置中提高 8.0 个百分点。在 LIBERO-Plus 上，pi_0 整体提高 5.1 个百分点，在物体布局和指令变化上的提升更大。标准 LIBERO 出现小幅下降，这与论文自己的解释一致：那里的训练和测试设置已经相似。

#### Evidence
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): 摘要给出了增强流水线，以及报告的 RoboTwin、LIBERO-Plus 和 LIBERO 结果。

### 推理速度和陈旧观测控制
两篇论文把延迟视为 VLA 部署的核心约束。Latent Bridge 通过在完整主干步骤之间预测特征或键值缓存增量，减少对大型 VLM 主干的调用。在 LIBERO 上，它报告 GR00T-N1.6-3B 每步 49 ms 时成功率为 94.54%，同步推理每步 90 ms 时为 96.58%。对于 pi_0.5，它报告每步 46 ms 时为 96.92%，同步推理每步 76 ms 时为 96.96%。

异步推理基准研究了相关问题：动作块生成过慢时，观测会变旧。它在匹配设置下比较了 IT-RTC、TT-RTC、VLASH 和 A2C2。在报告的测试中，A2C2 在高延迟下表现最好：在 Kinetix 上，它在延迟 d=8 前一直保持 90% 以上的解题率；在 LIBERO 上，它在 d=20 时达到约 58% 成功率，而朴素异步基线约为 10–12%。TT-RTC 在有效时运行时配置最简单，没有额外推理开销。

#### Evidence
- [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](../Inbox/2026-05-04--latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-language-action-model-inference.md): 摘要报告了 Latent Bridge 方法、VLM 调用减少、延迟和成功率。
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): 摘要报告了异步推理比较和高延迟结果。
