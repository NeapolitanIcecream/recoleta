---
source: arxiv
url: https://arxiv.org/abs/2606.07386v1
published_at: '2026-06-05T15:23:54'
authors:
- Mengze Tian
- Yiming Li
- Sichao Liu
- Auke Ijspeert
- Sylvain Calinon
topics:
- robot-imitation-learning
- spline-policy
- action-representation
- vision-language-action
- dexterous-manipulation
- flow-field-control
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Spline Policy: A Structured Representation for Robot Policies

## Summary
## 总结
Spline Policy 把机器人模仿策略的动作输出从固定长度的动作块改成样条参数，同时保持策略主干不变。论文声称，这样可以让同一个已训练策略输出一个连续轨迹对象，支持重采样、约束、转换为局部流场，并与控制器配合使用。

## 问题
- 现代机器人模仿策略常输出固定分辨率的动作块，这会在执行前掩盖连续性、导数、边界条件和重采样等有用的运动结构。
- 这很重要，因为机器人控制器在执行时往往需要平滑轨迹、跟踪误差后的修正，以及约束处理。
- 现有的运动基元和动力系统方法可以暴露这些结构，但通常没有作为一个简单的输出替换，直接接入当前的扩散、flow matching、Transformer 或 VLA 风格策略主干。

## 方法
- 策略预测的是样条参数，而不是一串离散动作。样条解码器把这些参数映射成任意查询时刻的连续轨迹。
- 主要实现使用分段二次 Bernstein 样条，每个片段有 3 个控制点，并且可以通过线性约束施加 C0 或 C1 连续性。
- 对于二次样条，先把当前状态投影到样条上最近的点，再把朝向曲线的吸引项和沿曲线运动结合起来，就可以把预测曲线转换成与状态相关的流场。
- 同一组样条参数还支持端点约束、零终端切线约束、对凸集合的凸包安全检查、通过控制点差分施加导数约束，以及通过样条基函数传播高斯不确定性。
- 论文通过修改输出头、预测目标和损失，把这种输出表示接到 ACT、Diffusion Policy、Flow Matching Policy、基于 Transformer 的策略和 VLA 风格策略上，而不是改动主干网络。

## 结果
- 这段摘要没有给出任务成功率、误差指标、数据集规模，或与动作块基线的数值对比。
- 论文声称实验覆盖低维运动学习、匹配主干下的仿真操作、灵巧操作和真实机器人案例研究。
- 最明确的具体结论是它可以兼容多种策略家族：ACT、扩散策略、flow matching、基于 Transformer 的策略，以及 VLA 风格模型。
- 摘要指出，二次样条输出可以进行解析距离场构造，并且在给定的正则性和投影假设下，诱导动力学不会增加到生成样条的距离。
- 该方法把密集动作序列压缩成更少的样条参数，但摘要没有给出压缩比或运行时间。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07386v1](https://arxiv.org/abs/2606.07386v1)
