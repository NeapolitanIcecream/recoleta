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
- robot-world-model
- trajectory-prediction
- mixture-of-experts
- morphology-encoding
- zero-shot-generalization
relevance_score: 0.36
run_id: materialize-outputs
language_code: zh-CN
---

# WestWorld: A Knowledge-Encoded Scalable Trajectory World Model for Diverse Robotic Systems

## Summary
WestWorld 是一个面向多种机器人系统的可扩展轨迹世界模型，核心是把机器人结构知识编码进表示，并用系统感知的专家混合来分担不同动力学。它旨在同时提升跨机器人预训练的可扩展性，以及对未见机器人/环境的零样本与小样本泛化能力。

## Problem
- 现有多机器人轨迹世界模型通常用一套共享参数去拟合差异很大的机器人动力学，容易产生梯度冲突和负迁移，随着机器人种类增多更难扩展。
- 不同机器人存在传感器/执行器维度与语义不一致、采样频率不同、运动学结构差异大等问题，导致统一建模困难。
- 许多方法把轨迹仅当作 token 序列处理，忽略机器人形态结构这一物理先验，因此对未见系统的零样本泛化较弱。

## Approach
- 先把状态和动作按通道做归一化与离散化，把每个标量通道变成 token embedding，并加入时间、通道顺序、模态等嵌入。
- 引入 **knowledge-encoded structural embedding**：把机器人形态表示为运动学树，再转成二叉树，用 pre/in/post-order 与 object id 编码每个部件位置，把这些结构嵌入加到轨迹表示中，显式注入形态先验。
- 使用 **Sys-MoE**：不是让所有机器人共享同一套稠密参数，而是学习一个系统 embedding，经 SSM/Mamba 风格层提取系统级特征，再由 router 生成专家权重，动态组合多个专家来表示不同系统动力学。
- 在每层中先用 self-attention 聚合状态通道关系，再用 cross-attention 注入动作条件，最后通过系统感知的专家混合输出未来状态表示，实现多步预测。
- 在 89 个仿真与真实机器人环境上预训练，目标是给定历史状态/动作和未来动作，一次前向预测未来多步状态。

## Results
- **零样本长时域预测（100-step rollout, 50-step history）**：在 Walker2D 上，WestWorld 达到 **MAE 16.350 / MSE 5.064 (×10^-2)**，优于 MLPEnsemble **26.006 / 12.028**、TDM **20.122 / 6.428**、TrajWorld **22.261 / 8.623**。
- 在 Hopper 上，WestWorld 达到 **MAE 13.731 / MSE 3.368 (×10^-2)**，优于 MLPEnsemble **19.987 / 7.216**、TDM **17.634 / 5.076**、TrajWorld **17.388 / 5.441**。
- 在真实 Franka 数据上，WestWorld 达到 **MAE 7.737 / MSE 2.539 (×10^-2)**，优于 MLPEnsemble **12.164 / 4.271**、TrajWorld **13.102 / 5.127**、TDM **23.686 / 8.435**。
- **小样本适配（仅 10 episodes 微调）**：Cassie 上达到 **5.316±0.108 / 0.808±0.025**，优于 TrajWorld **7.834±0.167 / 1.697±0.109**；A1 上达到 **4.227±0.120 / 0.628±0.040**，优于 TrajWorld **5.138±0.200 / 0.900±0.050**；UR5 上达到 **4.925±0.317 / 0.831±0.150**，优于 TrajWorld **8.066±0.799 / 2.117±0.433**。
- 论文还声称在扩展到更多环境时，WestWorld 的预测误差随环境数增加仍保持较稳定，而 TrajWorld 明显退化；但给定摘录未提供该图的具体数值。
- 作者还声称该模型能显著提升下游基于模型的控制，并已部署到真实 **Unitree Go1** 上实现稳定运动；不过摘录中未给出对应控制指标或成功率数字。

## Link
- [http://arxiv.org/abs/2603.14392v1](http://arxiv.org/abs/2603.14392v1)
