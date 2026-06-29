---
source: arxiv
url: http://arxiv.org/abs/2604.16484v1
published_at: '2026-04-13T03:19:36'
authors:
- Yueci Deng
- Guiliang Liu
- Kui Jia
topics:
- world-model
- vision-language-action
- sim2real
- dexterous-manipulation
- test-time-training
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# DexWorldModel: Causal Latent World Modeling towards Automated Learning of Embodied Tasks

## Summary
## 摘要
DexWorldModel 提出了一种用于机器人操作的世界模型，用语义视觉特征而不是像素来做预测，用固定大小的测试时内存保存历史，并把推理和机器人执行重叠起来。论文面向长时程具身控制和零样本仿真到现实迁移。

## 问题
- 现有用于操作的 world-action 模型常常预测像素或低层潜变量，把模型容量花在纹理、光照和背景细节上，而不是任务相关的交互动态上。
- 标准自回归 Transformer 会保留随序列长度增长的 KV cache，导致内存使用为 **O(T)**，在长时程任务上的推理也更慢。
- 闭环部署会被串行推理拖慢：机器人先动作，等下一次观测，再开始下一步昂贵的去噪。

## 方法
- CLWM 用 **DINOv3 特征空间** 替代像素重建。简单说，它先预测下一次观测的语义潜变量，再预测到达该潜状态所需的动作片段。
- 模型用共享的 Transformer 骨干同时做潜变量视频预测和动作预测，分两阶段用 **flow matching** 训练：先预测未来潜特征，再预测动作。
- 为了避免内存随时域增长，它用 **Dual-State Test-Time Training memory** 替代 Transformer 的 KV cache。一个长期状态通过在线权重更新保存真实观测历史，另一个工作状态在生成时分叉出来，承载临时的未来预测上下文。
- 为了提高部署速度，**Speculative Asynchronous Inference** 会在当前动作还在执行时，先开始下一步的部分去噪，等真实观测到来后再做校准。
- 论文还提出 **EmbodiChain**，这是一个用于后训练的在线仿真数据流，目标是持续加入新的物理约束轨迹并提升策略扩展性。

## 结果
- 摘要声称在 **复杂双臂仿真** 基准上达到 **state-of-the-art**，但这段摘录没有给出任务成功率、数据表或精确的基线差距。
- 论文报告 **Speculative Asynchronous Inference 将阻塞延迟降低了约 50%**，引言中把这个结果放在 **RoboTwin** 上，并与 **Lingbot VA** 做了比较。
- 该方法声称通过用测试时更新的记忆权重替代通常的 **O(T)** KV-cache 增长，在长时程操作中实现了严格的 **O(1)** 内存占用。
- 摘要声称在真实机器人上的 **零样本仿真到现实迁移** 优于在真实世界数据上 **finetuned** 的基线，但摘录没有给出具体成功率、任务数量或机器人设置。
- 这段摘录提供的定量证据不足，无法验证完整性能主张，除了已报告的 **约 50%** 延迟下降以及 **O(1)** 对比 **O(T)** 的内存规模。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16484v1](http://arxiv.org/abs/2604.16484v1)
