---
source: arxiv
url: https://arxiv.org/abs/2605.21854v1
published_at: '2026-05-21T01:02:41'
authors:
- Zhi Liu
topics:
- vision-language-action
- robot-policy-alignment
- flow-matching
- dpo
- parameter-efficient-finetuning
- inference-optimization
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# CrossVLA: Cross-Paradigm Post-Training and Inference Optimization for Vision-Language-Action Models

## Summary
## 总结
CrossVLA 研究了自回归和流匹配视觉-语言-动作模型上的 DPO 后训练，并为连续动作块提供了一个实用的替代对数概率。它最强的结论是 DoRA+DPO 在 OpenVLA 的 LIBERO 任务上带来提升，以及一个负面结果：前缀 KV 缓存不是流匹配 VLA 的好加速目标。

## 问题
- VLA 后训练主要集中在像 OpenVLA 这样的自回归动作 token 模型上，而像 pi_0.5 这样的流匹配模型缺少 DPO 所需的廉价对数概率。
- 机器人策略适配需要能同时适用于离散 token 和连续动作骨干的方法，而不是完整重训。
- VLA 的推理加速工作常盯着前缀 KV 缓存，但流匹配策略把大部分时间花在动作去噪上。

## 方法
- 对流匹配 VLA，论文用采样时间点上的负流匹配 MSE 代替精确的块级对数似然，并把它作为标准 DPO 中的替代对数概率。
- 它为 OpenVLA 和 pi_0.5 定义了统一的 VLA 接口，涵盖对数概率、参考对数概率、采样、观测编码和动作生成。
- 它比较了 LoRA 和 DoRA 这两种参数高效的 DPO 适配器，其中 DoRA 分离了权重的幅度和方向。
- 它按阶段测量 pi_0.5 的推理延迟，并测试块级缓存和 token 级前缀 KV 缓存。
- 它还用 LIBERO 帧训练了一个冻结 SigLIP 投影头，结合多视角和时序 InfoNCE。

## 结果
- 在 LIBERO 4-suite 的 OpenVLA 上，DoRA+DPO 的平均成功率达到 73.2%，SFT 为 62.75%，在 600 次试验和 3 个环境随机种子上提升了 10.4 个百分点。
- 相比 OpenVLA SFT，DoRA+DPO 在各套任务上的提升分别是 Object +20.0 个百分点、Long-horizon +11.0 个百分点、Goal +8.0 个百分点、Spatial +2.7 个百分点；Object 在三个随机种子上都是 76.0%，每次都是 38/50。
- 在可比较的多随机种子结果里，DoRA 在 Object 上是 76% 对 75%，在 Goal 上是 78% 对 77%，在 Long-horizon 上是 64% 对 64%。
- 流匹配 DPO 替代项在 pi_0.5 上训练稳定；已完成的 LIBERO Spatial 和 Object 运行保持在 SFT 的饱和水平，分别是 100% 和 98%。
- pi_0.5 的延迟大约是每次 sample_actions 调用 280 ms：图像预处理约 5 ms，前缀前向约 60 ms，占 21.4%，10 步去噪循环约 220 ms，占 78.6%。
- 前缀式缓存对 pi_0.5 效果很差：块缓存让 LIBERO Spatial 的成功率从 50/50 降到 40/50，同时把总耗时从 1258 s 增加到 1796 s；token 级前缀缓存在缓存命中设置下报告了 0/1 和 0/2 的失败运行。投影头预训练在 6000 个 LIBERO 帧上达到 99.5% 的 k-NN recall@1，是随机基线的 36 倍。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21854v1](https://arxiv.org/abs/2605.21854v1)
