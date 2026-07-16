---
kind: ideas
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- world models
- robot evaluation
- multimodal sensing
- policy adaptation
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/world-models
- topic/robot-evaluation
- topic/multimodal-sensing
- topic/policy-adaptation
language_code: zh-CN
---

# 机器人策略就绪检查

## 摘要
机器人团队可以先加入执行前检查，让混合机器人训练数据更容易合并，并在上硬件前用能力级诊断测试策略。证据中的具体收益来自推理时动作验证、跨具身形态的状态-动作对齐，以及能暴露总体成功率所掩盖失败的基准测试。

## VLA rollout 的执行前动作验证和不确定性日志
运行 π0 风格或其他随机式 VLA 策略的机器人团队，可以加一个小型运行时层：采样多个短动作片段，在运动前打分，执行得分最高的候选，并把被拒绝的候选连同最终结果一起记录。VERITAS 给出了最具体的做法：生成 N 个候选片段，使用与像素空间路标点绑定的视觉验证器，并保留成功的已验证 rollout，用于后续行为克隆微调。论文报告的设置使用 N = 5、15 Hz 控制；在一次性生成 VLM 轨迹后，几何验证开销低于 1 ms。

这适合一种操作工位：错误的第一次动作代价高，但多采样几次策略很便宜。同一个日志层还可以加入基于流的 VLA 的速度场分歧，把不确定的起始状态送入专家示范队列。这样，部署遥测会变成一份分流清单：成功的已验证 rollout 成为自训练数据，高分歧案例成为下一批需要收集的示范。

### 资料来源
- [Visual Verification Enables Inference-time Steering and Autonomous Policy Improvement](../Inbox/2026-06-16--visual-verification-enables-inference-time-steering-and-autonomous-policy-improvement.md): VERITAS 会采样短动作片段，在执行前用视觉方式验证，报告了跨策略的成功率提升，并记录已验证 rollout 用于微调。
- [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](../Inbox/2026-06-16--uncertainty-quantification-for-flow-based-vision-language-action-models.md): 这篇不确定性论文使用基于流的 VLA 动作头集成之间的速度场分歧，用于失败检测和主动微调案例选择。

## 多机器人操作数据集的规范化状态-动作模板
如果团队的示范数据分散在 Franka、UR、ALOHA、ARX 或类似机械臂上，就应把数据格式化当作模型训练的一部分。Qwen-RobotManip 将不同机器人映射到一个状态-动作模板，对缺失的关节或夹爪使用逐维二值掩码，预测相机坐标系下的末端执行器增量位姿，并把最近的执行历史作为当前具身形态的线索。

可以先做一个数据集适配器，在预训练或微调前把每个机器人日志转换到共享 schema。低成本验证可以用两到三个机器人系列训练，留出一个具身形态，再把零样本迁移和少样本适应结果与逐机器人动作编码进行比较。Qwen-RobotManip 报告了一个 38,100 小时语料库，并在 AgileX ALOHA、Franka、UR 和 ARX 上做了真实机器人验证，因此这些 schema 选择已经具体到足够让小型实验室复用。

### 资料来源
- [Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models](../Inbox/2026-06-16--qwen-robotmanip-technical-report-alignment-unlocks-scale-for-robotic-manipulation-foundation-models.md): Qwen-RobotManip 描述了规范化状态-动作对齐、二值掩码、相机坐标系下的末端执行器增量动作、执行历史条件输入、38,100 小时语料库，以及跨多个平台系列的真实机器人验证。
- [Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models](../Inbox/2026-06-16--qwen-robotmanip-technical-report-alignment-unlocks-scale-for-robotic-manipulation-foundation-models.md): 源文本称，该系统使用开源机器人数据集和人类示范视频构建了约 38,100 小时语料库，并在 15 个平台上进行从人到机器人的合成。

## 通用操作策略的能力级验收测试
选择通用操作策略的实验室，应加入一张部署前测试表，按任务类型、精度、时域长度、运行模式和分布偏移拆分成功率。EBench 说明了原因：π0、π0.5、XVLA 和 InternVLA-A1 的总体测试成功率都落在 24.4% 到 29.5% 的接近区间内，但 InternVLA-A1 虽然在移动操作上更强，在灵巧固定基座任务上的成功率却降到 5.8%。

处理线束或电缆的工业团队还需要额外的富接触测试。WireCraft 显示，特权状态 RL 可以在仿真中解决以太网连接器插入，State PPO 的插入成功率为 95.86%；但同一任务中 Vision PPO 的插入成功率为 17.74%，仅使用仿真数据的 ACT 在报告的真实 UR5 运行中为 0/10 次插入。验收测试应包含 reach、align、insert、route 和 seat 等分阶段指标，这样，能到达端口但接触对齐失败的策略会在硬件试验前被发现。

### 资料来源
- [EBench: Elemental Diagnosis of Generalist Mobile Manipulation Policies](../Inbox/2026-06-16--ebench-elemental-diagnosis-of-generalist-mobile-manipulation-policies.md): EBench 定义了能力轴和泛化偏移，并报告了接近的总体成功率；这些总体数字会掩盖通用策略之间很大的技能画像差异。
- [WireCraft: A Simulation Benchmark for Industrial DLO Manipulation](../Inbox/2026-06-16--wirecraft-a-simulation-benchmark-for-industrial-dlo-manipulation.md): WireCraft 报告了特权状态 RL 与基于视觉的策略在工业线束和连接器任务上的巨大差距，包括真实 UR5 插入结果。
