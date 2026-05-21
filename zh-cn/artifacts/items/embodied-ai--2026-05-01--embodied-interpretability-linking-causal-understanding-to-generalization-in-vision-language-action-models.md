---
source: arxiv
url: https://arxiv.org/abs/2605.00321v1
published_at: '2026-05-01T01:00:00'
authors:
- Hanxin Zhang
- Mingshuo Xu
- Abdulqader Dhafer
- Shigang Yue
- Hongbiao Dong
- Zhou Daniel Hao
topics:
- vision-language-action
- embodied-interpretability
- robot-policy
- causal-attribution
- ood-generalization
- manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Embodied Interpretability: Linking Causal Understanding to Generalization in Vision-Language-Action Models

## Summary
## 摘要
本文提出 ISS 和 NMR 两个诊断指标，用于检查视觉-语言-动作（VLA）策略的动作依据是任务相关图像区域，还是干扰区域。论文称，较高的干扰归因会预测更差的分布外操作表现。

## 问题
- VLA 策略在依赖背景、纹理、阴影或其他虚假视觉线索时，可能在分布偏移下失败，而任务真正需要的是机器人、物体和支撑物等信息。
- 注意力图和隐藏状态探针可以显示信息出现的位置，但不能证明某个区域会改变策略的动作。
- 这个问题很重要，因为依赖干扰线索的机器人策略可能通过已见任务测试，却在场景变化后失败。

## 方法
- 论文把视觉-动作归因视为一个干预问题：遮蔽或模糊图像 token，重新运行 VLA 策略，并测量预测动作的变化幅度。
- Interventional Significance Score（ISS）会给移除后导致动作大幅变化的视觉区域分配较高显著性。其实现使用随机二值掩码、模糊替换，并在固定各向同性高斯策略下用动作 MSE 作为 KL 散度的代理指标。
- Nuisance Mass Ratio（NMR）衡量 top-k ISS 显著性中有多少落在任务无关区域内，例如背景、墙面颜色、反射和干扰物体。
- 论文将视觉 token 划分为动作关键区域、环境支撑区域和干扰区域，然后把干扰归因视为策略学习到虚假依赖的证据。

## 结果
- 在使用 RLBench 评估的 AGNOSTOS 上，VLA 策略用 3,600 个已见任务 episode 进行微调，并用 575 个未见任务 episode 评估。
- 未见集合分为 U1 和 U2：U1 包含 13 个部分重叠的任务，U2 包含 10 个使用新物体或新动作的任务。
- 在 41 个任务、5 个随机种子、每个任务 25 次试验中，NMR@10 与任务成功率的 Pearson 相关系数为 -0.77，说明更高的干扰归因对应更低的成功率。
- 在一项噪声测试中，研究对 200 个选定 episode 的干扰区域施加标准差为 0.25 的高斯噪声；ISS 达到动作 MSE 0.002，显著性余弦相似度 0.995。
- 在同一测试中，注意力显著性达到动作 MSE 0.002、余弦相似度 0.959；token-norm 显著性达到动作 MSE 0.011、余弦相似度 0.999。
- 论文还称，ISS 有无偏估计量，并且在给定的高斯策略假设下，动作预测误差可作为因果影响的有效代理指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00321v1](https://arxiv.org/abs/2605.00321v1)
