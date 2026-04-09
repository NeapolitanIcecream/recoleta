---
source: arxiv
url: http://arxiv.org/abs/2603.28545v1
published_at: '2026-03-30T15:06:41'
authors:
- Yu Sun
- Meng Cao
- Ping Yang
- Rongtao Xu
- Yunxiao Yan
- Runze Xu
- Liang Ma
- Roy Gan
- Andy Zhai
- Qingxuan Chen
- Zunnan Xu
- Hao Wang
- Jincheng Yu
- Lucy Liang
- Qian Wang
- Ivan Laptev
- Ian D Reid
- Xiaodan Liang
topics:
- robot-benchmark
- vision-language-action
- generalist-robot-policy
- mobile-manipulation
- real-to-sim
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ManipArena: Comprehensive Real-world Evaluation of Reasoning-Oriented Generalist Robot Manipulation

## Summary
## 摘要
ManipArena 是一个面向通用机器人操作的真实世界基准，用于在标准化物理条件下评估强调推理能力的 Vision-Language-Action 和 world-model 系统。它提供一套共享评测设置，包含多样化任务、受控的分布外测试、丰富的传感器数据流，以及与之对应的仿真环境。

## 问题
- 现有机器人基准主要依赖仿真，因此无法覆盖真实部署中的问题，例如感知噪声、接触动力学、延迟和硬件限制。
- 真实世界评测通常在不同机器人平台和实验室环境中进行，因此结果难以复现，也难以解释。
- 通用机器人模型需要针对语义推理、空间泛化和长时程移动操作的测试，但以往基准只覆盖了其中一部分。

## 方法
- 该基准定义了 **20 个真实世界任务**，覆盖执行推理、语义推理和移动操作，并以约 **188 小时**采集的 **10,812 条专家轨迹**为支撑。
- 它采用 **统一共享的机器人本体** 和 **服务端推理协议**，每个参与者需为所有任务提交 **一个模型端点**，因此分数反映的是策略质量，而不是定制硬件或按任务单独优化。
- 评测在一个 **绿幕封闭隔间** 内进行，并使用固定光照来控制变量；每个任务采用 **分层的 10 次试验设计**：**T1-T4** 为域内，**T5-T8** 为分布有变化但仍在分布内，**T9-T10** 在可用时为语义 OOD。
- 训练多样性沿 **三个层级** 设计：物理属性、空间布局和语义组合，并对 OOD 物体设置了明确的训练/测试划分。
- 该基准还包含 **丰富的观测数据**，如关节速度和电机电流，以及基于 **3D Gaussian Splatting**、**Hunyuan3D** 资产和 **IsaacLab** 回放对齐构建的 **Real2Sim** 环境。

## 结果
- 摘录中 **没有提供基准分数或基线性能数字**，因此没有可报告的定量模型比较。
- 论文称其覆盖范围比以往基准更广：总计 **20 个任务**，其中包括 **10 个执行任务**、**5 个语义任务** 和 **5 个移动任务**。
- 数据集包含 **10,812 条轨迹** 和约 **188 小时**的数据。
- 移动任务比桌面任务长得多：在 20 fps 下，平均帧数为 **2,878 vs. 665**，约为 **4.3×**；移动任务占总数据集帧数的 **60.6%**，但轨迹数占比为 **26.7%**。
- 桌面任务每帧使用 **56D** 状态/动作；移动任务使用 **62D**。完整采集在发布前过滤前记录的是每帧 **112D**。
- 桌面评测使用 **15 个任务**，每个任务按 **10 次试验**计分，每次试验 **0-10 分**，因此每个任务最高 **100 分**，这些桌面评测任务合计最高 **1,500 分**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28545v1](http://arxiv.org/abs/2603.28545v1)
