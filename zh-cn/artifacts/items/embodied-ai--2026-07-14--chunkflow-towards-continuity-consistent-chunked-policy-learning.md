---
source: arxiv
url: https://arxiv.org/abs/2607.12992v1
published_at: '2026-07-14T17:43:25'
authors:
- Zhao Yang
- Yinan Shi
- Mingyuan Yao
- Wenyao Xue
- Yawei Jueluo
- Longjun Liu
topics:
- vision-language-action
- generalist-robot-policy
- robot-data-scaling
- dexterous-manipulation
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ChunkFlow: Towards Continuity-Consistent Chunked Policy Learning

## Summary
## 摘要
ChunkFlow 旨在解决生成重叠动作块的视觉-语言-动作策略中的时间抖动问题。它将接缝感知训练与确定性的重叠融合相结合，在部署时无需增加一次策略前向传播，即可改善连续性、长时域任务成功率和推理效率。

## 问题
- 连续动作块使用了发生偏移的观测和已执行历史，因此其重叠步骤可能产生不一致，造成边界抖动和机器人运动不稳定。
- 仅在推理阶段进行平滑的方法会重新加权冲突动作，但不会纠正导致接缝不匹配的策略误差，因此残余误差可能在长时间滚动执行中不断累积。

## 方法
- 将每个动作块划分为冻结区、可编辑接缝区和未来区，然后对重叠动作进行线性融合，使控制权以确定性的方式从前一个动作块转移到当前动作块。
- 使用边界损失，以及一阶全变分和二阶曲率惩罚，对原始动作块预测进行训练。
- 对动作历史进行扰动，并采用计划采样，使策略在训练期间接触执行历史误差。
- 使用基于优势加权的 actor-critic 更新进行微调，采用融合后的历史，同时保留接缝和连续性正则项。

## 结果
- 在 CALVIN ABC-D 上，ChunkFlow 报告的平均回合长度为 4.30，MSD-Δa 为 0.075，MSD-Δ²a 为 0.154，接缝跳变为 0.209，HF 比率为 0.431，TV-L1 为 0.001。
- 在 LIBERO-Long 上，其成功率达到 93.4%；PI0.5 为 92.6%，PI0.5-RTC 为 83.7%，CLIP-RT 为 83.8%，OpenVLA 为 53.7%。
- 在 LIBERO-Long 上，它报告了所列运动和伪影指标中的最低值：MSD-Δa 为 0.042，MSD-Δ²a 为 0.197，MSD-Δ³a 为 0.235，接缝跳变为 0.082，HF 比率为 0.135，TV-L1 为 0.011。
- 在 LIBERO 上，其平均推理延迟为 4.43 ms；PI0.5-RTC 为 18.47 ms，PI0.5 为 9.04 ms。
- 在两个真实机器人任务中，论文报告了 9/10 次试验成功；摘要未提供任务级基线或统计不确定性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.12992v1](https://arxiv.org/abs/2607.12992v1)
