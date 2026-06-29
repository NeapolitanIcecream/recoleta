---
kind: ideas
granularity: day
period_start: '2026-06-03T00:00:00'
period_end: '2026-06-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- 3D geometry
- tactile sensing
- quadrotor navigation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/3d-geometry
- topic/tactile-sensing
- topic/quadrotor-navigation
language_code: zh-CN
---

# 机器人策略验证门

## Summary
机器人团队可以在现有策略工作里加上三项实用检查：在训练前验证 UMI 风格示范，在接触密集任务上做触觉消融，在真实飞行测试前用跨环境预测质量给四旋翼世界模型排序。每项检查都针对最近结果里出现过的一种失效模式：不可执行轨迹、被摄像头掩盖的接触错误，以及没有选出真实世界赢家的仿真分数。

## Physical-validation gates for UMI demonstrations before VLA training
使用 Universal Manipulation Interface 数据的团队可以加一个摄取门，拒绝或降低那些有缺失片段、不连续、自碰撞风险，或在目标机器人上执行精度差的轨迹权重。VISTA 给出了这个流程的具体做法：它在训练前先验证 UMI 轨迹，并把动作数据和 UMI-VQA 配在一起，后者是一个面向腕部鱼眼视角的 800 万样本数据集。对正在扩大手持示范采集规模的团队来说，问题很直接：原始 UMI 数据里可能包含机器人无法执行的动作，而鱼眼腕部相机会让在标准图像上学到的 VLM 特征失真。

一个成本较低的落地测试，是把验证门跑在一批留出的 UMI 轨迹上，分别用保留和剔除后的数据训练两个小策略，然后在几个会考验可达范围和腕部相机遮挡的任务上比较真实执行结果。同一套流程还应记录哪些失败来自视觉定位，哪些来自运动学，因为这两类问题需要不同修复方式。

### Evidence
- [VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training](../Inbox/2026-06-03--vista-vision-grounded-and-physics-validated-adaptation-of-umi-data-for-vla-training.md): VISTA describes fisheye wrist-camera mismatch, robot-infeasible UMI trajectories, an 8M-sample UMI-VQA dataset, and physical-validation scores for completeness, continuity, self-collision risk, and execution fidelity.
- [VISTA: Vision-Grounded and Physics-Validated Adaptation of UMI data for VLA Training](../Inbox/2026-06-03--vista-vision-grounded-and-physics-validated-adaptation-of-umi-data-for-vla-training.md): The paper abstract states that VISTA scores each valid trajectory before training and reports that physical-validation scores predict deployment success.

## Tactile ablation suites for contact-heavy manipulation policies
操控团队应该为那些摄像头看不到关键接触状态的任务加一套小型触觉消融测试。HapTile 提供了一个可直接参考的模板：在遥操作时采集语言、第三人称 RGB、腕部 RGB、指尖触觉图像、机器人状态、7D 动作、时间戳和触觉反馈，然后用仅视觉输入、原始触觉图像、以及触觉标记特征来评估策略。

最先加入的任务应是插销、擦拭、转瓶和倒液。HapTile 在这些任务里报告了明显收益，例如 π0 在插销任务上从仅视觉输入的 0% 升到原始触觉图像下的 90%，白板擦拭从 50% 升到使用触觉标记特征时的 100%。倒液结果提醒人们要按任务来做消融：在报告的基线里，触觉标记特征反而降低了成功率。一个实用的上线检查，是要求每个新策略先通过接触测试套件，并按任务报告模态效果，再进入更大范围的真实世界试验。

### Evidence
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](../Inbox/2026-06-03--haptile-a-haptic-informed-vision-tactile-language-action-dataset-for-contact-rich-imitation-learning.md): HapTile specifies the dataset fields, teleoperation haptic feedback, benchmark input settings, and task-level results showing both tactile gains and tactile regressions.
- [HapTile: A Haptic-Informed Vision-Tactile-Language-Action Dataset for Contact-Rich Imitation Learning](../Inbox/2026-06-03--haptile-a-haptic-informed-vision-tactile-language-action-dataset-for-contact-rich-imitation-learning.md): The abstract states that most VLA datasets remain vision-only and that HapTile combines language conditioning, visuotactile observations, action trajectories, and haptic-informed demonstrations.

## Cross-environment reconstruction checks for quadrotor world models before real flight
训练 DreamerV3 风格世界模型的四旋翼团队，可以在进室内走廊或森林测试前，用跨环境重建指标筛选候选模型。做法很直接：在多个仿真随机性等级上训练模型，在留出布局下评估重建 MSE 和 SSIM，并在选定硬件策略前查看上下文阶段和想象阶段的预测。

这个提醒来自一个真实部署结果：仿真策略分数最好的模型在真实四旋翼上失败了，而另一些模型能穿过狭窄间隙到达目标。MAD 还提供了一种适合敏捷飞行的互补做法：训练潜变量模型，让它从深度和本体感觉预测机器人中心坐标系下的占用图和可见性图，再把这个潜状态用进策略里。一个最小验证流程可以把两者结合起来：先在留出重建和地图预测上比较世界模型候选，再用严格中止规则飞一段短间隙航线。

### Evidence
- [Generalization of World Models under Environmental Variability for Vision-based Quadrotor Navigation](../Inbox/2026-06-03--generalization-of-world-models-under-environmental-variability-for-vision-based-quadrotor-navigation.md): The quadrotor generalization study reports cross-environment reconstruction evaluation, real closed-loop tests, and the failure of the strongest simulation policy on the real platform.
- [MAD: Mapping-Aware World Models for Agile Quadrotor Flight](../Inbox/2026-06-03--mad-mapping-aware-world-models-for-agile-quadrotor-flight.md): MAD describes occupancy and visibility map prediction from depth and proprioception, the learned latent state used for agile flight policies, and real-world forest flight at 5.05 m/s.
