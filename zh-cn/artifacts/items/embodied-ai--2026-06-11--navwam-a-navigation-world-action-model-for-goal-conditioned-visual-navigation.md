---
source: arxiv
url: https://arxiv.org/abs/2606.13494v1
published_at: '2026-06-11T15:44:36'
authors:
- Daichi Azuma
- Taiki Miyanishi
- Koya Sakamoto
- Shuhei Kurita
- Yaonan Zhu
- Petr Khrapchenkov
- Motoaki Kawanabe
- Yusuke Iwasawa
- Yutaka Matsuo
topics:
- visual-navigation
- world-model
- diffusion-policy
- goal-conditioned-control
- robot-learning
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# NavWAM: A Navigation World Action Model for Goal-Conditioned Visual Navigation

## Summary
## 摘要
NavWAM 通过把未来预测直接变成动作来解决目标条件视觉导航，让机器人在不需要单独规划器的情况下使用视觉前瞻。它之所以重要，是因为部分可观测条件下的导航既需要预测下一步视角，也需要选择动作，而以往的世界模型把这两件事分开了。

## 问题
- 目标条件图像导航必须基于部分可见的自我中心视角运行，所以机器人需要预测运动会如何改变它看到的内容，以及这种变化是否会让它更接近目标。
- 以往的导航世界模型会预测未来视图，但仍依赖 CEM 式规划或其他外部选择器来决定动作。
- 直接导航策略可以高效输出动作，但它们没有把未来自我中心预测和目标进度估计明确放进同一个模型里。

## 方法
- NavWAM 是一个基于 Cosmos Predict2 的扩散 Transformer 策略，把导航看作对一个潜在画布进行去噪。
- 这个画布包含已观察帧，以及针对动作块、未来状态、未来自我中心视图和目标进度值的预测帧。
- 模型把未来视图预测、动作生成和价值估计一起学习，而不是使用独立头部或外部规划器。
- 在测试时，它以策略模式运行，并在滚动时域循环中直接输出一个动作块。
- 它也支持可选的 best-of-N 采样，但主要结果使用的是默认策略模式，不做 CEM 式搜索。

## 结果
- 在 go stanford 上，NavWAM 的轨迹误差优于规划基线：ATE 为 0.324，而 NWM 为 0.453、Cosmos Predict2 为 0.455；RPE 为 0.099，而另外两者分别为 0.107 和 0.109。
- 在 go stanford 上微调后，NavWAM 的 ATE 达到 0.192，RPE 达到 0.070，论文把这作为它在该基准上的最佳导航结果。
- 把模型变成策略之后，未来预测仍然有用：在微调前，subject consistency 从 NWM 的 0.524 提高到 NavWAM 的 0.668；微调后为 0.635。
- 在 sit 上，NavWAM 在使用 2B 视频骨干而不是 OmniVLA 的 7B OpenVLA 骨干时，表现与 OmniVLA 接近；在 h=4 时，ATE 为 0.077 对 0.086，SR 为 46.3% 对 45.4%；在 h=8 时，ATE 为 0.144 对 0.162，SR 为 15.9% 对 12.1%。
- 在 24 个真实机器人测试回合中，NavWAM 在 19/24 个回合到达目标，成功率为 79.2%；OmniVLA 为 14/24，NWM 为 4/24。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13494v1](https://arxiv.org/abs/2606.13494v1)
