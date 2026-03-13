---
source: arxiv
url: http://arxiv.org/abs/2603.07949v2
published_at: '2026-03-09T04:30:57'
authors:
- Zihao Zheng
- Sicheng Tian
- Hangyu Cao
- Chenyue Li
- Jiayu Chen
- Maoliang Li
- Xinhao Sun
- Hailong Zou
- Guojie Luo
- Xiang Chen
topics:
- vision-language-action
- edge-cloud-inference
- kinematic-triggering
- robot-systems
- latency-optimization
relevance_score: 0.8
run_id: materialize-outputs
---

# RAPID: Redundancy-Aware and Compatibility-Optimal Edge-Cloud Partitioned Inference for Diverse VLA Models

## Summary
RAPID提出一种面向VLA模型的边云协同推理框架，用机器人本体运动学而非视觉置信度来决定何时把推理卸载到云端。其目标是在多环境噪声下保持兼容性与动作连续性，同时降低时延并减少无效云端调用。

## Problem
- VLA模型参数大、边端推理慢，难以满足机器人实时控制需求，因此需要边云协同推理。
- 现有动态分割多依赖视觉熵等环境特征，容易被视觉噪声、遮挡和干扰误触发，跨环境兼容性差。
- 现有方法忽略 embodied 任务中的逐步动作冗余，导致在本可由边端平滑执行的阶段频繁打断动作、增加通信与推理开销。

## Approach
- 用**关节加速度**和**关节力矩变化**这两类不依赖环境视觉的本体感知信号，替代视觉熵作为边云分割触发依据。
- 设计两套分数：一套用滑窗统计归一化的加速度异常分数，检测任务切换、急停、避障等非线性运动变化；另一套用力矩变化的滑动均值和归一化异常分数，估计关键交互阶段对应的低冗余动作。
- 根据实时关节速度动态分配两类信号的权重：高速运动时更看重加速度，低速接触/操作时更看重力矩，从而形成动作重要性并触发双阈值卸载。
- 系统实现上加入异步多速率处理、动作抢占与冷却机制：传感器高频监控，控制低频执行；一旦检测到关键阶段就中止旧动作块并向云端请求新动作块，同时避免连续泛洪请求。
- 核心思想可用最简单的话概括为：**平稳、重复、低风险的动作留在边端执行；突然变化或关键接触时再调用云端更强的VLA重规划。**

## Results
- 论文声称相较于Edge-Only和vision-based基线（如SAFE/ISAR），RAPID可**最高提升准确率15.8%**，并实现**最高1.73×推理加速**，系统额外开销仅**5~7%**。
- 在仿真基准上，总时延从**Edge-Only 782.5±28.5 ms**降到**RAPID 222.9±11.4 ms**，约为**3.51×更快**；相较vision-based SAFE的**377.7±26.2 ms**，RAPID约快**1.69×**。
- 分项时延上，RAPID的云侧/边侧时延分别为**83.5 ms / 139.4 ms**，而SAFE为**62.5 ms / 315.2 ms**；说明RAPID通过更合理分工显著降低了边端负担。
- 在视觉基线的噪声鲁棒性分析中，总时延随环境恶化从**395.4 ms**（标准）升至**520.6 ms**（视觉噪声）和**685.3 ms**（干扰）；作者据此主张运动学触发比视觉触发更稳健。
- 动作冗余分析显示，冗余动作比例超过**80%**：Pick & Place **82.5%**、Drawer Opening **86.4%**、Peg Insertion **81.2%**；对应冗余动作平均注意力权重仅**0.008/0.005/0.007**，而关键动作为**0.076/0.062/0.058**。
- 论文给出了多项定量表格，但摘录中未完整展示真实机器人成功率等全部明细；最强结论是：RAPID在多噪声环境下兼顾了更低时延、更高兼容性和更少无效卸载。

## Link
- [http://arxiv.org/abs/2603.07949v2](http://arxiv.org/abs/2603.07949v2)
