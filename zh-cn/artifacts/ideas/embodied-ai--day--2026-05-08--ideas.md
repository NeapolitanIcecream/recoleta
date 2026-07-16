---
kind: ideas
granularity: day
period_start: '2026-05-08T00:00:00'
period_end: '2026-05-09T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- tactile control
- federated learning
- policy adaptation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/tactile-control
- topic/federated-learning
- topic/policy-adaptation
language_code: zh-CN
---

# 机器人控制回路的部署信号

## 摘要
机器人团队可以用最近的 VLA 论文里的具体流程，测试紧凑潜在规划、门控触觉纠正和私有日志训练。现在真正的落地阻碍不只是模型大小或基准分数，而是控制环在失效点有没有合适的部署信号：可达的未来状态、接触反馈，或无法集中保存的日志所对应的任务标签。

## Reachability checks for latent world-model planning
在 VLA 里加世界模型的团队，应该先测试潜在轨迹能不能被规划器使用，再相信预测损失。OneWM-VLA 给出了一条可行的实现路径：冻结 π0 的大部分参数，把每个相机视图和每一帧压缩成一个语义潜在 token，然后用一个 flow-matching 模型同时生成未来潜在 token 和动作片段。文中报告的提升足够支撑做一个小型原型，包括在 LIBERO 上 98.1% 的平均成功率，以及在真实 Piper 机械臂干净条件下 71.7% 的平均成功率。

缺的检查是可规划性。RC-aux 说明了原因：短视野的潜在预测仍然会产生潜在捷径，目标在潜在空间里看起来很近，动作预算内却到不了。一个低成本评估方法，是在世界模型测试集中加入有限预算可达性标签和时间硬负样本，然后在有障碍或长时程任务上，把动作成功率和终端潜在距离对比起来。对于 Wall 任务，RC-aux 把成功率从 LeWM 控制器的 50.4 ± 6.5 提高到 83.6 ± 3.6，规划器消融也显示，可达性感知规划器在训练之外还能带来额外收益。

### 资料来源
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA compresses each view and frame into one semantic token, jointly generates latent tokens and action chunks, and reports LIBERO and real Piper-arm gains.
- [Predictive but Not Plannable: RC-aux for Latent World Models](../Inbox/2026-05-08--predictive-but-not-plannable-rc-aux-for-latent-world-models.md): RC-aux identifies latent shortcuts as a planning failure mode and reports large gains from finite-budget reachability supervision.

## Gated tactile correction loops for contact-rich VLA tasks
接触密集型机器人任务需要一条比常规 VLA 推理节奏更快的纠正路径。AT-VLA 的改造很直接：加一个轻量级触觉编码器来处理三维法向力和三维切向力，训练一个接触门控，再运行双流循环，让视觉语言推理保持低频，触觉动作纠正以更高频率运行。这个门控只在检测到接触后才激活触觉输入，从而保护接触前的视觉定位。

这对做解袋子、擦拭、盖章、拧盖、插入等任务的团队最相关，因为这些任务里光靠视觉看不到受力状态。一个实用测试是，针对某个接触密集操作收集 30 到 50 个演示，给门控标注接触状态，然后在推理时关闭触觉输入，比较成功率。AT-VLA 报告闭环触觉反应时间在 0.04 秒以内，并把真实机器人上的擦花瓶成功率提高到 0.67，而 GO-1 和 π0.5 分别是 0.07 和 0.33；解袋子成功率提高到 0.33，而另外两者分别是 0.20 和 0.00。

### 资料来源
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](../Inbox/2026-05-08--at-vla-adaptive-tactile-injection-for-enhanced-feedback-reaction-in-vision-language-action-models.md): AT-VLA adds gated tactile feedback, a dual-rate tactile correction stream, and reports real-robot gains on contact-rich tasks.

## Federated pseudo-instruction training for private robot logs
有视觉-动作机器人日志的运营方，可以把私有车队数据变成 VLA 训练数据，而不用集中原始视频，也不用让员工写语言标注。ForgeVLA 给出的流程是：先在一个小型公开 VLA 数据集上训练具身指令分类器，再把它本地运行在每个客户端的视觉-动作对上，分配伪指令；然后用动作损失加对比规划损失训练客户端策略，最后在服务器端聚合更新，同时维护一个全局任务表示库。

第一次部署检查应当很窄：为某一类机器人选定固定指令集，在留出的日志上做本地伪标注，检查不同客户端的任务嵌入是否仍然分开。论文把非 i.i.d. 机器人数据下的特征坍塌列为一种失败模式，所以在更长的联邦训练前，嵌入分离应该进入验收测试。ForgeVLA 在 LIBERO-Goal 上达到 55.2% 的成功率和 100% 的 Pass@50，而 FedAvg 是 28.8% 和 80%；实验使用 10 个客户端、20 轮通信和每轮 5 个本地 epoch。

### 资料来源
- [ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations](../Inbox/2026-05-08--forgevla-federated-vision-language-action-learning-without-language-annotations.md): ForgeVLA trains from distributed vision-action logs with on-device pseudo instructions, contrastive planning loss, and adaptive server aggregation, with measured gains over FedAvg.
