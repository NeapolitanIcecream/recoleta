---
kind: ideas
granularity: day
period_start: '2026-05-20T00:00:00'
period_end: '2026-05-21T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D perception
- dexterous hands
- world models
- robot evaluation
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-perception
- topic/dexterous-hands
- topic/world-models
- topic/robot-evaluation
language_code: zh-CN
---

# 操作策略硬件检查

## Summary
机器人策略团队已经有足够细节，可以把三个实用检查加入工作流：低成本的物理 VLA 回归工位、和动作预测绑定的 3D 几何监督，以及面向灵巧手的直接关节传感测试。它们分别针对操作中的三个可见失效模式：实验室结果在真实接触下失效、动作解码器漏掉几何信息，以及依赖脆弱外部感知的手部控制器。

## 用于 VLA 策略发布的低成本物理回归工位
VLA 团队可以在发布流程里加一个小型真实机器人工位，把它当作持续回归测试。VLA-REPLICA 给出了一套具体的物料清单和流程：SO-101 6 自由度机械臂、RealSense D455 顶置相机、腕部摄像头、灯箱、现成物体、AprilTag 对齐、固定照明、参考图像和预定义物体摆放。整套配置的成本约为 1050 美元，有一位用户在不到一小时内搭建完成。

有用的采用变化，是在宣布新策略或微调有进展之前先过一个固定的本地门槛。跑同样的 10 个操作任务，复用 500 条示范组成的适配集，并在 50 个分布内场景和 40 个分布外场景上报告成功率。基线表也给出了预期：π0.5 在分布内测试中以 0.54 的平均成功率领先，ACT、DiT 变体、SmolVLA、X-VLA 和 π0 都更低。拿到新 VLA 的团队可以很快看出，排行榜上的提升在真实硬件上遇到光照、相机位姿、物体摆放和接触时是否还成立。

### Evidence
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA specifies the low-cost hardware, 10-task suite, 500 demonstrations, 90 test scenes, reproducibility check, and policy success rates.
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): The paper describes the motivation for a locally executable real-world benchmark and gives the accessible hardware setup.

## VLA 动作预测中的 3D 几何检查
在 RGB-D 操作数据上训练 VLA 的团队，可以通过加入显式的 3D 路径并衡量对接触敏感失败的影响，来检查几何信息是否进入了动作输出。PointACT 给出了一种实现方式：用 Point Transformer v3 编码彩色点云，让动作 token 在多尺度上关注局部点窗口，再在解码时把几何信息和 VLM 特征结合起来。GaussianDream 给出另一种测试方式：在训练阶段加入 3D 高斯重建和短时域场景流预测，在推理时去掉这些辅助头，只保留学到的前缀 token 生成动作。

实际检查可以做成一次受控消融，覆盖空间任务和长时程厨房任务。固定基础 VLA 和训练数据，只在解码器里加入点云注意力，或者加入 3D 高斯辅助监督，然后比较抓取点、目标姿态、堆叠、拆堆叠和空间关系上的误差。PointACT 在 LIBERO 上报告了 96.0% 的平均成功率，并且在同一张表里比 SpatialVLA 高 17.9 个百分点。GaussianDream 在 LIBERO 上报告 98.4%，在 RoboCasa Human-50 上报告 52.6%，同时避免了测试时的高斯渲染和未来视频展开。

### Evidence
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT describes point-cloud features connected directly to action tokens and reports LIBERO results and the SpatialVLA comparison.
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream describes training-time 3D Gaussian reconstruction, future scene-flow supervision, inference-time removal of auxiliary heads, and reported LIBERO and RoboCasa results.

## 面向 tendon-driven 灵巧手的直接关节传感评估
使用 tendon-driven 硬件的灵巧手团队，可以先做一次有针对性的传感升级，再考虑增加更多摄像头或触觉传感器。具体测试是安装直接关节角传感，基于关节位置和速度历史训练学生控制器，并在连续立方体旋转任务上与只用电机编码器和基于视觉的基线比较。Proprioceptive Transformer 先在 Isaac Lab 里用带特权物体位姿的教师策略训练，然后把控制蒸馏成一个接收关节历史、上一动作、上一指令和目标指令的策略。

论文里的硬件结果说明，这个检查值得在真实手上做。对 55 毫米立方体，直接关节感知的策略达到 11.83 RPM，旋转准确率 100%，无掉落成功率 100%，在 3 次各 60 秒的试验里没有一次掉落。同一篇论文还报告，在 55 毫米立方体上，直接关节感知版本比电机编码器版本快 26.8%。对于正在处理缆线伸长、回差、遮挡和相机标定问题的团队，这是一项可以量化的改造：加直接关节感知，训练历史模型，然后用 RPM、掉落次数和旋转准确率去对比现有控制器。

### Evidence
- [Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer](../Inbox/2026-05-20--learning-robust-dexterous-in-hand-manipulation-from-joint-sensors-with-proprioceptive-transformer.md): Proprioceptive Transformer specifies the joint-history student policy, direct joint sensing on the ORCA hand, and the cube-rotation results against baselines.
- [Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer](../Inbox/2026-05-20--learning-robust-dexterous-in-hand-manipulation-from-joint-sensors-with-proprioceptive-transformer.md): The abstract frames joint-only dexterous manipulation and the teacher-student design using only joint sensing feedback.
