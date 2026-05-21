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

## Summary
近期机器人学习论文给部署工作提供了具体检查项：用低成本遥操作和可直接训练的日志收集 VLA 演示；在灵巧手迁移前，用真实图像校准仿真随机化；在 rollout 期间，用子目标进展检查包住长时程策略。

## 用于 VLA 微调的手机遥操作和 LeRobot 格式记录
小型机器人实验室可以把遥操作接口和数据格式纳入模型测试。Phone2Act 给出了一种可执行的做法：Android 手机通过 ARCore 以 50 Hz 发布 6-DoF 位姿和按钮事件，ROS 2 将这些事件映射为机器人目标位姿，针对具体机器人的桥接节点处理最后的 API 调用。记录器以 20 Hz 将同步的 RGB 帧、关节状态、末端执行器位姿和夹爪状态写入 LeRobot 格式的 MP4 和 Parquet 文件。

一个有用的采用检查是：为本地机械臂构建一个桥接节点，在单个操作任务上收集约 100 到 150 个 episode，用高速视频测量手机到执行机构的延迟，并微调一个现有 VLA checkpoint。Phone2Act 报告收集了 130 个 episode，微调了 GR00T-N1.5-3B，并在 Dobot CR5 球入篮任务的 10 次试验中成功 9 次，端到端延迟为 350–440 ms。VILAS 在低成本操作系统上给出相近的工程路线：它使用一套 $8,000 的机械臂、夹爪、双 RealSense 相机、遥操作和软夹爪扩展，并在真实葡萄抓取任务上比较 pi_0、pi_0.5 和 GR00T N1.6 的延迟与连续抓取结果。

### Evidence
- [Phone2Act: A Low-Cost, Hardware-Agnostic Teleoperation System for Scalable VLA Data Collection](../Inbox/2026-05-03--phone2act-a-low-cost-hardware-agnostic-teleoperation-system-for-scalable-vla-data-collection.md): Phone2Act 详细说明了手机遥操作栈、ROS 2 桥接模式、LeRobot 格式记录、延迟、数据量和 Dobot 成功结果。
- [VILAS: A VLA-Integrated Low-cost Architecture with Soft Grasping for Robotic Manipulation](../Inbox/2026-05-03--vilas-a-vla-integrated-low-cost-architecture-with-soft-grasping-for-robotic-manipulation.md): VILAS 用一套 $8,000 的 VLA 操作系统、遥操作数据、软夹爪硬件和真实抓取指标，支撑了低成本硬件这一方向。

## 用于灵巧手迁移的 VLM 评分仿真随机化
灵巧操作团队可以在仿真训练策略之前加入一个评分循环：渲染候选随机化场景，用 VLM 真实感分数把它们与真实参考图像比较，并优化光照、纹理、质量、摩擦、相机位姿和传感器噪声上的随机化分布。DexSim2Real 使用 GPT-4V 作为视觉真实感评判器，并用 CMA-ES 优化仿真参数。

具体测试可以是每个任务做一次小规模校准：采集真实参考图像，运行 200–300 次 VLM 查询，检查真实感分数是否上升，然后用调好的随机化和基线随机化分别训练同一个策略。DexSim2Real 报告 VLM 真实感分数从 4.2/10 升至 7.8/10，摩擦均值误差从 0.35 降至 0.08，并增加约 2 GPU-hours 的开销。在六个 Franka Panda 和 Allegro Hand 任务上，它报告平均真实世界成功率为 78.2%，平均 sim-to-real 差距为 8.3%，而普通 domain randomization 为 28.5%，active domain randomization 为 19.2%。

### Evidence
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): 摘要给出了 FM-DR 方法、被优化的仿真参数、查询和额外开销、真实世界成功率，以及 sim-to-real 差距对比。
- [DexSim2Real: Foundation Model-Guided Sim-to-Real Transfer for Generalizable Dexterous Manipulation](../Inbox/2026-05-03--dexsim2real-foundation-model-guided-sim-to-real-transfer-for-generalizable-dexterous-manipulation.md): 论文正文说明了灵巧操作迁移中的 78.2% 真实世界成功率和 8.3% sim-to-real 差距。

## 用于长时程 VLA rollout 的进展门控子目标监督
测试长时程 VLA 策略的团队可以在策略外加一个监督器，用来维护活动目标、提出可达的文本和图像子目标，并在执行步骤后检查 rollout 进展。Anticipation-VLA 给出了一种具体设计：高层模型生成下一个子目标，逆动力学检查拒绝文本和图像不匹配的子目标，价值模型将 rollout 分类为已达成、正在改进或停滞。这个状态决定系统是继续执行、细化子目标，还是弹出已完成的目标。

低成本验证路径是：在 Libero-Long 或本地多阶段任务上，用同一个基础策略分别搭配和不搭配监督器运行，然后记录停滞发生的位置，以及递归子目标细化是否能恢复执行。Anticipation-VLA 报告在 Libero-Long 上成功率为 63.2，高于底层 pi_0.5-style 策略的 54.6 和 VLM-assisted 版本的 53.2。在 Arx-X5 真实世界测试中，论文报告它在已见和未见配置上都超过基线，未见设置中的增幅更大。

### Evidence
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): 摘要说明了目标栈、子目标生成、逆动力学检查、进展价值模型、Libero-Long 分数和真实世界增益。
- [Anticipation-VLA: Solving Long-Horizon Embodied Tasks via Anticipation-based Subgoal Generation](../Inbox/2026-05-03--anticipation-vla-solving-long-horizon-embodied-tasks-via-anticipation-based-subgoal-generation.md): 论文摘要说明了长时程误差累积问题，以及自适应递归子目标生成方法。
