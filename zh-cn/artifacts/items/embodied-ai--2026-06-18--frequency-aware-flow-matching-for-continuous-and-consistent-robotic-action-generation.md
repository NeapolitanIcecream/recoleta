---
source: arxiv
url: https://arxiv.org/abs/2606.20135v1
published_at: '2026-06-18T11:58:30'
authors:
- Jianing Guo
- Fangzheng Chen
- Zihao Mao
- Wong Lik Hang Kenny
- Zhenhong Wu
- Yu Li
- Yishuai Cai
- Yuanpei Chen
- Yikun Ban
- Kai Chen
- Qi Dou
- Yaodong Yang
- Xianglong Liu
- Huijie Zhao
- Simin Li
topics:
- flow-matching
- frequency-domain-actions
- vision-language-action
- temporal-smoothness
- robot-action-generation
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Frequency-Aware Flow Matching for Continuous and Consistent Robotic Action Generation

## Summary
## 摘要
FAFM 将流匹配机器人策略从预测固定离散动作块改为预测 DCT 频率系数，然后以任意控制频率重建连续动作。它的目标是在不增加网络参数的情况下生成更平滑、更稳定的机器人动作。

## 问题
- 固定动作块会丢失控制频率信息；这很关键，因为机器人数据集可能混合不同采样率的演示，例如 Open X-Embodiment 中 3 Hz 的 RT-1 和 50 Hz 的 ALOHA。
- 按步索引的训练可能把同一索引映射到不同物理时间，导致同一观测对应相互冲突的监督信号。
- 逐步独立预测动作可能在相邻动作之间产生抖动，从而影响倒液或外科操作等软体任务。

## 方法
- FAFM 将每个演示块转换为绑定物理时间的 DCT 系数，使目标描述轨迹形状，而非固定步索引。
- 流匹配在系数空间中运行：模型学习从噪声到目标系数向量的速度场。
- 预测系数通过余弦基解码为连续轨迹，因此策略可以按任意时间分辨率输出动作。
- 导数损失监督解码动作的解析一阶时间导数。该项惩罚高频系数误差，并减少突变动作。
- 该方法对导数项使用 λ=1，且不增加额外网络或可学习参数。论文将其用于独立流匹配策略和 VLA 动作头。

## 结果
- 在避障任务上，FAFM 报告 SR 61、LDLJ -5.60±1.08、12 个轨迹模式。基线包括 FM：SR 48、LDLJ -8.62±0.69、M=14；DP：SR 35、LDLJ -9.16±0.77、M=8；SFP：SR 49、LDLJ -6.98±0.82、M=3；MPD：SR 16、LDLJ -6.78±0.47、M=2；FreqPolicy：SR 39、LDLJ -9.02±1.11、M=10。
- 在合成双模式正弦基准上，论文称 FAFM 是唯一能分离两个模式并保持轨迹平滑的方法。摘录没有提供该基准的数值指标。
- 在 LapGym 穿绳任务上，可见表格报告 FAFM 的 SR 为 97、LDLJ 为 -7.57±1.32。可见基线中最高的 SR 是 MPD 的 94，DP 报告 92，SFP 72，FreqPolicy 89，FM 89。
- 在 LapGym 任务上，论文称 FAFM 在穿绳、抓取-抬起-触碰、双手组织操作和打结环任务上取得最高成功率和平滑度，并且比所有列出的基线收敛更快。摘录被截断，因此三个任务的完整 FAFM 数值不可见。
- 论文还称，FAFM 在使用 VLA 骨干的 LIBERO 上以及真实 Franka 机器人上带来提升，包括更平滑的运动，以及更好地处理机械偏差和混合频率输入。摘录不包含相关定量表格。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20135v1](https://arxiv.org/abs/2606.20135v1)
