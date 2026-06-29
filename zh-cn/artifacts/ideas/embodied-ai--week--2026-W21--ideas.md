---
kind: ideas
granularity: week
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-25T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D grounding
- spatial memory
- real-world evaluation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-grounding
- topic/spatial-memory
- topic/real-world-evaluation
language_code: zh-CN
---

# 实体 VLA 策略验证

## Summary
VLA 团队可以加入小型实体回归基准、目标状态日志和 RGB-D 几何路径，用来检查操作策略在真实控制条件下是否仍能工作。

## 用于 VLA 策略发布的本地真实机器人回归基准
VLA 实验室可以把小型实体基准纳入每次策略发布：重建同一套 SO-101 机械臂配置，运行固定的一组操作任务，并发布分布内和分布外场景的逐任务成功率。VLA-REPLICA 给出的细节足够支撑这套流程落地：SO-101 6-DoF 机械臂、RealSense D455 顶部相机、腕部网络摄像头、32 英寸灯箱、通用物体、相机叠加工具、AprilTag 对齐、固定照明、参考图像和预定义摆放位置。论文报告的搭建成本约为 $1050，一名新用户在不到一小时内完成了组装。

有用的检查很直接：在同一批 500 条专家演示上训练或微调，运行 90 个已定义测试场景，并与已报告的基线比较，例如 π₀.₅ 在 10 个分布内任务上的平均成功率为 0.54。这样，机器人团队在声称某个 VLA 策略能在仿真外工作前，可以先通过一个低成本实体关卡。

### Evidence
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA 描述了低成本硬件配置、500 条演示、90 个测试场景、可复现工具、搭建时间和基线成功率。
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): 论文说明了可在本地执行的真实世界评估动机，并列出了易获得的现成组件。

## 机器人动作预测前记录目标状态 token
处理密集棋盘、料箱或物体布局的操作团队，应要求策略在预测动作前暴露目标状态。AVP 给出了一种具体做法：VLM 预测点、框、掩码或记忆原语等视觉原语，将它们投影到视觉 token 空间，并用它们调节一个流匹配动作专家。标签来自通过相机标定得到的末端执行器运动学，因此团队可以在不为每个目标提示手工标注的情况下生成监督信号。

这也能给开发者更好的失败日志。一次运行失败时，他们可以检查模型选错了物体、选了不合适的放置区域，还是在目标正确后生成了较差的电机序列。AVP 在中国象棋操作上的平均成功率为 90.28%，π₀.₅ 为 62.67%，每条指令耗时 0.27 秒。SOMA 指向部分可见场景中的同一类运行需求：带有语义和 3D 位置数据的持久物体记忆缩短了五个视野外任务的抓取用时，并在其真实世界消融中把平均成功率提高到 28.3%。

### Evidence
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP 报告了动作预测前的视觉原语 token、由标定得到的监督信号、推理时不使用外部在线检测器或 VLM API，以及相对 π₀.₅ 的真实机器人提升。
- [Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action](../Inbox/2026-05-21--spatial-memory-for-out-of-vision-manipulation-in-vision-language-action.md): SOMA 展示了当前视野外物体的持久空间记忆，并给出了真实世界成功率、首次注视时间、搜索路径、抓取尝试次数和抓取用时结果。

## 用于精确操作的动作解码器内 RGB-D 几何信息
配有 RGB-D 相机的团队可以测试几何信息是否应进入动作路径，而不只放在感知预处理器中。PointACT 给出了一种直接的构建方式：用 Point Transformer v3 编码彩色点云，让动作 token 在多个尺度上关注局部点窗口，再把这些受几何条件影响的动作 token 与 VLM 特征结合。论文报告的 LIBERO 平均成功率为 96.0%，其中包括在引用表格中相对 SpatialVLA 的 17.9 个百分点提升。

GaussianDream 为想要几何监督但不想增加推理模块的团队提供了训练阶段方案。它在训练时把学到的前缀 token 解码为当前 3D Gaussian 场景和短时域未来 Gaussian 运动，并使用 RGB 渲染、深度和伪 3D 场景流损失。推理时，Gaussian 头被移除，策略只保留学到的前缀 token。论文报告 LIBERO 平均成功率为 98.4%，RoboCasa Human-50 为 52.6%，真实机器人评估为 50.0%。一个有用的采用测试是比较加入点-动作注意力或训练阶段 3D 监督前后的抓取点失败和空间关系失败。

### Evidence
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT 描述了动作 token 与多尺度点云的直接交互，并报告了相对 SpatialVLA 和 EO1 的 LIBERO 提升。
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream 描述了训练阶段 3D Gaussian 重建和未来预测、推理时只使用前缀 token，以及在 LIBERO、RoboCasa Human-50 和真实机器人上的结果。
