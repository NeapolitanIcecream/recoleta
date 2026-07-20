---
kind: ideas
granularity: day
period_start: '2026-07-17T00:00:00'
period_end: '2026-07-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied AI
- robot control
- VLA models
- physical reasoning
- deployment efficiency
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robot-control
- topic/vla-models
- topic/physical-reasoning
- topic/deployment-efficiency
language_code: zh-CN
---

# 闭环 VLA 训练与评估的变化

## 摘要
阶段标签既可以控制操作过程中的传感器访问，也可以控制策略评估中的计算复用。证据支持对训练和测试基础设施进行范围更窄的调整，而不支持关于一般物理可靠性的判断；后者仍受到以仿真为主的评估以及较弱的长时域安全结果所限制。

## 面向组合式操作的约束感知腕部相机遮挡
VLA 训练团队应将仅依据夹爪状态的腕部相机遮挡，改为同时考虑当前子任务及其物理约束的门控机制。AC-VLA 在夹爪闭合阶段进行遮挡，以抑制视觉捷径，并促成 LIBERO-OOD 上的大幅提升；但 IMBench 表明，即使模型能够识别约束，对齐、工具使用、隐藏状态、时序和平衡仍是执行瓶颈。这些操作在夹爪闭合后可能需要近距离或力敏感观测，因此单一遮挡规则可能会以传感器信息缺失为代价，换取对轨迹记忆的抑制。

具体做法是为 AC-VLA 自动分割的子任务附加约束标签：在第三人称视角的几何信息足够的搬运阶段抑制腕部视角，但在接触、对齐、工具、隐藏状态和稳定性阶段保留该视角。首先可以在留出的 LIBERO-OOD 和 IMBench 回合中，按阶段进行推理时遮挡消融；如果移除腕部视角对这些约束类别的损害明显更大，训练门控就应依据约束类型，而不只是夹爪状态进行条件控制。

### 资料来源
- [AC-VLA: Robust Out-of-Distribution Action Execution via Compositional Learning](../Inbox/2026-07-17--ac-vla-robust-out-of-distribution-action-execution-via-compositional-learning.md): AC-VLA 在夹爪闭合阶段遮挡腕部相机输入；使用 π₀.₅ 时，其 Spatial-OOD 和 Goal-OOD 成功率分别为 64.2% 和 73.3%，提升了 28.7 和 26.7 个百分点。
- [IMBench: A Benchmark for Intuitive Robotic Manipulation](../Inbox/2026-07-17--imbench-a-benchmark-for-intuitive-robotic-manipulation.md): IMBench 报告称，GPT-5.5 在仅视觉输入和特权状态输入下的闭环成功率分别只有 11.3% 和 18.8%；对齐、时序、工具使用、隐藏状态和平衡任务在两种设置下均为 0%。

## 共享慢速骨干前缀的分叉式闭环评估
比较多个动作专家或面向不同租户的 VLA 策略时，团队可以从共同的观测历史分叉模拟器状态，以减少重复的评估计算。对共享前缀只计算一次慢速骨干网络及其缓存，将各个隔离的动作专家连接到该缓存，并仅在它们的动作出现分歧时分叉环境。JoyNexus 已经隔离租户专属模块，并围绕常驻骨干网络对兼容工作负载进行分组；快慢速驾驶系统则表明，动作专家可以在控制频率下读取持久化骨干缓存和当前帧。

评估器必须保留闭环分支，而不是在同一条固定日志上为每个专家评分：驾驶研究中，同一动作专家的路线完成率从 10 Hz 时的 82.1% 提升到 20 Hz 时的 94.0%，说明控制频率会改变结果。成本最低的实现检查是分叉相同的模拟器快照，比较共享前缀缓存与独立计算缓存在数值和轨迹上的等价性，然后在分支发生前测量节省的 GPU 时间。JoyNexus 没有报告数值化的效率提升，因此在采用该设计前必须进行这项测量。

### 资料来源
- [JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models](../Inbox/2026-07-17--joynexus-service-oriented-multi-tenant-post-training-for-vla-models.md): JoyNexus 让共享骨干网络常驻，隔离租户专属的动作模块和策略状态，并对兼容样本进行共享骨干计算分组，但没有报告数值化的效率指标。
- [Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving](../Inbox/2026-07-17--think-at-5-hz-act-at-20-hz-asynchronous-fast-slow-vision-language-action-inference-for-closed-loop-driving.md): 一个 337M 参数的动作专家读取冻结的 7B 骨干网络的持久化缓存和当前帧；将新鲜控制频率从 10 Hz 提升到 20 Hz 后，CARLA 路线完成率从 82.1% 提升到 94.0%。
