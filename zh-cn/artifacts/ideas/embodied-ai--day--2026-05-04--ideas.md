---
kind: ideas
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action models
- robot data
- inference latency
- simulation augmentation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action-models
- topic/robot-data
- topic/inference-latency
- topic/simulation-augmentation
language_code: zh-CN
---

# VLA 评估门槛

## 摘要
机器人操作团队现在可以用更具体的门槛来检验 VLA 说法：跳过主干调用时的每步延迟、动作块延迟下的旧观测成功率、用于视觉变化的定向仿真视频增强，以及来自已发布 MolmoAct2 权重和数据集的可复现基线。

## VLA 动作块的延迟与旧观测测试台
评估 VLA 策略的机器人团队应在常规任务成功率测试之外加入延迟扫描。测试应记录每个控制步的端到端毫秒数、VLM 主干调用频率、动作块长度，以及在固定延迟下的成功率，例如 d=0、2、4、8、15 和 20。这样可以捕捉单独看成功率表时看不出的失败模式：下一段动作块是在旧观测上算出来时，机器人仍在继续移动。

两篇近期论文给出了这个检查的可用基线。Latent Bridge 报告在几乎同步的 LIBERO 成功率下，把 GR00T-N1.6-3B 的每步耗时从 90 ms 降到 49 ms，把 pi_0.5 从 76 ms 降到 46 ms，方法是在完整 VLM 调用之间预测特征或 KV-cache 的增量。异步推理基准展示了另一个控制问题：在 LIBERO 延迟 d=20 时，A2C2 的成功率约为 58%，而朴素异步基线约为 10–12%。实际接入时，一个可行的门槛是在任何真实机器人试验前先跑完这两项测量：先看跳过主干调用后的延迟，再看动作块延迟下的任务成功率。

### 资料来源
- [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](../Inbox/2026-05-04--latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-language-action-model-inference.md): Latent Bridge reports reduced per-step latency and close task-success retention for GR00T-N1.6-3B and pi_0.5.
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): The asynchronous-inference benchmark compares VLA delay methods and reports success rates under increasing action-chunk delays.
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): The paper describes why synchronous execution lowers control frequency and naive asynchronous execution creates stale-observation and chunk-boundary failures.

## 用于布局和指令变化的 coreset 仿真视频增强
已有仿真轨迹的团队，可以在继续采集更多真实机器人数据之前，先做一轮小而针对性的图传输实验。具体流程是用动作预测损失和视觉多样性选出一个 coreset，生成保持相同动作轨迹的真实风格变体，然后用混合数据训练 VLA 策略。验证集应包含物体布局、纹理、光照和语言指令的变化。

Seeing Realism from Simulation 给出了第一次实验可参考的规模。用 10% 的增强 coreset，RDT-1B 在 RoboTwin 2.0 Hard 多任务上的成功率从 23.0% 提高到 31.0%，LIBERO-Plus 上的 pi_0 从 42.7% 提高到 47.8%，其中物体布局和指令变化上的提升更大。同一篇论文也报告了在标准 LIBERO 上的小幅下降，所以这个检查应优先放在训练和测试视觉差异足够大的部署场景。

### 资料来源
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): The summary describes the video-transfer pipeline, coreset selection method, and reported gains on RoboTwin 2.0 and LIBERO-Plus.
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): The abstract states the method converts simulated VLA videos into realistic training videos while preserving task semantics and action trajectories.
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): The paper describes preserving task semantics and action trajectories while diversifying the visual environment.

## 使用 MolmoAct2 权重和机器人数据集的可复现本地基线
比较封闭或部分开放的机器人策略的实验室，现在可以围绕 MolmoAct2 建一个本地基线。最有用的最低流程是先在一小组本地任务上运行已发布的模型和代码，然后用同一套评估脚本，对已发布的 SO-100/101、DROID 或 BimanualYAM 数据源进行微调或筛选。这样团队就能在花时间采集大规模本地数据之前，先检查自己的机器人、相机和任务组合是否受益于这个开源模型。

MolmoAct2 之所以相关，是因为这次发布包含模型权重、代码和训练数据，其中包括 720 小时的双臂 YAM 轨迹、38,059 个 SO-100/101 片段，以及 74,604 个过滤后的 DROID 成功片段。论文也列出了本地团队已经会遇到的部署障碍：昂贵的硬件假设、推理型策略带来的延迟，以及低于稳定使用门槛的成功率。缺少的操作步骤，是在实验室自己的任务上做一次可复现运行，把成功率、干预次数和控制延迟一起记录下来。

### 资料来源
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): The summary reports released weights, code, training data, model components, dataset sizes, and deployment constraints.
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): The paper lists the released Hugging Face model, dataset, and code links.
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): The paper describes practical deployment blockers and the released robot datasets.
