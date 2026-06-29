---
kind: ideas
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot manipulation
- VLA policies
- real-robot evaluation
- occlusion
- dexterous manipulation
- sim-real correlation
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vla-policies
- topic/real-robot-evaluation
- topic/occlusion
- topic/dexterous-manipulation
- topic/sim-real-correlation
language_code: zh-CN
---

# Real-world robot control reliability

## Summary
这段时间的机器人操作工作指向三项实际改动：用固定的实体回放流程评测腕部视角策略，在执行前加入 RGB-D 动作检查，以及通过共享手部关键点和接触标签，利用人类视频训练灵巧手策略。

## Fixed real-robot rollout protocols for UMI-style wrist-view policies
训练 UMI 风格桌面策略的团队，应先加入可重复的实体评测流程，再比较模型版本。UMI-Bench 1.0 给出了一种可直接照用的做法：固定工作站设置、腕部视角 RGB 输入、场景重置图像、场景 JSON、回放日志、人工评分、Full Success Rate，以及 0 到 100 的 Progress Score。真正有用的是按已见和未见因素拆分，因为它能把布局、位姿、动力学、物体身份和外观引起的失败分开。

这对目前用临时重置或换相机方式比较策略的实验室很重要。UMI-Bench 报告，π0.5 在三模型比较中以 55.84 的平均 Overall Score 领先，但更直接的结果是 Progress Score 的下降：Seen/Seen 轮次为 59.62，在位置、布局、位姿或动力学变化下为 45.33，在组合变化下为 40.19。策略发布清单可以照这个结构做，每个任务保留 20 到 50 次回放、保存重置图像、因素标签和每次回放的失败记录。同一张评测表也可以把仿真只留给排名检查，前提是它能保住真实世界的排序；这项 sim-real 研究发现，在测试的模拟器里，REALM 的策略排序相关性最好，模拟器后训练前的 Spearman 为 0.700，之后为 0.875。

### Evidence
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): UMI-Bench specifies the workstation, reset, logging, scoring, task-factor splits, and reported degradation under physical shifts.
- [A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation](../Inbox/2026-06-09--a-practical-recipe-towards-improving-sim-and-real-correlation-for-vla-evaluation.md): The sim-real study reports policy-ranking correlation metrics and shows why simulation should be checked against real rollout decisions.

## RGB-D action verification before VLA policy execution
VLA 操作部署可以在现有策略外面加一个执行前动作验证器。验证器从冻结策略里采样多个候选 7D 动作，把深度回投到 3D 场景坐标，对接触和间隙几何打分，然后执行分数最高的候选动作。对那些在一次性输出后出现抓取失败、轻微位姿误差、碰撞或子目标推进错误的团队，这种做法很合适。

VeriSpace 是最清楚的实现参考。把它用在 OpenVLA 和 SimplerEnv-WidowX 上时，四个任务、每个任务 50 次试验的平均成功率从 37.0% 提高到 55.0%。列表中增幅最大的任务是 Stack Cubes，从 28.0% 到 62.0%。一个成本不高的接入测试，是记录前五个候选动作、验证器分数、由深度得到的接触特征，以及执行结果，任务要选那些一旦失败就会把场景改到难以恢复的地方。如果验证器只在简单场景里有用，就把它留作诊断工具；如果它能减少第一次动作的物理错误，就该放进控制回路。

### Evidence
- [VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models](../Inbox/2026-06-09--verispace-spatially-grounded-action-verification-for-vision-language-action-models.md): VeriSpace describes candidate action sampling, RGB-D spatial scoring, pairwise ranking, and the reported success gains.
- [VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models](../Inbox/2026-06-09--verispace-spatially-grounded-action-verification-for-vision-language-action-models.md): The paper frames the operational failure mode: one-shot action prediction can cause grasp failure, collision, or wrong task progression.

## Dexterous-hand training from human video with wrist, fingertip, object, and contact labels
灵巧手团队可以先测试一条基于人类视频的数据流程，再投入数周多指遥操作。Dexterous Point Policy 用六个共享的 3D 手部点，手腕和五个指尖，再加上物体点、语言、相机位姿和指尖接触标签。部署时，逆运动学把预测关键点映射到机器人关节，接触标志再加上用于指尖力的闭合偏移。

它报告的差距大到足以支持先在一个抓放任务和一个工具使用任务上做小规模复现。在 8 个真实机器人灵巧任务上，DPP 的平均成功率为 75.0%，而 Point Policy 为 3.7%，VITRA 为 1.0%。它的消融结果把 71.3 个百分点的提升归因于接触预测，而不是只用点的基线。接入的主要障碍是标注质量：流程需要可靠的手部关键点、物体掩码、深度或双目估计，以及接触标签。首次内部测试应先看提取出的指尖轨迹和接触标志在不同相机角度和物体类别下是否稳定，再训练完整策略。

### Evidence
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](../Inbox/2026-06-09--dexterous-point-policy-learning-point-based-dexterous-hand-policies-from-human-demonstrations.md): Dexterous Point Policy reports the six-keypoint representation, human-video-only training setup, contact prediction, and real-robot results.
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](../Inbox/2026-06-09--dexterous-point-policy-learning-point-based-dexterous-hand-policies-from-human-demonstrations.md): The paper states the embodiment gap and the high cost of robot demonstrations for dexterous manipulation.
