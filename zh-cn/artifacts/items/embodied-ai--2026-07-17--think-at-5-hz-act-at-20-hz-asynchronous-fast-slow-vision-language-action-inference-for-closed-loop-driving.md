---
source: arxiv
url: https://arxiv.org/abs/2607.15621v1
published_at: '2026-07-17T04:40:02'
authors:
- Yun Li
- Jiachen Gong
- Simon Thompson
- Ehsan Javanmardi
- Qunli Zhang
- Zifan Zeng
- Shiming Liu
- Peng Wang
- Zixuan Guo
- Manabu Tsukada
topics:
- vision-language-action
- robot-foundation-model
- embodied-foundation-model
- real-time-inference
- closed-loop-driving
- sim2real
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Think at 5 Hz, Act at 20 Hz: Asynchronous Fast-Slow Vision-Language-Action Inference for Closed-Loop Driving

## Summary
## 摘要
论文提出了一种用于闭环驾驶的异步快慢视觉-语言-动作系统：冻结的 7B 骨干网络缓慢更新缓存的场景表示，而一个 3.37 亿参数的动作专家在每个控制时刻预测航点。在 CARLA 中，该系统消除了陈旧指令的重复执行，使路线完成率从 37.0 提升至 94.0，但长路线安全性仍然较弱。

## 问题
- 大型视觉-语言骨干网络无法在车辆控制预算内重新计算视觉历史，因此 LMDrive 以 10 Hz 生成新决策，并在间隔的 20 Hz 控制时刻重复执行已有指令。
- 基于 50–100 ms 之前观测结果进行控制，可能导致路线偏离、超时和错过交通事件，使延迟成为闭环控制问题，而不仅是推理速度问题。
- 这项研究的意义在于检验：经过语言条件化的驾驶智能体能否在消费级硬件上保持场景推理能力，同时持续输出新鲜控制信号。

## 方法
- 冻结的 LLaMA-7B 视觉-语言骨干网络每经过四个 20 Hz 控制时刻处理一次指令和视觉历史，并将其逐层键值缓存作为持久化的场景表示。
- 一个 3.37 亿参数的 Transformer 动作专家在每个控制时刻对该缓存和当前摄像头画面执行交叉注意力，然后在一次前向传播中预测五个航点。
- 随机陈旧度训练会隐藏骨干网络历史中随机延迟的部分，训练动作专家将陈旧上下文、当前视觉证据和前一次预测结合起来。
- 增量式缓存更新使每个控制时刻的模型成本几乎不受历史长度影响；该系统在 RTX 3090 Ti 上运行，据报告每个控制时刻的模型成本为 32.4 ms。

## 结果
- 在 CARLA town05 的 32 条 LangAuto-Short 路线上，路线完成率从以 10 Hz 重复执行控制指令的 LMDrive 的 37.0 ± 0.4 提升至所提 20 Hz 系统的 94.0 ± 2.6；驾驶得分从 28.8 ± 0.8 提升至 32.9 ± 0.7。
- 让同一个动作专家以基线的 10 Hz 频率运行时，路线完成率达到 82.1，这表明进一步提升至 94.0 的主要来源是每个控制时刻都使用最新观测；路线偏离次数从每公里 11.3 次降至 4.3 次，闯红灯次数从 10.4 次降至 6.9 次。
- 使用随机陈旧度时，开放环路航点 L1 误差为 0.031 m；无陈旧度训练的动作专家为 0.037 m，冻结骨干网络的动作头为 0.123 m。
- 从 town05 零样本迁移到未见过的 town01 和 town02 后，路线完成率分别为 84.3% 和 94.4%；LMDrive 分别为 40.5% 和 30.7%。
- 在未见过的 town03 中执行八条长路线时，该系统完成了 85.4% 的路线，但驾驶得分仅为 2.96，因为碰撞和闯红灯使其惩罚因子降至 0.04；因此，作者并未证明其具备长时域安全性或上路可用性。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15621v1](https://arxiv.org/abs/2607.15621v1)
