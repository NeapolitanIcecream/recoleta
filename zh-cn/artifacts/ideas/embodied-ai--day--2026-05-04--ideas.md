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

## Summary
机器人操作团队现在可以用更具体的门槛来测试 VLA 声明：跳过主干调用时的每步延迟、动作块延迟下的旧观测成功率、面向视觉变化的定向仿真视频增强，以及基于已发布 MolmoAct2 权重和数据集的可复现基线。

## 面向 VLA 动作块的延迟与旧观测测试台
评估 VLA 策略的机器人团队，应在常规任务成功率测试中加入延迟扫描。测试应记录每个控制步的端到端毫秒数、VLM 主干调用频率、动作块长度，以及在 d=0、2、4、8、15、20 等固定延迟下的成功率。这样可以发现单一成功率表格会掩盖的一类故障：机器人可能还在移动，而下一段动作块是根据旧观测计算出来的。

两篇近期论文为这项检查提供了可用基线。Latent Bridge 通过在完整 VLM 调用之间预测特征或 KV-cache 增量，在保持接近同步推理的 LIBERO 成功率的同时，将 GR00T-N1.6-3B 从每步 90 ms 降到 49 ms，将 pi_0.5 从 76 ms 降到 46 ms。异步推理基准展示了另一个控制问题：在 LIBERO 延迟 d=20 时，A2C2 的成功率约为 58%，而朴素异步基线约为 10–12%。一个实用的采用门槛是，在任何真实机器人试验前，让候选策略通过两项测量：跳过主干调用时的延迟，以及动作块延迟下的任务成功率。

### Evidence
- [Latent Bridge: Feature Delta Prediction for Efficient Dual-System Vision-Language-Action Model Inference](../Inbox/2026-05-04--latent-bridge-feature-delta-prediction-for-efficient-dual-system-vision-language-action-model-inference.md): Latent Bridge 报告称，GR00T-N1.6-3B 和 pi_0.5 的每步延迟降低，同时任务成功率保持接近原水平。
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): 异步推理基准比较了多种 VLA 延迟处理方法，并报告了动作块延迟增加时的成功率。
- [Understanding Asynchronous Inference Methods for Vision-Language-Action Models](../Inbox/2026-05-04--understanding-asynchronous-inference-methods-for-vision-language-action-models.md): 论文说明了同步执行为何会降低控制频率，以及朴素异步执行为何会产生旧观测和动作块边界故障。

## 面向布局和指令变化的 coreset 仿真视频增强
已有仿真轨迹的团队，可以先测试一次小规模、有针对性的视频迁移，再去采集更多真实机器人数据。具体流程是用动作预测损失和视觉多样性选择一个 coreset，生成保留相同动作轨迹的逼真变体，然后用混合数据训练 VLA 策略。验证集应包含变化后的物体布局、纹理、光照和语言指令。

Seeing Realism from Simulation 为首次实验提供了可参考的规模。10% 增强 coreset 将 RDT-1B 在 RoboTwin 2.0 Hard 多任务上的成功率从 23.0% 提高到 31.0%；LIBERO-Plus 上的 pi_0 从 42.7% 提高到 47.8%，在物体布局和指令变化上的提升更大。同一篇论文报告称，标准 LIBERO 上出现小幅下降，因此这项检查应面向训练和测试视觉差异足够影响部署的场景。

### Evidence
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): 摘要描述了视频迁移流程、coreset 选择方法，以及 RoboTwin 2.0 和 LIBERO-Plus 上报告的提升。
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): 摘要称，该方法将仿真 VLA 视频转换为逼真的训练视频，同时保留任务语义和动作轨迹。
- [Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation](../Inbox/2026-05-04--seeing-realism-from-simulation-efficient-video-transfer-for-vision-language-action-data-augmentation.md): 论文描述了在保留任务语义和动作轨迹的同时，增加视觉环境多样性。

## 使用 MolmoAct2 权重和机器人数据集建立可复现本地基线
比较闭源或部分发布机器人策略的实验室，现在可以围绕 MolmoAct2 建立本地基线。最低限度的有用流程是，在少量本地任务上运行已发布的模型和代码，然后用同一套评估脚本，从已发布的 SO-100/101、DROID 或 BimanualYAM 数据源进行微调或筛选。这样，团队可以在投入时间采集大型本地数据集之前，检查自己的机器人、相机和任务组合是否能从开源模型中受益。

MolmoAct2 值得关注，因为这次发布包含模型权重、代码和训练数据，其中包括 720 小时双臂 YAM 轨迹、38,059 个 SO-100/101 episode，以及 74,604 个筛选后的 DROID 成功 episode。论文还列出了本地团队已经会遇到的部署阻碍：昂贵的硬件假设、推理负担较重策略带来的延迟，以及达不到可靠使用水平的成功率。缺少的操作步骤是在实验室自己的任务上做一次可复现运行，并同时记录成功率、干预次数和控制延迟。

### Evidence
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): 摘要报告了已发布的权重、代码、训练数据、模型组件、数据集规模和部署约束。
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): 论文列出了已发布的 Hugging Face 模型、数据集和代码链接。
- [MolmoAct2: Action Reasoning Models for Real-world Deployment](../Inbox/2026-05-04--molmoact2-action-reasoning-models-for-real-world-deployment.md): 论文描述了实际部署阻碍和已发布的机器人数据集。
