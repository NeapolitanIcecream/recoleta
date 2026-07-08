---
source: arxiv
url: https://arxiv.org/abs/2607.06370v1
published_at: '2026-07-07T15:10:15'
authors:
- Ryuji Oi
- Hikari Otsuka
- Kosuke Matsushima
- Yuki Ichikawa
- Masato Motomura
- Tatsuya Kaneko
- Daichi Fujiki
topics:
- vision-language-action
- robot-policy-acceleration
- action-caching
- flow-matching
- robot-manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Training-Free Acceleration for Vision-Language-Action Models with Action Caching and Refinement

## Summary
## 摘要
ActionCache 通过检索过去的动作片段，并用很少或零个动作头步骤进行细化，加速基于 flow 的视觉-语言-动作模型。它面向实时机器人控制场景，在这类场景中，迭代式 flow matching 会带来较高的推理延迟。

## 问题
- 基于 flow 的 VLA 模型通过反复评估动作头来生成连续动作片段，这会拖慢闭环机器人控制。
- 论文报告称，在代表性 VLA 模型上，动作头占端到端延迟的 37-66%。
- 直接减少 NFE 会降低任务成功率，因为模型从噪声开始，细化步骤太少。

## 方法
- ActionCache 存储成功的历史生成中的中间动作片段，并将其与紧凑键配对；这些键由 VLM 输出嵌入构建，对于 GR00T-N1.6，还会加入编码后的机器人状态特征。
- 推理时，它将当前多模态上下文投影为 500 维稀疏随机键，并通过余弦相似度检索最近的缓存条目。
- 如果相似度超过阈值，系统会直接执行检索到的动作片段，或在当前上下文下用 1-2 个 flow 步骤进行细化。
- 如果相似度过低，系统会退回到原始的从高斯噪声开始的完整步数生成。
- 该方法不需要重新训练，也不改变 VLA 主干或动作头。

## 结果
- 在使用 π0.5 的 VLABench 上，完整基础模型达到 38.8% 成功率，动作头延迟为 18.8 ms。NFE=0 的 ActionCache 达到 32.9% 成功率，延迟为 1.6 ms，加速 11.75 倍。
- 在使用 GR00T-N1.6 的 VLABench 上，完整基础模型达到 34.0% 成功率，延迟为 24.1 ms。NFE=0 的 ActionCache 达到 22.3% 成功率，延迟为 0.7 ms，加速 34.43 倍。
- 使用 π0.5 且 NFE=1 时，直接减少 NFE 得到 6.8% 成功率、2.5 ms 延迟；ActionCache 得到 32.4% 成功率、3.6 ms 延迟，相比完整生成加速 5.22 倍。
- 使用 GR00T-N1.6 且 NFE=2 时，ActionCache 达到 35.7% 成功率、13.4 ms 延迟，略高于 34.0% 的完整基础模型成功率，并加速 1.79 倍。
- 与 π0.5 上的 EfficientVLA 相比，ActionCache 在低延迟设置下表现更好：NFE=1 时，EfficientVLA 得到 2.3% 成功率、5.1 ms 延迟，ActionCache 得到 32.4% 成功率、3.6 ms 延迟。
- 在跨任务 VLABench 测试中，用 select_fruit 构建的缓存在 select_painting 上得到 20.0% 进度分数，在 select_toy 上得到 51.7% 进度分数，接近基础模型的 21.0% 和 50.5%；缓存命中率分别为 2.7% 和 8.1%，在 episode 早期时间步的命中率超过 80%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06370v1](https://arxiv.org/abs/2607.06370v1)
