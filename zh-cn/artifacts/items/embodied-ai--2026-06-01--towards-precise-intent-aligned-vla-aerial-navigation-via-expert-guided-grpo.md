---
source: arxiv
url: https://arxiv.org/abs/2606.02313v1
published_at: '2026-06-01T14:31:35'
authors:
- Tianyang Chen
- Wenjun Li
- Xin zhou
- Yuze Wu
- Fei Gao
topics:
- vision-language-action
- uav-navigation
- reinforcement-fine-tuning
- grpo
- sim2real
- intent-alignment
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Towards Precise Intent-Aligned VLA Aerial Navigation via Expert-Guided GRPO

## Summary
## 总结
EG-GRPO 通过把在线 rollout 和每个 GRPO 组中的一条专家轨迹结合起来，训练 VLA 无人机策略去遵循细粒度飞行指令。论文报告称，相比 SFT 基线，它在任务成功率和意图对齐上更高，同时并行仿真与推理也让 rollout 更快。

## 问题
- 监督微调需要昂贵的无人机轨迹数据，而且对 S 形绕行、环绕、上穿或下穿这类细致指令的监督很弱。
- 用在线 RL 做三维空中导航时，奖励稀疏，动作空间又很大，所以随机探索很难找到复杂飞行技能所需的有效轨迹。
- rollout 采集速度慢，因为串行循环里，RT-core GPU 上的物理仿真和计算 GPU 上的 VLA 推理会让硬件空转。

## 方法
- 策略从 OpenVLA-OFT 开始，动作限制为 4-DoF 无人机指令：Δx、Δy、Δz 和 Δψ。
- EG-GRPO 为每个轨迹组生成 G-1 条在线 rollout 和恰好 1 条基于规则的专家轨迹，使用 ρ = 1/G。专家样本让组内奖励方差仍可用于相对优势估计。
- 轨迹级奖励模型根据语言指令给整条飞行路径打分。评估器是一个 LLM，论文说它在 10K 条 rollout 轨迹上经过了认证无人机飞手检查，但摘录里没有一致率百分比。
- 系统使用 Isaac Lab 的向量化仿真，包含高保真场景、碰撞网格和无人机运动学模型。
- 双缓冲流水线通过 Ray 和 SSH 隧道，把仿真放在 NVIDIA L20 工作站上运行，把 VLA 推理放在 NVIDIA A100 服务器上并行运行。

## 结果
- 总体上，OpenVLA-OFT 的 SFT 从 26.1% SR 和 4.50 IAS 提升到 55.6% SR 和 7.24 IAS，使用 EG-GRPO 后达到这一结果。相比 SFT 基线，成功率提高了 2.13 倍，IAS 提高了 60.9%。
- 在简单任务上，OpenVLA-OFT 从 33.5% SR 和 5.19 IAS 提升到 68.2% SR 和 8.28 IAS，SR 增加 34.7 个百分点，IAS 增加 3.09。
- 在困难任务上，OpenVLA-OFT 从 18.7% SR 和 3.81 IAS 提升到 43.1% SR 和 6.20 IAS，SR 增加 24.4 个百分点，IAS 增加 2.39。
- 与 π0 的整体结果相比，该方法报告为 55.6% SR 和 7.24 IAS，对比 32.0% SR 和 5.31 IAS。
- 在困难任务的消融实验中，不注入专家的 GRPO 达到 26.4% SR 和 4.66 IAS。EG-GRPO 达到 43.1% SR 和 6.20 IAS，比 GRPO 增加了 16.7 个百分点的 SR 和 1.54 的 IAS。
- 并行 rollout 流水线把每步 rollout 时间从 904.67 s 降到 511.01 s，减少了 43.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.02313v1](https://arxiv.org/abs/2606.02313v1)
