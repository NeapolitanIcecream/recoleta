---
kind: trend
trend_doc_id: 590
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
topics:
- robot manipulation
- VLA policies
- real-robot evaluation
- occlusion
- dexterous manipulation
- sim-real correlation
run_id: materialize-outputs
aliases:
- recoleta-trend-590
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vla-policies
- topic/real-robot-evaluation
- topic/occlusion
- topic/dexterous-manipulation
- topic/sim-real-correlation
language_code: zh-CN
---

# 机器人操作论文正在用真实失败模式检验策略

## Overview
这个时间窗口里的机器人研究集中在让操作结论经得起真实执行。LIBERO-Occ、UMI-Bench 1.0 和 Dexterous Point Policy 说明了重点：隐藏物体、真实轨迹协议，以及机器人数据稀缺。

## Clusters

### 遮挡和物理基准暴露了操作策略的脆弱性
几篇论文收紧了视觉-语言-动作（VLA）机器人策略的评测，其中 VLA 指把语言和视觉输入映射到机器人动作。LIBERO-Occ 新增了 2,000 个被遮挡的 LIBERO 任务，并报告当任务物体或容器被遮住时，成绩大幅下降。VIM 通过生成一个互补的手腕或夹爪视角挽回部分损失，在没有真实额外视角的情况下把平均成功率做到 65.05%。

UMI-Bench 1.0 为通用操作接口（Universal Manipulation Interface）策略提供了真实机器人桌面基准，包含固定重置、手腕视角输入、轨迹记录和人工评分。结果显示，布局、位姿和动力学等物理因素带来的影响，比外观或物体类别变化更大。另一项仿真-真实研究发现，REALM 比 VLA-Arena 和 SIMPLER 更能跟上真实机器人的策略排序，在模拟器后训练前后的 Spearman 相关系数分别是 0.700 和 0.875。

#### Evidence
- [LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination](../Inbox/2026-06-09--libero-occ-evaluating-and-improving-vision-language-action-models-under-scene-induced-occlusion-via-viewpoint-imagination.md): LIBERO-Occ task design, VIM method, and occlusion success rates.
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): UMI-Bench protocol, task coverage, model scores, and shift diagnostics.
- [A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation](../Inbox/2026-06-09--a-practical-recipe-towards-improving-sim-and-real-correlation-for-vla-evaluation.md): Sim-real evaluation setup and REALM correlation results.

### 测试时检查加入了几何、接触和稠密进度信号
执行时的安全和纠错是一个主要主题。VeriSpace 从冻结的 VLA 策略里采样多个候选动作，用 RGB-D 空间推理给它们打分，执行分数最高的候选动作。在 SimplerEnv-WidowX 上配合 OpenVLA，四个任务的平均成功率从 37.0% 提升到 55.0%。

接触密集型工作增加了另一层反馈。TacForeSight 从腕部力和当前触觉输入预测短时域的触觉潜变量，再用这些预测生成动作。它在五个真实机器人接触任务上的平均完成分数是 79.0%，而列出的最强基线是 43.0%。SARM2 通过带阶段感知的稠密奖励模型处理长时域进度估计；和 SPIRAL 配合后，它在 Cleaning Whiteboard 上达到 18/20 次成功，在 Folding Shorts Flat 上达到 12/12 次成功。

#### Evidence
- [VeriSpace: Spatially Grounded Action Verification for Vision-Language-Action Models](../Inbox/2026-06-09--verispace-spatially-grounded-action-verification-for-vision-language-action-models.md): VeriSpace test-time verifier design and success gains.
- [TacForeSight: Force-Guided Tactile World Model for Contact-Rich Manipulation](../Inbox/2026-06-09--tacforesight-force-guided-tactile-world-model-for-contact-rich-manipulation.md): TacForeSight force-conditioned tactile world model and real-robot scores.
- [SARM2: Multi-Task Stage Aware Reward Modeling for Self Improving Robotic Manipulation](../Inbox/2026-06-09--sarm2-multi-task-stage-aware-reward-modeling-for-self-improving-robotic-manipulation.md): SARM2 reward accuracy and SPIRAL real-robot improvement results.

### 长时域控制受益于明确的编排和规划
长任务正在被当作控制回路设计问题来处理。层次化 VLA 研究把高层语言子目标和低层动作执行分开，然后测试规划器选择、控制器选择、记忆、观测编码和终止规则。它的最佳层次结构在长时域 MuJoCo ALOHA 任务上达到 67.08%，而扁平 VLA 只有 25.30%。在真实的 ALOHA 水果分拣任务上，它把 15 个水果中的 12 个放对了，而扁平设置只放对 3 个。

MODIP 对扩散策略也采用类似思路。它用潜在世界模型和模型预测控制生成更好的轨迹，然后用监督去噪训练扩散策略。该方法在 D4RL Kitchen Complete 上报告 0.94 的成功率，在 Kitchen Partial 上报告 0.98 的成功率，在这些设置里明显超过行为克隆。

#### Evidence
- [What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents](../Inbox/2026-06-09--what-matters-in-orchestrating-robot-policies-a-systematic-study-of-hierarchical-vla-agents.md): Hierarchical VLA design study and long-horizon simulation plus real ALOHA results.
- [MODIP: Efficient Model-Based Optimization for Diffusion Policies](../Inbox/2026-06-09--modip-efficient-model-based-optimization-for-diffusion-policies.md): MODIP world-model planning approach and offline-to-online success metrics.

### 当策略使用可迁移的手部几何时，人类视频就变得可用
Dexterous Point Policy 是这个窗口里最强的数据扩展结果。它只用人类视频训练灵巧机器人手的行为，没有使用机器人示教。关键抽象是六个共享的 3D 点：腕部和五个指尖。然后，物体点、语言、相机位姿和接触标签共同引导一个自回归 Transformer，而逆运动学把预测点映射到机器人关节。

它报告的真实机器人差距很大。在八个灵巧任务上，DPP 的平均成功率达到 75.0%，而 Point Policy 只有 3.7%，VITRA 只有 1.0%。接触预测在论文消融中很关键，相比只用点的基线带来了 71.3 个百分点的提升。

#### Evidence
- [Dexterous Point Policy: Learning Point-based Dexterous Hand Policies from Human Demonstrations](../Inbox/2026-06-09--dexterous-point-policy-learning-point-based-dexterous-hand-policies-from-human-demonstrations.md): DPP human-video training setup, 3D keypoint abstraction, and real-robot success rates.
