---
kind: ideas
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- VLA
- failure recovery
- long-horizon planning
- world models
- sim-to-real
- embodied datasets
tags:
- recoleta/ideas
- topic/robotics
- topic/vla
- topic/failure-recovery
- topic/long-horizon-planning
- topic/world-models
- topic/sim-to-real
- topic/embodied-datasets
language_code: zh-CN
---

# 机器人策略可靠性

## Summary
机器人团队可以用具体产物测试可靠性工作：用于接触漂移的恢复标签 rollout、用于长时程 VLA 推理的熵门控搜索、转换为零售适应机器人动作流的门店视频，以及用于可变形物体的动作条件世界模型。

## 面向高接触 VLA 任务的恢复标签 rollout 缓冲区
从事双臂或高接触操作的 VLA 团队应把失败和恢复片段加入训练缓冲区，并使用单独标签，然后用注入的抓取错误评估策略。RePO-VLA 给出了清晰做法：从完整 episode 中切出恢复片段，为这些片段重置观测历史，用可靠性衰减保留失败 rollout 中有用的前缀，并给终止漂移分配低价值。部署路径也可操作，因为论文报告的策略使用固定的高价值条件，不需要在线失败检测器，也不需要手写重试规则。

第一个低成本测试可以围绕已经会让机器人失效的故障模式建立一个小型对抗套件：过早闭合、抓取滑移、抓取位置偏移和抓取姿态不匹配。RePO-VLA 报告平均对抗成功率从 20% 升至 75%；其 FRBench-Sim 数据包含 46 个任务中的 23,453 个双臂 episode，其中包括 6,392 个经过验证的失败-恢复 episode。这个规模大于多数实验室一开始会复制的规模，但流程足够清楚，可以先在少数高价值任务上试点，再扩大采集。

### Evidence
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): 记录了 RePO-VLA 的成功、失败和恢复标签流程，FRBench-Sim 规模，注入错误类型，以及报告的对抗成功率提升。
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): 确认部署使用固定的高价值条件，没有在线失败检测器或启发式重试规则。

## 用于长时程 VLA 推理的熵触发动作块搜索
机器人部署团队可以加入一个推理时门控，只在 VLA 策略不确定时花费额外算力。CAPS 保持基础策略不变，根据动作熵计算上下文 SNR，并在熵超过阈值时，对未来动作块运行 Metropolis-Hastings 搜索。不确定性较低时，它使用贪心执行。

这适合长时程任务，因为一个局部看来合理的动作就可能丢失指令目标。验证路径很直接：在 rollout 期间记录熵，用动作块搜索重放高熵窗口，并将任务成功率和延迟与基础策略比较。CAPS 报告在 RoboTwin 1.0 上配合 π0 的平均成功率为 47.4%，相比之下 π0 为 32.2%，π0 加 TACO 为 41.3%。在 Simpler-WindowX 上，它报告平均成功率为 60.5%，高于 π0 的 48.0% 和 π0 加 TACO 的 55.5%。

### Evidence
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): 概述了 CAPS 的熵/SNR 触发器、Metropolis-Hastings 动作块搜索，以及在 RoboTwin 和 Simpler-WindowX 上报告的成功率。
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): 确认 CAPS 是一种无需训练的推理时方法，用于处理长时程 VLA 指令漂移。

## 生成机器人动作流的零售视频采集管线
零售机器人团队可以先采集店内人类活动，再投入昂贵的机器人遥操作。SABER 展示了一条具体的数据流程：用第一视角相机和固定 360° 相机记录自然的杂货店工作，估计手部和身体运动，人工修正姿态估计，并把结果重定向为机器人兼容的动作目标。得到的数据流覆盖潜在动作序列、灵巧手部姿态轨迹，以及用于人形机器人的全身运动。

这直接处理了门店机器人采用中的阻碍：通用 VLA 训练数据常缺少货架拣选、冰箱打开、篮筐装载、地面拾取、遮挡、光照和多样包装。SABER 报告基于约 100 小时真实门店采集得到 44.8K 个训练样本，并将 GR00T N1.6 后训练到在 10 个 RoboBenchMart 任务上达到 29.3% 的平均成功率；相比之下，仅用仿真微调为 13.4%。一个可操作的试点做法是采集一条过道，把一小组员工动作转换成同样的三类监督流，并测试在最常失败的门店特定动作上任务成功率是否提高。

### Evidence
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): 记录了 SABER 的门店采集流程、数据集组成、GR00T N1.6 后训练设置，以及报告的 RoboBenchMart 改进。
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): 确认零售机器人的数据缺口，以及在没有遥操作开销的情况下使用真实店内采集。
