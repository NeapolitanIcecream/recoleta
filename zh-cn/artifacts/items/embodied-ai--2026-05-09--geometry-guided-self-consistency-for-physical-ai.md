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
KeyStone 通过在推理时采样多个动作块，并在动作空间最大的簇中选择最居中的那个块，提升了基于扩散和 flow-matching 的机器人动作生成表现。论文报告，在多个 VLA 和 WAM 操作基准上，成功率最高提升 13.3 个百分点，而每轮额外延迟很小。

## 问题
- 扩散和 flow-matching 机器人策略在每个控制回合只生成一个开放环动作块；一次随机采样出错就可能带偏整个任务，而且误差会在多轮回合中累积。
- TACO 这类现有的多样本选择器需要针对每个任务或本体额外训练一个评分器，会增加训练成本和推理次数。
- 机器人部署需要在严格的延迟限制下，稳定地做出每轮动作选择。

## 方法
- KeyStone 会从同一观察、机器人状态和指令上下文中抽取 K 个独立动作块。
- 它会把每个块展开，计算两两 L2 距离，用动作空间距离来衡量机器人运动是否相似。
- 如果样本看起来是单峰分布，它就返回全局 medoid；否则先做小规模 k-means 聚类，找出最大簇，再执行该簇的 medoid。
- 选中的块是模型实际采样得到的结果，所以这种方法不会在不同动作模式之间做平均。
- 它把 K 条 diffusion 链批量执行，同时共享编码后的上下文或缓存张量；论文对 K 做了分析，并在 GR00T N1.6 和 X-VLA 上使用 K=4，在其他测试模型上使用 K=16。

## 结果
- 在 SimplerEnv-WidowX 上，GR00T N1.6 的成功率从 50.0 ± 4.3% 提高到 63.3 ± 2.9%，K=4，提升 13.3 个百分点。
- 在 SimplerEnv-Google Robot 上，GR00T N1.6 的成功率从 79.4 ± 3.5% 提高到 86.7 ± 1.5%，K=4，提升 7.3 个百分点。
- 在 LIBERO 上，SmolVLA 的成功率从 50.4 ± 2.1% 提高到 57.2 ± 1.3%，K=16，提升 6.8 个百分点；π0.5 的 LIBERO 成功率从 96.8 ± 0.7% 提高到 97.8 ± 1.1%，提升 1.0 个百分点。
- 在 SimplerEnv-WidowX 上，StarVLA 的成功率从 52.8 ± 1.6% 提高到 59.7 ± 1.3%，K=16，提升 6.9 个百分点；X-VLA 从 92.7 ± 1.0% 提高到 95.8 ± 1.0%，K=4，提升 3.1 个百分点。
- 在 RoboTwin 2.0 上，Fast-WAM 的成功率从 90.0 ± 1.5% 提高到 93.0 ± 1.0%，K=16，提升 3.0 个百分点；这是 WAM 测试案例。
- 论文称，KeyStone 在不训练选择器的情况下，能达到与 TACO 这类基于模型的选择器相当的准确率。论文还报告了 K 取 {1,4,8,16} 时每轮延迟和 GPU 峰值显存保持稳定，但摘录没有给出具体延迟值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08638v1](https://arxiv.org/abs/2605.08638v1)
