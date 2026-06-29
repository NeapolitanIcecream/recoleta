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

# Robot Policy Reliability

## Summary
机器人团队可以用具体产物来测试可靠性工作：用于接触漂移的恢复标注 rollout、用于长时序 VLA 推理的熵门控搜索、把门店视频转成机器人动作流以适配零售场景，以及面向可变形物体的动作条件世界模型。

## Recovery-labeled rollout buffers for contact-rich VLA tasks
做双臂或高接触操作的 VLA 团队，应该把失败和恢复回合放进训练缓冲区，并用单独标签区分，然后用注入的抓取错误来评估策略。RePO-VLA 给了一个清楚的做法：从完整回合里切出恢复片段，为这些片段重置观测历史，保留失败 rollout 中仍然有用的前缀并做可靠性衰减，同时把终端漂移标成低价值。这个部署路径也很实用，因为论文里的策略直接用固定的高价值条件，不需要在线失败检测器，也不需要手写重试规则。

先做一个低成本测试就行，围绕已经会让机器人出错的几种失败模式：提前闭合、抓取滑脱、抓取位置偏移、抓取姿态不匹配。RePO-VLA 报告平均对抗成功率从 20% 提高到 75%，它的 FRBench-Sim 数据包含 46 个任务上的 23,453 个双臂回合，其中 6,392 个是已验证的失败-恢复回合。这个规模一开始通常不会被大多数实验室照搬，但流程已经足够清楚，可以先在几个高价值任务上试，再扩大采集。

### Evidence
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): Documents RePO-VLA's success, failure, and recovery labeling workflow, FRBench-Sim scale, injected error types, and reported adversarial success gain.
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): Confirms deployment with a fixed high value condition and no online failure detector or heuristic retry rule.

## Entropy-triggered action-chunk search for long-horizon VLA inference
机器人部署团队可以加一个推理时门控，只在 VLA 策略变得不确定时才多花算力。CAPS 保持基础策略不变，根据动作熵计算上下文 SNR，并在熵超过阈值时对未来动作块做 Metropolis-Hastings 搜索。不确定性保持较低时，就直接用贪心执行。

这适合长时序任务，因为一个局部上看起来合理的动作，可能让指令目标在后面丢失。验证路径很直接：在 rollout 中记录熵，用动作块搜索重放高熵窗口，再把任务成功率和延迟与基础策略对比。CAPS 在 RoboTwin 1.0 上用 π0 时平均成功率为 47.4%，对比 π0 的 32.2% 和 π0 加 TACO 的 41.3%。在 Simpler-WindowX 上，它的平均成功率是 60.5%，高于 π0 的 48.0% 和 π0 加 TACO 的 55.5%。

### Evidence
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): Summarizes CAPS's entropy/SNR trigger, Metropolis-Hastings action-chunk search, and reported success rates on RoboTwin and Simpler-WindowX.
- [Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning](../Inbox/2026-05-10--drift-is-a-sampling-error-snr-aware-power-distributions-for-long-horizon-robotic-planning.md): Confirms CAPS as a training-free inference-time method for long-horizon VLA instruction drift.

## Retail video capture pipelines that produce robot action streams
零售机器人团队可以先采集门店内的人类活动视频，再做昂贵的机器人遥操作。SABER 给出了一条具体的数据流程：用头戴式 GoPro 和固定的 360° 相机记录真实超市工作，估计手和身体动作，人工修正姿态估计，再把结果转换成机器人可用的动作目标。最后得到的三类流覆盖潜在动作序列、灵巧手部姿态轨迹，以及面向人形机器人的全身运动。

这正好针对门店机器人落地的阻碍：通用 VLA 训练数据往往覆盖不到货架取物、冰箱打开、篮筐装载、地面取回、遮挡、光照变化和不同包装。SABER 报告从约 100 小时的真实门店采集里得到 44.8K 个训练样本，并用这些数据把 GR00T N1.6 的 10 个 RoboBenchMart 任务平均成功率提高到 29.3%，而只做仿真微调时是 13.4%。一个可行的试点是先采一个货架通道，把少量员工动作转成同样的三类监督流，再测试门店里最常失败的那些动作是否变得更稳。

### Evidence
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): Documents SABER's store-capture workflow, dataset composition, GR00T N1.6 post-training setup, and reported RoboBenchMart improvement.
- [SABER: A Scalable Action-Based Embodied Dataset for Real-World VLA Adaptation](../Inbox/2026-05-10--saber-a-scalable-action-based-embodied-dataset-for-real-world-vla-adaptation.md): Confirms the data gap for retail robotics and the use of real in-store capture without teleoperation overhead.
