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
ManipArena 是一个面向通用机器人操作的真实世界基准，用于在标准化物理条件下评估偏重推理的 Vision-Language-Action 和 world-model 系统。它建立了一套共享评测设置，包含多样任务、受控的分布外测试、丰富的传感器流和对应的仿真环境。

## 问题
- 现有机器人基准偏向仿真，因此会遗漏真实部署中的问题，例如感知噪声、接触动力学、时延和硬件限制。
- 真实世界评测常在不同机器人和实验室设置上进行，这让比较难以复现，也难以解释。
- 通用机器人模型需要针对语义推理、空间泛化和长时程移动操作的测试，但以往基准只覆盖了其中一部分。

## 方法
- 该基准定义了 **20 个真实世界任务**，覆盖执行推理、语义推理和移动操作，基于约 **188 小时**采集的 **10,812 条专家轨迹**。
- 它使用 **单一共享机器人本体** 和 **服务器端推理协议**，每个参与者为所有任务提交 **一个模型端点**，因此分数反映的是策略质量，而不是定制硬件或按任务专门优化。
- 评测在一个 **绿幕封闭舱** 内进行，并使用固定照明来隔离受控变量；每个任务采用 **分层 10 次试验设计**：**T1-T4** 为域内，**T5-T8** 为偏移但仍在分布内，**T9-T10** 在可用时为语义 OOD。
- 训练多样性沿着 **三个层级** 设计：物理属性、空间布局和语义组合，并为 OOD 物体明确划分训练/测试。
- 该基准还包含 **丰富观测**，例如关节速度和电机电流，以及使用 **3D Gaussian Splatting**、**Hunyuan3D** 资产和 **IsaacLab** 回放对齐构建的 **Real2Sim** 环境。

## 结果
- 摘要中**没有提供基准得分或基线性能数值**，因此没有可报告的定量模型对比。
- 论文声称其覆盖范围比以往基准更广：总计 **20 个任务**，其中包括 **10 个执行任务**、**5 个语义任务** 和 **5 个移动任务**。
- 数据集包含 **10,812 条轨迹** 和约 **188 小时**的数据。
- 移动任务比桌面任务长得多：在 20 fps 下平均 **2,878 帧对 665 帧**，约为 **4.3 倍**，并且它们占总数据集帧数的 **60.6%**，但只占 **26.7%** 的轨迹。
- 桌面任务每帧使用 **56D** 状态/动作；移动任务使用 **62D**。完整采集在发布前过滤之前，每帧记录 **112D**。
- 桌面评测使用 **15 个任务**，每个任务 **10 次试验**，每次 **0-10 分**，单个任务最高 **100 分**，这些被评测的桌面任务总分最高 **1,500 分**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28545v1](http://arxiv.org/abs/2603.28545v1)
