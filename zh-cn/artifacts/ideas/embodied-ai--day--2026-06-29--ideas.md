---
kind: ideas
granularity: day
period_start: '2026-06-29T00:00:00'
period_end: '2026-06-30T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- manipulation
- test-time RL
- tactile sensing
- navigation
- autonomous driving
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/test-time-rl
- topic/tactile-sensing
- topic/navigation
- topic/autonomous-driving
language_code: zh-CN
---

# 机器人操作 rollout 检查

## Summary
机器人策略团队可以围绕评估、部署和几何增加面向执行的检查，从当前工作中获得更多价值。实际做法是：在任务关键运动片段上给模型变体排序，在闭环试验前验证感知-动作回路，并为小误差会导致任务失败的接触阶段存储对象相对姿态。

## 机器人 rollout 前的关键区间验证
机器人操作团队应增加一道验证步骤，只在抓取、接触、插入、精细对齐以及类似任务关键片段中计算策略误差。Critical Interval MSE 给出了一套具体做法：标注关键时间步，应用与 rollout 时相同的动作执行流程，用局部动态时间规整对齐预测动作序列和专家动作序列，并用筛选后的误差比较模型变体。

这适合训练大量相近 checkpoint 的团队，因为每次改动都做实体 rollout 太慢，结果波动也可能太大。在 LBM-Eval 上，CI-MSE 与 rollout 成功率的 Spearman ρ = -0.87，原始 MSE 为 -0.61。低成本的采用测试是：取一组已有 rollout 结果的历史 checkpoint，标注留出示范中接触密集的区间，然后检查新排名是否比原始验证损失更接近硬件排名。

### Evidence
- [Critical Interval MSE: Toward Reliable Offline Validation for Robot Manipulation Policies](../Inbox/2026-06-29--critical-interval-mse-toward-reliable-offline-validation-for-robot-manipulation-policies.md): 定义了 CI-MSE、关键区间计分和 rollout 时对齐步骤，并报告其与 rollout 成功率的相关性强于原始 MSE。

## 面向动作语义、坐标系和时序的 VLA 部署预检
将 OpenVLA 风格策略迁移到本地机械臂的团队，应先做部署预检，再把模型质量视为主要故障来源。UR5e 案例研究给出了一份具体检查清单：动作单位和夹爪语义、坐标系约定、相机预处理、模态时序、推理速率、数据集覆盖范围，以及用于执行动作块的控制接口。

同一研究报告称，原始 OpenVLA 在 A100 上的推理速度约为 3 Hz；当集成细节不匹配时，闭环行为不稳定。一个有用的预检是在机器人客户端记录一次开环回放：把录制的相机观测送入服务器，解码动作，按预定坐标系做变换，并在启用自主执行前，将时序和末端执行器运动与示范进行比较。

### Evidence
- [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](../Inbox/2026-06-29--vision-language-action-models-experimental-insights-from-a-real-world-ur5-platform.md): 报告了 UR5e OpenVLA 部署流水线、A100 上约 3 Hz 的推理速度，以及与动作语义、坐标系、时序、预处理和数据覆盖相关的失败。

## 用于桌面操作的对象相对关键姿态记忆
对于重复的桌面任务，小型的对象相对关键姿态库可以让示范在不同场景中复用。OpenSPM 将接近、抓取、抬起、预放置和释放等阶段姿态存为末端执行器与对象坐标系之间的 SE(3) 变换。推理时，系统估计当前 6D 对象姿态，迁移已存储的相对姿态，检查可行性，并在相邻姿态之间生成短动作块。

这适合故障集中在抓取对齐、放置精度，或语义规划器已经选对对象后仍发生碰撞的团队。OpenSPM 报告在 10 个 LIBERO-GOAL 任务上成功率为 85.6%，动作块生成延迟为 4.8 ms，动作模型参数量为 0.24M。一个低成本检查是：从某一类抓取-放置任务的少量成功示范中提取对象相对姿态，在对象位置改变后回放，并测量抓取和放置附近的姿态误差。

### Evidence
- [OpenSPM: An Environment-Transferable Robotic Key Spatial Pose Memory and Closed-Loop High-Frequency Flow-Matching Action Generation Model](../Inbox/2026-06-29--openspm-an-environment-transferable-robotic-key-spatial-pose-memory-and-closed-loop-high-frequency-flow-matching-action-generation-model.md): 描述了从示范中存储对象相对 SE(3) 关键姿态、结合 6D 对象姿态估计进行迁移，并报告了 LIBERO-GOAL 成功率和延迟结果。
