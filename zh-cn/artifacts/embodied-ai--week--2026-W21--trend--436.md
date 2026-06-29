---
kind: trend
trend_doc_id: 436
granularity: week
period_start: '2026-05-18T00:00:00'
period_end: '2026-05-25T00:00:00'
topics:
- "\u5177\u8EAB AI"
- "\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C"
- "\u673A\u5668\u4EBA\u64CD\u4F5C"
- "3D \u5B9A\u4F4D"
- "\u7A7A\u95F4\u8BB0\u5FC6"
- "\u771F\u5B9E\u4E16\u754C\u8BC4\u4F30"
run_id: materialize-outputs
aliases:
- recoleta-trend-436
tags:
- recoleta/trend
- "topic/\u5177\u8EAB-ai"
- "topic/\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C"
- "topic/\u673A\u5668\u4EBA\u64CD\u4F5C"
- "topic/3d-\u5B9A\u4F4D"
- "topic/\u7A7A\u95F4\u8BB0\u5FC6"
- "topic/\u771F\u5B9E\u4E16\u754C\u8BC4\u4F30"
language_code: zh-CN
---

# 机器人 VLA 主张现在需要真实执行证据

## Overview
本周具身 AI 研究把机器人策略视为必须承受真实控制条件的系统。视觉-语言-动作（VLA）模型通过视觉扰动、3D 接触线索、记忆、延迟和可复现硬件运行来测试。StableVLA、GaussianDream 和 AVP 给出了最清晰的信号。

## Clusters

### 不完整感知下的执行可靠性
VLA 工作现在要看执行时的表现：模糊、光照变化、延迟、扰动和细粒度任务阶段。StableVLA 用 Information Bottleneck Adapter 直接处理这个问题，在不增加机器人数据的情况下过滤有噪声的视觉通道。报告中的提升很具体：在 severity-5 扰动下的 LIBERO Spatial 上为 82.0% 对 58.5%，在真实 Pack Doll 任务中相对 VLA-Adapter 基线为 50% 对 20%。本周的日常趋势证据也显示，延迟和照明测试是常见的可靠性检查。

#### Evidence
- [StableVLA: Towards Robust Vision-Language-Action Models without Extra Data](../Inbox/2026-05-18--stablevla-towards-robust-vision-language-action-models-without-extra-data.md): StableVLA 摘要给出了视觉扰动设置、适配器设计，以及报告的仿真和真实机器人提升。

### 动作预测中的 3D 接触线索
多篇论文把显式几何加入策略路径，而非只放在感知模块。GaussianDream 用 3D Gaussian 重建和短时域未来预测训练 VLA 策略，推理时只保留学到的前缀 token。它报告在 LIBERO 上平均成功率为 98.4%，在 RoboCasa Human-50 上为 52.6%，在真实机器人评估中为 50.0%。PointACT 将分层点云特征送入动作解码器，在 LIBERO 上达到 96.0% 平均成功率，并在报告表格中比 SpatialVLA 高 17.9 个点。这些结果把 3D 结构纳入动作接口。

#### Evidence
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream 摘要涵盖了 3D Gaussian 训练监督、推理设计，以及报告的基准和真实机器人数字。
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT 摘要涵盖了点云动作解码，以及它在 LIBERO 上的结果和与 SpatialVLA 的比较。

### 闭环操作的空间定位与记忆
最强的具身定位论文加入了机器人可执行的中间状态。AVP 让视觉语言模型先输出视觉 primitive token，再进行动作预测，然后使用 flow-matching 动作专家。在中国象棋操作任务上，它报告平均成功率为 90.28%，π₀.₅ 为 62.67%，同时每条指令运行时间为 0.27 秒。SOMA 为当前相机视野外的物体加入持久空间记忆。在五个真实世界视野外任务上，完整 SOMA 达到 28.3% 平均成功率，并且相较 GR00T-N1.5 缩短了各任务的抓取用时。共同点很实际：策略在执行期间需要目标状态、场景记忆和快速动作检查。

#### Evidence
- [Action with Visual Primitives](../Inbox/2026-05-21--action-with-visual-primitives.md): AVP 摘要给出了视觉 primitive 动作接口、真实机器人成功率和延迟。
- [Spatial Memory for Out-of-Vision Manipulation in Vision-Language-Action](../Inbox/2026-05-21--spatial-memory-for-out-of-vision-manipulation-in-vision-language-action.md): SOMA 摘要给出了持久空间记忆、视野外任务结果、搜索时间和抓取用时减少。

### 可复现的真实世界基准成为基础设施
评估工作正在让实体机器人测试更容易复现。VLA-REPLICA 使用现成硬件、固定照明、相机对齐工具、参考摆放位置，以及覆盖 10 个操作任务的 500 条专家演示。报告称完整装置约为 $1050，新用户可在一小时内完成组装。它的 90 个测试场景覆盖同分布和分布外评估，π₀.₅ 达到报告中最好的同分布平均成功率 0.54。这类基准降低了检查策略能否在模拟器外工作的成本。

#### Evidence
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA 摘要提供了硬件成本、设置细节、任务套件、演示数量、测试场景和基线结果。
