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

## 概览
这一时期最强的信号是对 Vision-Language-Action（VLA）机器人策略的实际部署压力。MolmoAct2 用开放权重和机器人数据集来说明可复现性。Latent Bridge 和异步推理基准关注的是，策略能否在不损失任务成功率的情况下保持较高控制频率。

## 研究发现

### Open VLA models and robot datasets
MolmoAct2 是这一时期最明确的面向部署的发布。论文描述了一个开放的 VLA 系统，公开了权重、代码和训练数据。它的骨干模型 Molmo2-ER 是一个 4B 视觉-语言模型（VLM），先在一个包含 330 万样本的具身推理语料上训练，再通过动作分词器和连续动作专家连接到机器人动作。

数据公开是这项主张的重要部分。作者报告了 720 小时的双臂 YAM 数据、一个经过筛选的 SO-100/101 社区数据集，包含 38,059 个 episode，以及一个经过筛选的 DROID Franka 子集，包含 74,604 个成功 episode。他们还报告，Molmo2-ER 在 13 个具身推理基准上的平均性能为 63.8%，比 Molmo2 高 17 个点。给出的摘录说 MolmoAct2 在模拟和真实世界基准上都超过了强基线，但没有给出底层任务成功率。

#### 资料来源
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): Summary lists MolmoAct2 components, released assets, datasets, and reported benchmark results.

### Simulation video transfer for VLA training data
Seeing Realism from Simulation 通过把模拟机器人视频转成更逼真的训练视频，同时保留动作轨迹，来应对数据瓶颈。这个流程先给模拟视频生成说明文字，再改写场景描述以改变外观，使用深度图作为几何条件，并用 Cosmos-Transfer 2.5 生成逼真的视频。coreset 采样器按动作预测损失和视觉多样性选取样本，所以方法不会给每条轨迹都做增强。

当评测加入视觉或语言变化时，收益最明显。在 RoboTwin 2.0 上，RDT-1B 在 Hard 单任务设置下提升了 10.0 个点，在一个 32 任务多任务设置中、使用 10% 增强 coreset 时提升了 8.0 个点。在 LIBERO-Plus 上，pi_0 的总体性能提升了 5.1 个点，在物体布局和指令变化上提升更大。标准 LIBERO 出现了小幅下降，这和论文自己的解释一致，因为那里的训练和测试设置本来就很相似。

#### 资料来源
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): Summary gives the augmentation pipeline and reported RoboTwin, LIBERO-Plus, and LIBERO results.

### Inference speed and stale-observation control
有两篇论文把延迟当作 VLA 部署的核心约束。Latent Bridge 通过在完整骨干步骤之间预测特征或键值缓存的增量，减少对大型 VLM 骨干的调用。在 LIBERO 上，它报告 GR00T-N1.6-3B 在每步 49 ms 时成功率为 94.54%，而同步推理在每步 90 ms 时为 96.58%。对于 pi_0.5，它报告每步 46 ms 时为 96.92%，而 76 ms 时为 96.96%。

异步推理基准研究的是动作块生成太慢时出现的观察陈旧问题。它在相同设置下比较了 IT-RTC、TT-RTC、VLASH 和 A2C2。A2C2 在报告的测试中最能应对高延迟：在 Kinetix 上，它在延迟 d=8 之前一直保持 90% 以上的解题率；在 LIBERO 上，它在 d=20 时的成功率约为 58%，而朴素异步基线只有大约 10% 到 12%。TT-RTC 在工作正常时运行开销最小，没有额外推理开销。

#### 资料来源
- [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](../Inbox/2026-05-04--latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-language-action-model-inference.md): Summary reports Latent Bridge method, VLM-call reduction, latency, and success rates.
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): Summary reports the asynchronous-inference comparison and high-delay results.
