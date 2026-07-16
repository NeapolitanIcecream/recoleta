---
kind: ideas
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- VLA
- sim-to-real
- teleoperation
- world models
- planning security
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vla
- topic/sim-to-real
- topic/teleoperation
- topic/world-models
- topic/planning-security
language_code: zh-CN
---

# 机器人学习部署检查

## 摘要
近期机器人学习论文给出了可直接用于部署工作的测试方法：用低成本遥操作和可训练的数据日志采集 VLA 示范，在灵巧手迁移前用真实图像校准仿真随机化，并在 rollout 期间用子目标进度检查包住长时程策略。

## 基于手机的遥操作与 LeRobot 格式记录，用于 VLA 微调
小型机器人实验室可以把遥操作界面和数据格式当作模型测试的一部分。Phone2Act 给出了一种可落地的做法：Android 手机通过 ARCore 以 50 Hz 发布 6 自由度位姿和按键事件，ROS 2 把这些事件映射为机器人目标位姿，针对具体机器人的桥接节点再处理最后的 API 调用。记录器以 20 Hz 将同步的 RGB 帧、关节状态、末端执行器位姿和夹爪状态写入 LeRobot 格式的 MP4 和 Parquet 文件。

一个有用的接入检查是：为本地机械臂做一个桥接节点，在单个操作任务上采集大约 100 到 150 段 episode，用高速视频测量手机到执行的延迟，并在现有 VLA 检查点上做微调。Phone2Act 报告采集了 130 段 episode，完成了 GR00T-N1.5-3B 微调，并在 Dobot CR5 的球入篮任务上 10 次试验取得 9 次成功，端到端延迟为 350–440 ms。VILAS 在低成本操作系统上给出同样的实践方向：它使用一台 8,000 美元的机械臂、夹爪、双 RealSense 相机、遥操作和软夹爪扩展，然后在真实的葡萄抓取任务上比较 pi_0、pi_0.5 和 GR00T N1.6 的延迟和连续抓取结果。

### 资料来源
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Phone2Act details the phone teleoperation stack, ROS 2 bridge pattern, LeRobot-format recording, latency, data volume, and Dobot success result.
- [VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation](../Inbox/2026-05-03--vilas-a-vla-integrated-low-cost-architecture-with-soft-grasping-for-robotic-manipulation.md): VILAS supports the low-cost hardware angle with an $8,000 VLA manipulation setup, teleoperation data, soft gripper hardware, and real grasping metrics.

## 用 VLM 评分的仿真随机化，用于灵巧手迁移
灵巧操作团队可以在仿真训练策略前加一个评分循环：渲染候选随机场景，用 VLM 真实感分数和真实参考图像比较，再对光照、纹理、质量、摩擦、相机位姿和传感器噪声的随机化分布做优化。DexSim2Real 用 GPT-4V 作为视觉真实感评审，并用 CMA-ES 优化仿真参数。

具体测试是每个任务做一次小规模校准：采集真实参考图像，运行 200–300 次 VLM 查询，检查真实感分数是否上升，然后用调好的随机化和基线随机化分别训练同一个策略。DexSim2Real 报告 VLM 真实感分数从 4.2/10 提升到 7.8/10，摩擦平均误差从 0.35 降到 0.08，额外开销约 2 个 GPU 小时。在 6 个 Franka Panda 和 Allegro Hand 任务上，它报告真实世界平均成功率为 78.2%，平均 sim-to-real 差距为 8.3%，而普通 domain randomization 为 28.5%，active domain randomization 为 19.2%。

### 资料来源
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): The summary gives the FM-DR method, optimized simulation parameters, query and overhead costs, real-world success rate, and sim-to-real gap comparisons.
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): The paper text states the 78.2% real-world success rate and 8.3% sim-to-real gap claim for dexterous manipulation transfer.

## 带进度门控的子目标监督，用于长时程 VLA rollout
测试长时程 VLA 策略的团队可以在策略外面包一层监督器，让它维护当前目标，提出可达的文本和图像子目标，并在执行步骤后检查 rollout 进度。Anticipation-VLA 给出了一种具体设计：高层模型生成下一个子目标，逆动力学检查拒绝不匹配的文本-图像子目标，价值模型把 rollout 标成已完成、在改进或停滞。这个状态决定系统是继续执行、细化子目标，还是弹出已完成目标。

一个低成本验证路径是在 Libero-Long 或本地多阶段任务上分别启用和关闭监督器运行同一个基础策略，然后记录停滞发生的位置，以及递归子目标细化是否能恢复。Anticipation-VLA 在 Libero-Long 上报告 63.2 的成功率，高于底层 pi_0.5 风格策略的 54.6 和带 VLM 的版本的 53.2。在 Arx-X5 的真实世界测试中，论文报告在已见和未见配置上都超过了基线，且未见配置上的提升更大。

### 资料来源
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): The summary specifies the goal stack, subgoal generation, inverse dynamics check, progress value model, Libero-Long score, and real-world gains.
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): The paper abstract states the long-horizon compounding-error problem and adaptive recursive subgoal generation approach.
