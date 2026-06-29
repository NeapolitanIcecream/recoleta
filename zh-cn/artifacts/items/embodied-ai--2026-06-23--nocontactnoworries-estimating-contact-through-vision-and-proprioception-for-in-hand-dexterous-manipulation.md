---
source: arxiv
url: https://arxiv.org/abs/2606.24450v1
published_at: '2026-06-23T11:36:46'
authors:
- Soham Patil
- Avirup Das
- Sourabh Bhosale
- Spandan Roy
topics:
- dexterous-manipulation
- pseudo-tactile-sensing
- rgb-d-proprioception
- contact-estimation
- sim2real
- robot-policy
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# NoContactNoWorries: Estimating Contact through Vision and Proprioception for In-Hand Dexterous Manipulation

## Summary
## 摘要
NoContactNoWorries 使用腕部 RGB-D 视频和关节状态，为 LEAP Hand 预测指尖接触，让机器人在没有触觉传感器的情况下获得二值伪触觉反馈。论文称，该信号可以替代仿真器或触觉传感器提供的接触信号，用于手内物体重定向，并支持真实机器人迁移。

## 问题
- 灵巧手内操作依赖接触反馈，但指尖触觉传感器会增加成本、易损性、布线、标定工作，并且覆盖范围有限。
- 腕部 RGB-D 相机更容易部署，但在操作过程中，手指与物体的接触常被手或物体遮挡。
- 这个任务有实际意义，因为接触信号可以帮助策略响应抓取变化、滑移和接触丢失，同时不需要添加定制硬件。

## 方法
- 模型预测一个 4-bit 二值接触向量，LEAP Hand 的每个指尖接触点对应 1 bit。
- 冻结的 RGB-D 分割编码器从 240×320 RGB 和深度帧中提取空间视觉特征。
- 当前关节角和指令关节角分别嵌入，然后作为查询，通过交叉注意力读取视觉 token。
- 因果 Transformer 读取 8 帧窗口，并通过 sigmoid 接触头输出当前指尖接触概率。
- 训练使用 PhysX 的仿真器接触标签；真实力敏电阻只用于评估，接触阈值为 0.1 N。

## 结果
- 接触预测器在 50 条仿真 rollout 上训练，每条 15 s，覆盖 5 个训练物体；标签以 30 Hz 覆盖 4 个指尖接触点。
- 在已见物体的仿真测试中，完整模型的 F1 分数为：长方体 0.93、五棱柱 0.90、十二面体 0.91、星形物体 0.88、阶梯形物体 0.88。
- 在留出物体的仿真测试中，模型在六棱柱上达到 0.89 F1，在字母 R 上达到 0.87 F1。
- 在真实 LEAP Hand 上，模型在长方体上达到 0.84、五棱柱 0.83、十二面体 0.82、星形物体 0.71、阶梯形物体 0.79、六棱柱 0.80、字母 R 0.74。
- 在六棱柱的仿真遮挡分析中，接触区域在约 61% 的帧中被遮挡；完整模型在可见时的 F1 为 0.93，在被遮挡时为 0.85，而仅视觉模型从 0.79 降至 0.51。
- 消融实验显示，完整模型优于仅视觉、仅姿态、无时序建模和运动学深度基线；例如，在真实长方体数据上，各分数为完整模型 0.84、最佳仅姿态 0.72、仅视觉 0.48、无时序建模 0.69、运动学深度 0.55。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24450v1](https://arxiv.org/abs/2606.24450v1)
