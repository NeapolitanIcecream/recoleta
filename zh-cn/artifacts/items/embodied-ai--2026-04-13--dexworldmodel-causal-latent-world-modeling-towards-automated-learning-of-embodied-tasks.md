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
DexWorldModel 提出了一种用于机器人操作的世界模型：它预测语义视觉特征而不是像素，用固定大小的测试时记忆保存历史，并将推理与机器人执行重叠进行。论文关注长时程具身控制和零样本仿真到现实迁移。

## 问题
- 现有用于操作的世界-动作模型通常预测像素或低层潜变量，这会把模型容量花在纹理、光照和背景细节上，而不是与任务相关的交互动力学上。
- 标准自回归 Transformer 保留会随序列长度增长的 KV cache，导致内存使用为 **O(T)**，并且在长时程任务上推理更慢。
- 闭环部署还会被顺序推理拖慢：机器人先执行动作，等待下一次观测，然后才开始下一步代价高的去噪。

## 方法
- CLWM 用 **DINOv3 特征空间**中的预测替代像素重建。简单说，它先预测下一次观测的语义潜变量，再预测到达该潜在状态所需的动作块。
- 模型对潜变量视频预测和动作预测共用一个 Transformer 主干，并用 **flow matching** 分两阶段训练：先预测未来潜变量特征，再预测动作。
- 为了避免内存随时域长度增长，它用 **Dual-State Test-Time Training memory** 替代 Transformer 的 KV cache。一个长期状态通过在线权重更新存储真实观测历史，另一个工作状态在生成时分叉出来，用于保存临时预测的未来上下文。
- 为了提高部署速度，**Speculative Asynchronous Inference** 会在当前动作仍在执行时就开始下一步的部分去噪，然后在真实观测到达后进行校准。
- 论文还引入了 **EmbodiChain**，这是一个用于后训练的在线仿真数据流，目的是持续加入新的基于物理的轨迹，并提升策略的扩展效果。

## 结果
- 摘要称该方法在**复杂双臂仿真**基准上达到 **state-of-the-art performance**，但给出的摘录没有提供任务成功率、数据集表格或相对基线的具体优势。
- 论文报告 **Speculative Asynchronous Inference 将阻塞延迟降低约 50%**，引言中提到了 **RoboTwin**，并将这一延迟结果与 **Lingbot VA** 对比。
- 该方法声称，在长时程操作中，用测试时更新的记忆权重替代常见的 **O(T)** KV-cache 增长后，可以实现严格的 **O(1) memory footprint**。
- 摘要称该方法在物理机器人上实现了**零样本仿真到现实迁移**，并且优于那些**在真实世界数据上 finetuned** 的基线，但摘录没有给出具体成功率、任务数量或机器人设置。
- 除了报告的 **约 50% 延迟下降** 以及陈述的 **O(1)** 对 **O(T)** 内存扩展差异外，摘录没有包含足够的定量证据来验证这些完整的性能说法。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16484v1](http://arxiv.org/abs/2604.16484v1)
