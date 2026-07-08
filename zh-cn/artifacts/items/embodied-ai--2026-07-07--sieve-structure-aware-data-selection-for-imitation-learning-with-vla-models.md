---
source: arxiv
url: https://arxiv.org/abs/2607.06442v1
published_at: '2026-07-07T16:10:02'
authors:
- Changti Wu
- Bin Yu
- Zhaolong Shen
- Shijie Lian
- Xiaopeng Lin
- Cong Huang
- Zhirui Zhang
- Lei Zhang
- Kai Chen
topics:
- vision-language-action
- imitation-learning
- robot-data-scaling
- data-selection
- vla-models
- robot-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models

## Summary
## 摘要
SIEVE 通过保留可复用的行为结构和中心样本，为 VLA 模仿学习选择更小、更干净的机器人演示子集。在 Bridge-V2 上配合 Qwen3-VL-4B-GR00T 使用时，它只使用 50% 的演示和 50% 的训练步数，就超过了全数据训练。

## 问题
- VLA 策略通常在大规模机器人演示集上训练，但这些数据集常包含重复轨迹、带噪声的动作、质量较差的演示，以及不均衡的任务覆盖。
- 现有选择方法通常给整条轨迹或单个状态-动作对打分，可能漏掉长时程任务中反复使用的中层行为单元。
- 这会影响训练效率，因为行为克隆可能把算力用在重复或不一致的监督信号上；如果保留了合适的行为覆盖，更小的已选数据集可以更快完成训练。

## 方法
- SIEVE 在夹爪或手部状态翻转处切分每条轨迹，并使用 5 帧持续规则来避免抖动边界。
- 它用 V-JEPA2 编码每个片段，每个片段采样 8 帧，拼接起始、中间和结束特征，并用 PCA 将特征降到 256 维。
- 它用 MiniBatch K-Means 对片段特征聚类，以发现可复用的视觉-运动原语，然后把每条轨迹表示为有序的原语序列。
- 它使用结构暴露目标在原语序列桶之间分配选择预算；该目标奖励对复用原语和相邻转移的覆盖，并采用收益递减。
- 在每个桶内，它根据拼接片段特征的余弦相似度，选择最接近 medoid 的轨迹，使入选演示成为适合行为克隆的中心样本。

## 结果
- 在 Bridge-V2 上，SIEVE 使用 50% 的选择预算、26.5K 条演示和 25K 个训练步，在 SimplerEnv-WidowX 上达到 56.3% 的平均成功率，高于使用 50K 步的全数据训练结果 51.8%。
- 在同样的 50% 数据和 25K 步设置下，SIEVE 的平均成功率超过 Random 的 39.6%、DemInf 的 43.2% 和 SCIZOR 的 52.2%。
- 使用 50% 数据和 50K 个训练步时，SIEVE 达到 59.4% 的平均成功率；Random 为 40.4%，DemInf 为 46.6%，SCIZOR 为 55.5%。
- 使用 70% 的选择预算、37.1K 条演示和 35K 个训练步时，SIEVE 达到 62.3% 的平均成功率；Random 为 44.6%，DemInf 为 55.2%，SCIZOR 为 56.8%。
- 使用 70% 数据和 50K 步时，SIEVE 达到 62.5% 的平均成功率，高于 Random 的 46.9%、DemInf 的 57.1%、SCIZOR 的 58.1% 和全数据训练的 51.8%。
- 摘录还说明，实验覆盖 Bridge-V2、Fractal 和 GR00T-X-Sim，并使用两个 Qwen3-VL-4B VLA 变体；但所提供的定量表格对应的是 Bridge-V2 与 Qwen3-VL-4B-GR00T。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06442v1](https://arxiv.org/abs/2607.06442v1)
