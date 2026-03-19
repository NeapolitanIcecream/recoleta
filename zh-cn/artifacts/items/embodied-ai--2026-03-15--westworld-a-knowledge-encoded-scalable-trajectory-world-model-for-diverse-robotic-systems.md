---
source: arxiv
url: http://arxiv.org/abs/2603.14392v1
published_at: '2026-03-15T14:12:43'
authors:
- Yuchen Wang
- Jiangtao Kong
- Sizhe Wei
- Xiaochang Li
- Haohong Lin
- Hongjue Zhao
- Tianyi Zhou
- Lu Gan
- Huajie Shao
topics:
- world-model
- trajectory-prediction
- mixture-of-experts
- robot-morphology
- scalable-pretraining
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# WestWorld: A Knowledge-Encoded Scalable Trajectory World Model for Diverse Robotic Systems

## Summary
WestWorld提出了一个可扩展的轨迹世界模型，用于在多种机器人系统之间联合学习动力学，同时显式编码机器人形态结构知识。核心贡献是把“不同机器人该用不同动力学子模块”与“机器人结构先验”结合起来，以提升零样本、少样本和下游控制表现。

## Problem
- 现有多机器人轨迹世界模型通常把所有系统塞进一个共享的稠密模型里，随着机器人种类增多，容易出现梯度冲突和负迁移，扩展性差。
- 不同机器人存在传感器/执行器维度和采样频率异构，以及形态学和运动学结构差异，导致共享表示很难学好。
- 许多方法只把轨迹当作token序列处理，忽略机器人形态结构这一物理先验，因此对未见机器人零样本泛化较弱。

## Approach
- 作者提出 **WestWorld**，在89个仿真与真实环境上预训练一个统一的轨迹世界模型，用过去的状态-动作历史预测未来状态。
- 为了处理不同机器人的动力学差异，模型使用 **system-aware Mixture-of-Experts (Sys-MoE)**：先学习一个系统嵌入，再用它给多个专家分配权重，让不同机器人动态组合不同专家，而不是强迫所有系统共享同一套参数。
- 为了注入物理结构先验，模型构造 **structural embedding**：把机器人视作运动学树，经LCRS转换后提取pre/in/post-order遍历索引和对象ID，并把这些结构索引嵌入到状态/动作通道表示中。
- 输入侧先对每个状态/动作标量通道做归一化、离散化和嵌入；主干中用自注意力建模状态通道关系、用交叉注意力注入动作条件，再经Mamba风格SSM和MoE专家进行动力学建模。
- 训练目标是对离散化后的下一步状态token做交叉熵预测；推理时可一次前向完成多步预测。

## Results
- **零样本长时域预测**（50步历史输入，100步预测）在3个未见环境上均优于基线：
  - **Walker2d**：MAE **16.350** vs TDM 20.122 / TrajWorld 22.261 / MLPEnsemble 26.006；MSE **5.064** vs 6.428 / 8.623 / 12.028。
  - **Hopper**：MAE **13.731** vs 17.634 / 17.388 / 19.987；MSE **3.368** vs 5.076 / 5.441 / 7.216。
  - **Franka**：MAE **7.737** vs 23.686 / 13.102 / 12.164；MSE **2.539** vs 8.435 / 5.127 / 4.271。
- **少样本适应**（每个数据集仅10个episode微调）在3个真实机器人系统上也最好：
  - **Cassie**：MAE **5.316±0.108** vs TrajWorld 7.834±0.167；MSE **0.808±0.025** vs 1.697±0.109。
  - **A1**：MAE **4.227±0.120** vs TrajWorld 5.138±0.200；MSE **0.628±0.040** vs 0.900±0.050。
  - **UR5**：MAE **4.925±0.317** vs TrajWorld 8.066±0.799；MSE **0.831±0.150** vs 2.117±0.433。
- **扩展性**：预训练环境数从 **N=1,2,5,10,20,30** 增加时，文中称WestWorld误差保持较低且变化不大，而TrajWorld随环境增多显著退化；该段未给出具体数值，但作为主要可扩展性结论被强调。
- **下游与真实部署**：作者声称WestWorld显著提升不同机器人的下游模型式控制表现，并已部署到真实 **Unitree Go1**，展示稳定运动；摘录中未提供具体控制分数或成功率数值。

## Link
- [http://arxiv.org/abs/2603.14392v1](http://arxiv.org/abs/2603.14392v1)
