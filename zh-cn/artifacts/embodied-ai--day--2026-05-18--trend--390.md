---
kind: trend
trend_doc_id: 390
granularity: day
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-19T00:00:00'
topics:
- embodied AI
- robot manipulation
- VLA models
- dexterous robotics
- world models
- robot benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-390
tags:
- recoleta/trend
- topic/embodied-ai
- topic/robot-manipulation
- topic/vla-models
- topic/dexterous-robotics
- topic/world-models
- topic/robot-benchmarks
language_code: zh-CN
---

# 具身 AI 论文把真实机器人执行变成了主要测试

## 概览
这一时期的具身 AI 工作主要把策略当成可部署的机器人系统来处理。视觉语言动作（VLA）模型被放到灵巧手、受污染的摄像头、双臂任务和接触密集的世界模型基准上测试。Dexora、StableVLA 和 WorldArena 2.0 定下了基调：成功率、真实物理滚动、触觉信号和迁移测试，比干净的仿真分数更重要。

## 研究发现

### 灵巧操作正在进入真实手和桌面
Dexora 是这组里最强的执行结果。它把两条 6-DoF 机械臂、两只 12-DoF 灵巧手、一个对应的 MuJoCo 数字孪生、10 万条仿真轨迹和 1 万段真实遥操作数据放在一起。它在 12 个基础真实任务上的平均成功率为 89.6%，在 6 个灵巧任务上的平均成功率为 66.7%，把高 DoF 双臂控制放到了这一时期的核心位置。

DexHoldem  পরীক্ষা的是另一种失败模式：一个灵巧系统在处理扑克牌和筹码时，能否让不断变化的桌面场景继续可用。这个基准包含 1,470 条遥操作示范，覆盖 14 个原语，并同时评估任务完成和场景保持。最佳策略的任务完成率为 61.2%，场景保持成功率最高只有 47.5%，说明即使在紧凑的桌面场景里，精细操作和状态安全执行仍然很难。

#### 资料来源
- [Dexora: Open-source VLA for High-DoF Bimanual Dexterity](../Inbox/2026-05-18--dexora-open-source-vla-for-high-dof-bimanual-dexterity.md): Dexora hardware, data scale, and real-world success rates.
- [DexHoldem: Playing Texas Hold'em with Dexterous Embodied System](../Inbox/2026-05-18--dexholdem-playing-texas-hold-em-with-dexterous-embodied-system.md): DexHoldem benchmark design and real primitive execution results.

### VLA 可靠性正在通过记忆和视觉容错改进
Key-Gram 和 StableVLA 针对 VLA 策略的两个实际弱点。Key-Gram 把可复用的指令知识放在主干网络外部，检索像物体关系和子目标这样的短“key-grams”，再把它们注入到选定的 Transformer 层。报告中的提升范围很广：pi0-KG 把 RoboTwin2.0 的难任务成功率从 58.4% 提高到 75.6%，把真实长时程双臂任务成功率从 69.3% 提高到 80.0%。

StableVLA 处理的是差的摄像头输入。它把视觉投影器换成 Information Bottleneck Adapter，通过一条并行路径保留空间细节，同时压制噪声特征通道。论文没有加入额外机器人数据，也没有做针对腐蚀的增强，但在 severity-5 的 LIBERO 上给出了明显提升，例如 Object 任务从 29.3% 提高到 70.2%，Long 任务从 26.2% 提高到 45.3%。

#### 资料来源
- [Key-Gram: Extensible World Knowledge for Embodied Manipulation](../Inbox/2026-05-18--key-gram-extensible-world-knowledge-for-embodied-manipulation.md): Key-Gram memory mechanism and success-rate gains across RoboTwin2.0, LIBERO-Plus, and real dual-arm tasks.
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): StableVLA adapter design and corruption-tolerance results.

### 世界模型按接触、控制用途和物理结构来评判
WorldArena 2.0 把世界模型评估从视频预测扩展出去。它加入了视觉触觉感知、在学得动力学内进行强化学习，以及真实机器人平台测试。UniVTAC 的结果有好有坏：Wan2.2 的触觉质量最好，PSNR 为 21.26、SSIM 为 0.746，但在 Insert HDMI 和 Lift Bottle 两个任务上的平均成功率只有 50%。好的触觉重建并不保证控制就有用。

WorldString 和 PH-Dreamer 从不同层面处理物理结构。WorldString 通过稀疏状态关键点预测占据的 3D 形状，并在 4 个可动对象上报告 86.61 的平均 IoU。PH-Dreamer 用 Port-Hamiltonian 能量动力学约束潜在滚动，在 6 个 DeepMind Control 视觉任务上报告 789.2 的平均回报，超过 DreamerV3 和 R2Dreamer，同时相空间体积更小，动作统计也更平滑。

#### 资料来源
- [WorldArena 2.0: Extending Embodied World Model Benchmarking on Modality, Functionality and Platform](../Inbox/2026-05-18--worldarena-2-0-extending-embodied-world-model-benchmarking-on-modality-functionality-and-platform.md): WorldArena 2.0 modalities, RL-in-world-model evaluation, and tactile/task results.
- [WorldString: Actionable World Representation](../Inbox/2026-05-18--worldstring-actionable-world-representation.md): WorldString controllable 3D object representation and reconstruction metrics.
- [PH-Dreamer: A Physics-Driven World Model via Port-Hamiltonian Generative Dynamics](../Inbox/2026-05-18--ph-dreamer-a-physics-driven-world-model-via-port-hamiltonian-generative-dynamics.md): PH-Dreamer physical regularization and DeepMind Control results.

### 具身记忆正在变成动作机制，而不只是日志
两篇论文把记忆当成控制输入，而不是被动记录。Key-Gram 检索可复用的语言先验来做操作控制，Robo-Cortex 则把导航过程转成自然语言启发式，给后续规划提供指引。Robo-Cortex++ 在推理时更新启发式库，然后报告 IGNav 成功率为 45.07，高于 World-In-World 的 38.57，并把 IGNav SPL 提高到 35.06。

更关键的是记忆如何被使用。Robo-Cortex 会预测短期未来视觉结果，用视觉语言模型评估候选动作，再把最近的失败摘要和检索到的长期原则反馈回去。文中给出的启发式迁移表对导航很有用：IGNav SPL 从基础流程的 24.03 提高到迁移启发式后的 39.33。

#### 资料来源
- [Robo-Cortex: A Self-Evolving Embodied Agent via Dual-Grain Cognitive Memory and Autonomous Knowledge Induction](../Inbox/2026-05-18--robo-cortex-a-self-evolving-embodied-agent-via-dual-grain-cognitive-memory-and-autonomous-knowledge-induction.md): Robo-Cortex memory design, online heuristic induction, and navigation gains.
- [Key-Gram: Extensible World Knowledge for Embodied Manipulation](../Inbox/2026-05-18--key-gram-extensible-world-knowledge-for-embodied-manipulation.md): Key-Gram external language memory used inside VLA manipulation policies.
