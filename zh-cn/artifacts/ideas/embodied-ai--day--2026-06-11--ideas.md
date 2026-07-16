---
kind: ideas
granularity: day
period_start: '2026-06-11T00:00:00'
period_end: '2026-06-12T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot manipulation
- VLA
- tactile sensing
- world models
- data annotation
- dexterous robotics
- real-time control
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vla
- topic/tactile-sensing
- topic/world-models
- topic/data-annotation
- topic/dexterous-robotics
- topic/real-time-control
language_code: zh-CN
---

# 机器人操作部署检查

## 摘要
机器人操作团队可以根据现有证据做三项具体改动：按物理交互信号给示范标签打分，在部署自回归 VLA 策略前加入固定延迟解码测试，并在标准化接触硬件前按传感器类型测试触觉策略。

## 交互式可靠性评分用于机器人示范标签
机器人数据团队应在操作示范的自动标注流程里加入可靠性门控。SPARC 给出了一个可直接照着做的流程：通过夹爪阶段、语言解析、目标掩码、跟踪、3D 提升、物体运动、夹爪距离和机器人身体重叠，识别正在被操作的物体。输出是标签加可靠性分数，这样数据团队可以设定精度目标，并保留可用于训练的样本子集。

这正好解决拥挤机器人视频里的一个常见问题：检测器会把高置信度给错物体。一个有用的初始实现，是把现有的检测器和跟踪器标签与基于交互的评分器并行跑在几千条示范上，然后只人工复核接近接受阈值的样本。SPARC 在 IA-Bench 上的交互物体定位准确率是 80.2%，高于 58.1% 的检测置信度基线，并且在 90% 精度工作点下保留了 77.6% 的覆盖率。

### 资料来源
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): SPARC describes interaction-based auto-labeling, reliability thresholds, IA-Bench, and reported localization and coverage results.
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): The source text states why detector confidence can select the wrong manipulated object in cluttered robot demonstrations.

## 自回归 VLA 策略的固定延迟解码测试
部署自回归 VLA 策略的团队，应在机器人试验前把延迟当作可测试的策略约束。实时执行论文给出了一套具体做法：调整动作块的分词方式，以上一个动作块为条件，只解码下一个块中需要的部分，并用受限解码保证每个生成的 token 序列都能在控制器的延迟预算内完成。

部署检查很直接。让策略按机器人的指令间隔运行，测量卡顿和无效动作块，并把任务成功率与同步推理和已有的实时控制基线对比。论文报告，pi0-REALFAST 在 LIBERO 上的平均任务成功率为 95.7%，高于加入实时控制的 pi0 的 89.4%，也高于加入实时控制的 pi0.5 的 94.7%。它还报告了测试设置中的较小额外解码开销，示例大约在 4 到 13 毫秒之间。

### 资料来源
- [Real-Time Execution with Autoregressive Policies](../Inbox/2026-06-11--real-time-execution-with-autoregressive-policies.md): The summary gives the latency problem, action-token recipe, constrained decoding method, and LIBERO success results.
- [Real-Time Execution with Autoregressive Policies](../Inbox/2026-06-11--real-time-execution-with-autoregressive-policies.md): The source text describes asynchronous inference and the need to keep actions continuous while preserving reactivity.

## 面向接触密集操作的跨传感器触觉迁移测试
给机器人加入触觉感知的团队，应先测试策略在不同传感器硬件之间的迁移，再决定固定使用哪一套触觉栈。FTP-1 给出了一个具体的支撑层：把图像、阵列和状态触觉输入映射到共享的、考虑形态的 token 空间，用共享的 Transformer 专家建模这些触觉 token，再把它们与 VLA 风格策略融合。

一个实用的接入测试，是选两个接触密集任务，比如滑动、抓握稳定或插入，用一种触觉传感器训练，然后把同一策略分支跑到一个留出的传感器配置上。这样可以尽早发现硬件锁定问题。FTP-1 在来自 26 个来源、21 种触觉传感器、约 3,000 小时的触觉数据上做预训练，然后报告在未见传感器配置上的平均成功率为 46.6%，高于其 FTP-pi0.5 基线的 15.0%。

### 资料来源
- [FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation](../Inbox/2026-06-11--ftp-1-a-generalist-foundation-tactile-policy-across-tactile-sensors-for-contact-rich-manipulation.md): FTP-1 describes heterogeneous tactile inputs, morphology-aware tokens, pretraining scale, and seen and unseen sensor results.
- [FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation](../Inbox/2026-06-11--ftp-1-a-generalist-foundation-tactile-policy-across-tactile-sensors-for-contact-rich-manipulation.md): The source text states that tactile policies are constrained by differences in modality, resolution, morphology, and contact response across hardware.
