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

# 机器人控制环的部署信号

## Summary
机器人团队可以用近期 VLA 论文中的具体协议测试紧凑潜在规划、门控触觉校正和私有日志训练。常见采用阻碍已经超出模型大小或基准分数，还包括控制环在失败点是否拥有合适的部署信号：可达的未来状态、接触反馈，或无法汇集日志中的任务标签。

## 面向潜在世界模型规划的可达性检查
团队在给 VLA 添加世界模型时，应先测试规划器能否使用潜在状态展开，再信任预测损失。OneWM-VLA 给出了一条可落地的构建路径：冻结 π0 的大部分参数，把每个相机视角和每一帧压缩成一个语义潜在 token，然后用一个流匹配模型同时生成未来潜在 token 和动作片段。报告中的增益足以支持做一个小型原型，包括 LIBERO 上 98.1% 的平均成功率，以及干净条件下真实 Piper 机械臂 71.7% 的平均成功率。

缺少的检查是可规划性。RC-aux 说明了原因：短时域潜在预测仍可能产生潜在捷径，使目标看起来很近，但在动作预算内无法到达。一个低成本评估方法是把有限预算可达性标签和时间困难负样本加入世界模型测试套件，然后在有障碍或长时域任务上比较动作成功率与终端潜在距离。Wall 任务上，RC-aux 将成功率从 LeWM 对照的 50.4 ± 6.5 提高到 83.6 ± 3.6；规划器消融显示，可达性感知规划器在单独训练之外还能增加价值。

### Evidence
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA 将每个视角和每一帧压缩成一个语义 token，联合生成潜在 token 和动作片段，并报告了 LIBERO 和真实 Piper 机械臂上的增益。
- [Predictive but Not Plannable: RC-aux for Latent World Models](../Inbox/2026-05-08--predictive-but-not-plannable-rc-aux-for-latent-world-models.md): RC-aux 将潜在捷径识别为一种规划失败模式，并报告了有限预算可达性监督带来的大幅增益。

## 面向接触密集型 VLA 任务的门控触觉校正循环
接触密集型机器人任务需要一条快于常规 VLA 推理节奏的校正路径。AT-VLA 是一个具体改造方案：添加一个用于 3D 法向力和切向力的轻量触觉编码器，训练一个接触门控，并运行双流循环，让视觉-语言推理保持低频，同时让触觉动作校正以更高频率运行。该门控只在检测到接触后激活触觉输入，从而保护接触前的视觉定位。

这最适合正在处理拉开拉链、擦拭、盖章、旋转瓶盖、插入等任务的团队，因为这些任务中单靠视觉会漏掉力状态。一个实用测试是为一个接触密集操作收集 30 到 50 条示范，为门控标注接触状态，并在推理时禁用触觉输入来比较成功率。AT-VLA 报告闭环触觉反应时间在 0.04 s 内，并将真实机器人 Wipe Vase 成功率提高到 0.67，而 GO-1 为 0.07、π0.5 为 0.33；Unzip Bag 提高到 0.33，而对照为 0.20 和 0.00。

### Evidence
- [AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models](../Inbox/2026-05-08--at-vla-adaptive-tactile-injection-for-enhanced-feedback-reaction-in-vision-language-action-models.md): AT-VLA 添加门控触觉反馈、双速率触觉校正流，并报告了接触密集任务上的真实机器人增益。

## 面向私有机器人日志的联邦伪指令训练
拥有视觉-动作机器人日志的运营方可以把私有机队数据转成 VLA 训练数据，无需集中原始视频，也无需让员工编写语言标注。ForgeVLA 展示了流程：在一个小型公共 VLA 数据集上训练具身指令分类器，在每个客户端本地对视觉-动作样本分配伪指令，用动作损失加对比规划损失训练客户端策略，并在服务器端聚合更新，同时维护一个全局任务表示库。

首次部署检查应保持范围较窄：为一个机器人系列选择固定指令集，在留出日志上运行本地伪标注，并检查任务嵌入在不同客户端之间是否仍然分离。论文把非独立同分布机器人数据下的特征坍缩列为失败模式，因此在更长的联邦训练运行之前，嵌入分离应纳入验收测试。LIBERO-Goal 上，ForgeVLA 达到 55.2% 成功率和 100% Pass@50，而 FedAvg 为 28.8% 和 80%；实验使用 10 个客户端、20 轮通信、每轮 5 个本地 epoch。

### Evidence
- [ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations](../Inbox/2026-05-08--forgevla-federated-vision-language-action-learning-without-language-annotations.md): ForgeVLA 使用设备端伪指令、对比规划损失和服务器端自适应聚合，从分布式视觉-动作日志中训练，并报告了相对 FedAvg 的实测增益。
