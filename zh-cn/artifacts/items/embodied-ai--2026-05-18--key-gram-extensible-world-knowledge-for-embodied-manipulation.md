---
source: arxiv
url: https://arxiv.org/abs/2605.18556v1
published_at: '2026-05-18T15:37:02'
authors:
- Jingjing Fan
- Siyuan Li
- Botao Ren
- Zhidong Deng
topics:
- vision-language-action
- robot-manipulation
- external-memory
- compositional-grounding
- world-knowledge
- real-world-robotics
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Key-Gram: Extensible World Knowledge for Embodied Manipulation

## Summary
## 摘要
Key-Gram 为 VLA 机器人策略加入了一个外部语言记忆模块，让可复用的任务知识可以通过指令短语检索出来，并注入到视觉推理层中。它在 RoboTwin2.0、LIBERO-Plus 和真实双臂操作任务上都报告了稳定的成功率提升。

## 问题
- VLA 和 world-action 模型常把指令知识和视觉状态推理混在同一个 backbone 里，这会削弱组合式操作中的指令落地。
- 为了学习新的对象、关系或任务而更新 backbone，可能会覆盖原有知识。这对部署后还要继续适应的机器人很重要。

## 方法
- 解析器把每条指令拆成一组固定的短 key-gram，例如对象关系、任务目标和子目标。
- 每个 key-gram 通过确定性的多头哈希映射到外部嵌入表中的行，从而让由指令派生的键可以进行 O(1) 查找。
- 检索到的记忆向量被投影到选定的 Transformer 层中，然后用逐 token 的门控决定哪些视觉 token 接收检索到的语言先验。
- 一个轻量的长跨度卷积先混合检索到的 key-gram 信息，再把它作为残差更新加到隐藏状态上。
- 同一套受记忆引导的 backbone 还会提供给未来视觉 latent head 和 flow-matching 动作专家，用于轨迹预测。

## 结果
- 在 RoboTwin2.0 的 50 任务平均上，pi0-KG 将 easy success 从 65.9% 提高到 80.3%（+21.9%），将 hard success 从 58.4% 提高到 75.6%（+29.5%）；pi0.5-KG 将 easy 从 82.7% 提高到 89.0%（+7.6%），将 hard 从 76.8% 提高到 84.4%（+9.9%）。
- 在从 LIBERO 向 LIBERO-Plus 的迁移中、且没有目标域微调时，pi0-KG 将 53.6% 提高到 72.8%（+35.8%），pi0.5-KG 将 83.9% 提高到 87.7%（+4.5%）。
- 在 LIBERO-Plus 微调后，pi0-KG 达到 88.5%，而 pi0 为 84.0%（+5.4%）；pi0.5-KG 达到 92.6%，而 pi0.5 为 90.4%（+2.4%）。
- 在真实世界长程双臂任务上，pi0-KG 将平均成功率从 69.3% 提高到 80.0%（+15.4%），pi0.5-KG 将 82.0% 提高到 88.7%（+8.1%）。
- 在真实世界扩展任务上，pi0-KG 将平均成功率从 72.4% 提高到 81.6%（+12.7%），未见配对的增益分别为 +34.6% 和 +41.7%；pi0.5-KG 将 80.0% 提高到 86.8%（+8.5%），未见配对的增益分别为 +18.8% 和 +21.2%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18556v1](https://arxiv.org/abs/2605.18556v1)
