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
本文提出 ISS 和 NMR 这两个诊断方法，用来检查 Vision-Language-Action 策略是否依据与任务相关的图像区域做出动作，还是依据无关区域做出动作。文中声称，更高的无关归因可以预测更差的分布外操作性能。

## 问题
- 当 VLA 策略依赖背景、纹理、阴影或其他虚假的视觉线索，而不是依赖机器人、物体和任务所需的支撑物时，它们会在分布偏移下失效。
- 注意力图和隐状态探针可以显示信息看起来出现在哪里，但不能证明某个区域真的改变了策略的动作。
- 这个问题很重要，因为依赖无关线索的机器人策略可能在见过的任务上通过测试，但在场景变化后失败。

## 方法
- 论文把视觉-动作归因看作一个干预问题：遮挡或模糊图像 token，重新运行 VLA 策略，然后测量预测动作变化了多少。
- Interventional Significance Score（ISS）会把那些移除后导致动作明显变化的视觉区域标为高显著性。实现中使用随机二值掩码、模糊替换，以及在固定各向同性高斯策略下用动作 MSE 作为 KL 散度的代理。
- Nuisance Mass Ratio（NMR）衡量 top-k ISS 显著性中有多少落在与任务无关的区域里，例如背景、墙面颜色、反光和干扰物体。
- 论文把视觉 token 分成动作关键区域、环境支撑区域和无关区域，然后把无关归因视为策略学到了虚假依赖的证据。

## 结果
- 在 AGNOSTOS 和 RLBench 评测中，VLA 策略在 3,600 个见过的任务 episode 上微调，并在 575 个未见任务 episode 上评估。
- 未见集合分成了 U1 和 U2：U1 包含 13 个部分重叠任务，U2 包含 10 个使用新物体或新动作的任务。
- 在 41 个任务、5 个随机种子、以及每个任务 25 次试验的设置下，NMR@10 与任务成功率的 Pearson 相关系数为 -0.77，说明无关归因越高，成功率越低。
- 在一个噪声测试中，对 200 个选定 episode 的无关区域施加标准差为 0.25 的高斯噪声后，ISS 的动作 MSE 为 0.002，显著性余弦相似度为 0.995。
- 在同一测试中，attention saliency 的动作 MSE 为 0.002，余弦相似度为 0.959，而 token-norm saliency 的动作 MSE 为 0.011，余弦相似度为 0.999。
- 论文还声称，ISS 存在无偏估计量，并且在文中给出的高斯策略假设下，动作预测误差可以作为因果影响的有效代理。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00321v1](https://arxiv.org/abs/2605.00321v1)
