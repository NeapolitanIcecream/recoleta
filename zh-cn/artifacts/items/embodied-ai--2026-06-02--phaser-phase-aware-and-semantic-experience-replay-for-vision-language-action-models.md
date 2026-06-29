---
source: arxiv
url: https://arxiv.org/abs/2606.03598v1
published_at: '2026-06-02T13:04:15'
authors:
- Ziyang Chen
- Shaoguang Wang
- Weiyu Guo
- Qianyi Cai
- He Zhang
- Pengteng Li
- Yiren Zhao
- Yandong Guo
topics:
- vision-language-action
- continual-learning
- experience-replay
- robot-manipulation
- catastrophic-forgetting
- libero-benchmark
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# PHASER: Phase-Aware and Semantic Experience Replay for Vision-Language-Action Models

## Summary
## 摘要
PHASER 通过把回放记忆从按帧均匀存储改为按阶段感知的存储，并按阶段级别进行回放路由，提升了视觉-语言-动作机器人策略的持续学习效果。它针对 LIBERO 顺序操作任务中的灾难性遗忘，在 3 个 VLA 骨干模型上报告了明显的 ASR 提升。

## 问题
- 当 VLA 机器人策略在一串新的语言条件任务上训练时，会遗忘早先的操作任务。
- 均匀经验回放按阶段长度存储帧，因此像抓取这类接触密集但很短的阶段，可能只得到很少样本。
- 均匀回放也会把内存分给旧任务，但不会检查哪些过去阶段最可能与当前任务发生冲突。

## 方法
- PHASER 把每条轨迹拆成接近、抓取、搬运等子技能阶段。
- 每个阶段获得相同的帧预算，阶段内使用步长为 3 的时间下采样和 reservoir sampling。
- 回放路由器用语言相似度、视觉相似度和动作偏差，对旧阶段与当前阶段打分。
- 回放采样对缓存的阶段分数使用 Boltzmann 分布，在每次任务切换时计算一次，因此内循环回放开销与标准 ER 相当。
- Auto-PC 可以用动作信号变点检测，再加上 VLM 语义验证，替代人工阶段标签。

## 结果
- 在 LIBERO-Goal 上，使用 OpenVLA-OFT-7B 时，PHASER 的 ASR 达到 87.8%，NBT 为 7.8；ER 的 ASR 为 77.6%，NBT 为 22.2。
- 在 LIBERO-Long 上，使用 OpenVLA-OFT-7B 时，PHASER 的 ASR 达到 85.8%；ER 为 54.6%，MIR 为 82.2%。
- 在主表中，PHASER 相比 ER 的 ASR 提升为 +10.2 到 +39.6 个百分点，具体取决于骨干模型和套件；摘要报告在匹配预算的 ER 上最高提升 +31 个百分点。
- 在 QwenGR00T-3B 上，PHASER 将 LIBERO-Goal ASR 从 51.6% 提升到 78.0%，将 LIBERO-Long ASR 从 31.4% 提升到 48.6%，相较 ER。
- 在 QwenOFT-3B 上，PHASER 将 LIBERO-Goal ASR 从 39.4% 提升到 79.0%，将 LIBERO-Long ASR 从 33.0% 提升到 51.6%，相较 ER。
- Auto-PC 的阶段发现结果与 LIBERO-Long 上的人工阶段标签接近：OpenVLA-OFT-7B 为 89.6 对 85.8 的 ASR，QwenGR00T-3B 为 48.0 对 48.6，QwenOFT-3B 为 49.0 对 51.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03598v1](https://arxiv.org/abs/2606.03598v1)
