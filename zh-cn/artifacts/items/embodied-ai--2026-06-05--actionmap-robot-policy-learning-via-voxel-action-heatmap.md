---
source: arxiv
url: https://arxiv.org/abs/2606.06904v1
published_at: '2026-06-05T04:42:56'
authors:
- Pei Yang
- Hai Ci
- Yanzhe Chen
- Qi Lv
- Han Cai
- Mike Zheng Shou
topics:
- vision-language-action
- robot-policy-learning
- action-decoder
- voxel-heatmap
- data-efficiency
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ActionMap: Robot Policy Learning via Voxel Action Heatmap

## Summary
## 总结
ActionMap 用覆盖平移、旋转和夹爪动作的体素热图，替换了视觉-语言-动作机器人策略里的单点动作解码器。它在 LIBERO 和真实 Franka 任务上报告了更高的成功率、更快的训练速度，以及更好的低数据表现，而且没有改动 VLA 主干。

## 问题
- 目前的 VLA 动作解码器通常通过 token 分箱、L1 回归或流匹配输出一个动作点，因此训练时会丢掉邻近动作的几何关系。
- 这对机器人操作很重要，因为末端执行器的微小误差就可能导致抓取、扫掠或插入失败。
- 论文测试的是，动作表示本身是否能改善 VLA 策略，而不是依赖更大的主干或更多机器人数据。

## 方法
- ActionMap 是一个可直接替换的 MLP 动作头，读取 VLA 的动作 token 隐状态，替换原生解码器。
- 这个头分别预测 3D 平移、3D 旋转和二值夹爪指令的概率网格。
- 训练时，把每个真实动作转换成体素网格上的软高斯团块，并用交叉熵和预测热图对齐。
- 推理时，主实验使用 top-k soft argmax 恢复连续动作，其中 k=10、温度为 1.0；夹爪使用 argmax。
- 论文把这个头接入 OpenVLA-OFT 和 pi0.5，其余部分保持不变。

## 结果
- 在 LIBERO 上，ActionMap 将 OpenVLA-OFT 的 L1 回归在四套任务上的平均成功率从 89.1% 提高到 97.3%，在相同的 10K 训练步数下提升 8.2 个百分点。
- 在使用 pi0.5 的 LIBERO 上，它把四套任务平均值从 96.9% 提高到 98.5%，在相同的 30K 训练步数下提升 1.6 个百分点。
- 在 LIBERO-Long 上，最大的提升是 OpenVLA-OFT 的 26.6 个百分点和 pi0.5 的 4.8 个百分点。
- 在 LIBERO-Spatial 10% 数据量下，也就是 43 条示范时，ActionMap 达到 93.2%，而 OpenVLA-OFT 的 L1 回归只有 67.2%，差距为 26.0 个百分点。
- 在真实 Franka 任务上、使用全部数据时，ActionMap 在 30 次试验中成功 20 次，而 OpenVLA-OFT 的 L1 回归只有 7 次；每个任务只用 50 条示范时，它达到 14/30，而后者是 4/30。
- 在 Franka Pick 任务上，ActionMap 在全部数据时的抓取位置误差为 4.8 毫米，在 50 条示范时为 15.0 毫米，误差大约比 L1 回归头低 2 到 3 倍。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06904v1](https://arxiv.org/abs/2606.06904v1)
