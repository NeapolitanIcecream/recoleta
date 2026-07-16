---
kind: ideas
granularity: day
period_start: '2026-05-27T00:00:00'
period_end: '2026-05-28T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- manipulation
- tactile sensing
- model compression
- autonomous driving safety
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/tactile-sensing
- topic/model-compression
- topic/autonomous-driving-safety
language_code: zh-CN
---

# 机器人策略部署基准

## 摘要
机器人团队可以直接测试部署门槛：4 位策略压缩、面向力的操作评分，以及带原语标签的长时程微调，在所引论文中都有明确的评测方案。

## W4A4 机器人 VLA 策略验收测试
试图把 Pi 0.5 或 GR00T 级策略部署到机器人本体附近的机器人团队，应在购买更多推理硬件前先加一项 4 位策略验收测试。测试很具体：把语言主干和扩散动作头量化到统一的 W4A4，在一小批无标注轨迹上校准 DiT 激活尺度，然后在团队的操作任务集上和 FP16 策略对比。

Ω-QVLA 报告 Pi 0.5 的 W4A4 平均 LIBERO 成功率为 98.0%，FP16 为 97.1%；GR00T N1.5 的 W4A4 为 87.8%，FP16 为 87.0%，静态内存占用减少 71.3%。实际门槛应包括任务成功率、动作平滑性、内存占用和真实机器人进展，因为同一篇论文还报告了 ARX R5 双臂的进展接近 FP16，而且明显优于 QuantVLA。

### 资料来源
- [Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling](../Inbox/2026-05-27--o-qvla-robust-quantization-for-vision-language-action-models-via-composite-rotation-and-per-step-scaling.md): Ω-QVLA reports uniform W4A4 quantization of both language backbone and DiT action head, near-FP16 LIBERO success, 71.3% static memory reduction, and real ARX R5 progress results.
- [Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling](../Inbox/2026-05-27--o-qvla-robust-quantization-for-vision-language-action-models-via-composite-rotation-and-per-step-scaling.md): The paper abstract reports 98.0% and 87.8% success rates while reducing static memory footprint by 71.3%.

## 用于轻柔操作 rollout 的接触力指标
处理易碎、易滑或可变形物体的操作团队，应把接触力指标加入 rollout 评估。一个有用的评分表要记录每次任务尝试的瞬时最大抓取力、平均抓取力、瞬时最大施加力和平均施加力，并区分像“轻轻地”和“用力地”这样的语言条件运行。

Tabero 通过在 Isaac Lab 里回放带触觉感知的操作轨迹，记录 GelSight 风格的触觉图像、标记位移网格和指尖力，然后把预测的位姿和力目标送入混合控制器，展示了这条数据路径。它报告在“轻轻地”指令下，平均抓取力降低了 70% 以上。CoP 为灵巧手补了一条配套路径：把触觉表示成每个触觉区域的三维接触力和三维接触位置，然后在仿真中训练。在真实的孔插入任务中，CoP 在六种形状上的成功率达到 0.78，而原始 taxel 为 0.48，二值接触为 0.53。一次 rollout 可以完成任务，但仍然超出接触力上限。

### 资料来源
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): Tabero defines the force-control problem, simulated tactile data pipeline, hybrid controller, and four contact-quality metrics.
- [Tabero: Learning Gentle Manipulation with Closed-Loop Force Feedback from Vision, Touch, and Language](../Inbox/2026-05-27--tabero-learning-gentle-manipulation-with-closed-loop-force-feedback-from-vision-touch-and-language.md): The abstract states that Tabero reduces average grip force by over 70% under gentle instructions while maintaining high task success.
- [Beyond Binary: Sim-to-Real Dexterous Manipulation with Physics-Grounded Contact Representation](../Inbox/2026-05-27--beyond-binary-sim-to-real-dexterous-manipulation-with-physics-grounded-contact-representation.md): CoP reports a compact tactile representation and real peg-in-hole success gains over raw taxels and binary contact.

## 用于长时程 VLA 演示的原语标签和切换规则
拥有任务级演示的机器人数据团队，可以在 VLA 微调前加一个离线的原语标注步骤。流程很明确：先在 Grasp、Place、Lift、Move、Push、Pull、Insert、Press、Twist、Tilt 和 Rotate 这些原语上推断序列；再为这些片段生成基于状态的边界规则；用 SAM 和 Cutie 跟踪物体掩码；用规范化的原语指令训练 VLA；执行时再用规划器和状态历史切换规则。

PrimitiveVLA 在“记住整段演示”最吃亏的地方给出了大幅提升。OpenVLA 在 LIBERO-90-Novel 上从 7.38% 提升到 45.50%；OpenVLA-OFT 在 LIBERO-Long 上从 3.75% 提升到 66.50%；pi0.5 在 LIBERO-Long 上从 30.50% 提升到 80.25%。一个便宜的检查方式，是用相同演示预算留出一组新的物体-技能配对和长时程任务。

### 资料来源
- [PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation](../Inbox/2026-05-27--primitivevla-learning-reusable-motion-primitives-for-efficient-and-generalizable-robotic-manipulation.md): PrimitiveVLA describes the 11 primitives, automated boundary detection, object-centric masks, test-time primitive planning, and LIBERO gains.
- [PrimitiveVLA: Learning Reusable Motion Primitives for Efficient and Generalizable Robotic Manipulation](../Inbox/2026-05-27--primitivevla-learning-reusable-motion-primitives-for-efficient-and-generalizable-robotic-manipulation.md): The paper explains why task-level demonstrations are segmented into shared task-agnostic motion patterns such as Grasp and Pull.
