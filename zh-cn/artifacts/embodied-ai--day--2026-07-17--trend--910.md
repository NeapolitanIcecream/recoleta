---
kind: trend
trend_doc_id: 910
granularity: day
period_start: '2026-07-17T00:00:00'
period_end: '2026-07-18T00:00:00'
topics:
- embodied AI
- robot control
- VLA models
- physical reasoning
- deployment efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-910
tags:
- recoleta/trend
- topic/embodied-ai
- topic/robot-control
- topic/vla-models
- topic/physical-reasoning
- topic/deployment-efficiency
language_code: zh-CN
---

# 闭环执行成为具身智能的决定性检验

## 概览
当天的证据将近期对部署的关注点从单纯的推理速度扩展开来。IMBench 表明，识别物理约束并不能可靠地产生可执行行为；AC-VLA 和快慢驾驶则通过使学习或计算与控制回路相匹配来改善结果。大多数证据仍来自仿真，因此尚不能证明广泛的现实世界可靠性。

## 研究发现

### 物理推理必须经受执行检验
IMBench 让推理与行动之间的鸿沟变得可测量。领先的视觉语言模型在约束理解上的得分约为 74%，但 GPT-5.5 仅完成了视觉输入任务的 11.3%，在获得特权物体状态信息时也只有 18.8%。若干对齐、工具使用、隐状态和平衡任务的完成率仍为零。

AC-VLA 针对策略层面的相关失效。它将指令分解为可复用的子任务，并在选定阶段屏蔽腕部视角，以减少轨迹记忆和视觉捷径。在 LIBERO-OOD 上，π₀.₅ 变体在 Spatial-OOD 和 Goal-OOD 上的成功率分别达到 64.2% 和 73.3%，提升了 28.7 和 26.7 个百分点。两项研究共同表明，评估和训练应关注可执行的动作重组，而不能只依赖语言能力或分布内能力。

#### 资料来源
- [IMBench: A Benchmark for Intuitive Robotic Manipulation](../Inbox/2026-07-17--imbench-a-benchmark-for-intuitive-robotic-manipulation.md): 报告称约束理解率约为 74%，但仅有 11.3% 的纯视觉闭环成功率和 18.8% 的特权状态闭环成功率。
- [AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning](../Inbox/2026-07-17--ac-vla-robust-out-of-distribution-action-execution-via-compositional-learning.md): 介绍了子任务监督和状态条件掩码方法，以及 28.7 和 26.7 个百分点的 OOD 提升。

### 慢速上下文与快速行动相互分离
快慢驾驶将延迟转化为架构选择。一个冻结的 7B 主干网络以 5 Hz 刷新场景上下文，而一个 337M 的动作专家利用最新帧以 20 Hz 发出控制指令。CARLA 中的路线完成率从使用重放指令时的 37.0% 上升到 94.0%；不过，长路线驾驶得分只有 2.96，安全性仍未得到解决。

JoyNexus 将类似的分离原则应用于后训练基础设施。它让共享主干网络常驻，同时隔离租户专属的动作模块、优化器状态和策略版本。组批处理在兼容的工作负载之间复用主干网络计算。论文报告了更低的总体 GPU 时间，但没有给出数值化的效率结果，因此这体现的是架构层面的信号，而不是经过量化的系统性进展。

#### 资料来源
- [Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving](../Inbox/2026-07-17--think-at-5-hz-act-at-20-hz-asynchronous-fast-slow-vision-language-action-inference-for-closed-loop-driving.md): 详细介绍了 5 Hz/20 Hz 的划分、路线完成率从 37.0% 提升至 94.0% 的结果，以及较弱的长路线安全得分。
- [JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models](../Inbox/2026-07-17--joynexus-service-oriented-multi-tenant-post-training-for-vla-models.md): 介绍了共享常驻主干网络、隔离的租户状态和组批处理；论文未报告数值化的效率提升。
