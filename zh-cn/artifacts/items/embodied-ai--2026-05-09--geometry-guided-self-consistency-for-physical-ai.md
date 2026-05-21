---
source: arxiv
url: https://arxiv.org/abs/2605.08638v1
published_at: '2026-05-09T03:14:30'
authors:
- Yinwei Dai
- Zhuofu Chen
- Lijie Yang
- Ravi Netravali
topics:
- vision-language-action
- robot-foundation-model
- world-action-model
- diffusion-policy
- test-time-scaling
- robot-manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Geometry Guided Self-Consistency for Physical AI

## Summary
## 摘要
KeyStone 通过在推理时采样多个动作块，并选择最大动作空间簇中最居中的动作块，改进了带随机性的扩散和流匹配机器人动作生成。在 VLA 和 WAM 操作基准上，它报告的成功率最高提升 13.3 个百分点，且每轮延迟增加很小。

## 问题
- 扩散和流匹配机器人策略在每个控制轮生成一个开环动作块；一次不好的随机采样可能让整个 episode 偏离目标，误差会在多轮中累积。
- TACO 等现有多样本选择器需要为每个任务或机体形态训练额外评分器，增加训练成本和推理次数。
- 机器人部署需要在严格延迟限制下做出可靠的逐轮动作选择。

## 方法
- KeyStone 从同一观察、机器人状态和指令上下文中抽取 K 个独立动作块。
- 它将每个动作块展平并计算两两 L2 距离，把动作空间距离用作机器人运动相似性的度量。
- 如果样本看起来是单峰的，它返回全局 medoid；否则运行小规模 k-means 聚类，找到最大簇，并执行该簇的 medoid。
- 被选中的动作块是一个真实的模型样本，因此该方法避免了在动作模式之间做平均。
- 它在共享编码上下文或缓存张量的同时批处理 K 条扩散链；论文对 K 做了性能分析，并对 GR00T N1.6 和 X-VLA 使用 K=4，对其他测试模型使用 K=16。

## 结果
- 在使用 GR00T N1.6 的 SimplerEnv-WidowX 上，K=4 时成功率从 50.0 ± 4.3% 升至 63.3 ± 2.9%，提升 +13.3 个百分点。
- 在使用 GR00T N1.6 的 SimplerEnv-Google Robot 上，K=4 时成功率从 79.4 ± 3.5% 升至 86.7 ± 1.5%，提升 +7.3 个百分点。
- 在使用 SmolVLA 的 LIBERO 上，K=16 时成功率从 50.4 ± 2.1% 升至 57.2 ± 1.3%，提升 +6.8 个百分点；使用 π0.5 时，LIBERO 从 96.8 ± 0.7% 升至 97.8 ± 1.1%，提升 +1.0 个百分点。
- 在 SimplerEnv-WidowX 上，StarVLA 在 K=16 时从 52.8 ± 1.6% 升至 59.7 ± 1.3%，提升 +6.9 个百分点；X-VLA 在 K=4 时从 92.7 ± 1.0% 升至 95.8 ± 1.0%，提升 +3.1 个百分点。
- 在使用 Fast-WAM 的 RoboTwin 2.0 上，K=16 时成功率从 90.0 ± 1.5% 升至 93.0 ± 1.0%，提升 +3.0 个百分点；这是 WAM 测试案例。
- 论文称，KeyStone 在无需训练选择器的情况下，达到与 TACO 等基于模型的选择器相当的准确率。论文还报告，在 K 取 {1,4,8,16} 时，每轮延迟和峰值 GPU 内存保持稳定，但摘录没有给出具体延迟值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08638v1](https://arxiv.org/abs/2605.08638v1)
