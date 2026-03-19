---
source: arxiv
url: http://arxiv.org/abs/2603.08744v1
published_at: '2026-03-02T13:53:59'
authors:
- "Yanis A\xEFt-A\xEFssa"
- Thomas Carle
- Sergei Chichin
- Benjamin Lesage
- Claire Pagetti
topics:
- code-generation
- multi-core-scheduling
- real-time-systems
- dnn-inference
- constraint-programming
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Extension of ACETONE C code generator for multi-core architectures

## Summary
本文扩展了 ACETONE，把原本面向单核、可认证的 DNN 推理 C 代码生成，推进到多核 CPU 上的可预测并行执行。核心是在离线阶段把网络推理建模为 DAG 调度问题，再用约束规划或启发式方法生成带同步的并行代码。

## Problem
- 目标问题：在航空等安全关键系统中，如何让已训练好的 DNN 在**多核 CPU**上更快运行，同时仍保持**可预测性、可分析 WCET、易认证**的代码属性。
- 重要性：单核执行会导致推理时间快速增长，可能违反实时约束；而航空场景短期内又不适合依赖专用加速器，因此多核 CPU 是现实可落地的路线。
- 难点：多核并行不仅要决定任务如何划分和映射到核心，还要处理同步、通信延迟、静态调度、非抢占执行，以及认证友好的代码生成限制。

## Approach
- 把 DNN 的每一层视为一个任务，整体表示成 **DAG**：节点带有该层的 WCET，边带有跨核通信延迟；目标是在固定数量核心上最小化总完成时间（makespan）。
- 采用**静态离线调度**：任务非抢占，只有所有前驱完成且数据可用后才可开始；允许任务复制到多个核心上，以减少通信开销，但会限制冗余复制。
- 提出一种比 Tang 等人更高效的**约束规划/ILP 风格编码改写**：去掉原来复杂的 4D 通信变量张量，改用更少决策变量与改进约束来表达通信与复制，从而提升求解规模能力。
- 同时实现两类启发式：**ISH** 通过关键路径优先的列表调度并利用空闲间隙插入任务；**DSH** 进一步尝试复制父任务以减少跨核等待，通常更接近最优但更慢、更占内存。
- 在代码生成层面，作者将 ACETONE 扩展为能根据离线调度结果生成**多核并行 C 代码**，并在 bare-metal 环境中加入核心映射与同步机制。

## Results
- 在随机生成的 **20 / 50 / 100 节点 DAG**、**10% density** 数据集上评估，随着核心数从 **2 到 20** 增加，ISH 和 DSH 的**speedup** 都先上升后进入平台期；平台由图的最大并行度决定。
- 启发式比较：**DSH 的 speedup 总是高于或等于 ISH**，说明其更接近最优；但**DSH 的计算时间会随核心数增长上升 1–2 个数量级**，在文中实验里**接近每张图 2 分钟**，而 ISH 更快且更稳定。
- 精确求解比较：在相同条件下，**Tang 等人的表示在 1 小时超时内无法找到解**；作者的优化编码则在**所有测试配置**下都能返回至少一个解，且返回解**不差于** Tang 方法。
- ILP/CP 优化编码的速度代价仍然很高：在 **50 节点**图上，平均求解时间**从不低于 54 分钟**，且经常触发 **1 小时 timeout**；因此它更适合较小图或作为高质量优化器使用。
- 质量上，优化编码得到的 speedup 平台与 DSH 接近，但通常**约在 5 个核心**就达到平台，而 DSH 约需**7 个核心**，支持“**DSH 是近最优，求解器更接近最优**”这一结论。
- 关于真实部署效果，文摘明确声称该多核扩展已通过**OTAWA 的 WCET 分析**和**实验测得的 WCET**进行验证，但给定摘录中**未提供具体实机 WCET 数值**。

## Link
- [http://arxiv.org/abs/2603.08744v1](http://arxiv.org/abs/2603.08744v1)
