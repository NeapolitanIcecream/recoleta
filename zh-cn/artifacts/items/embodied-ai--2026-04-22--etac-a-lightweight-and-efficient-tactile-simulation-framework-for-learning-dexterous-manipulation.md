---
source: arxiv
url: http://arxiv.org/abs/2604.20295v1
published_at: '2026-04-22T07:51:20'
authors:
- Zhe Xu
- Feiyu Zhao
- Xiyan Huang
- Chenxi Xiao
topics:
- tactile-simulation
- dexterous-manipulation
- reinforcement-learning
- sim2real
- robot-learning
relevance_score: 0.81
run_id: materialize-outputs
language_code: zh-CN
---

# ETac: A Lightweight and Efficient Tactile Simulation Framework for Learning Dexterous Manipulation

## Summary
## 摘要
ETac 是一个面向灵巧操作的触觉仿真框架，目标是在不承担 FEM 级别计算成本的前提下，保留接近 FEM 的形变质量。它把简单的物理先验与一个小型学习式修正模型结合起来，再用模拟得到的触觉场在大规模强化学习中训练盲抓策略。

## 问题
- 触觉强化学习需要大量模拟交互，但 FEM 这类高保真软体仿真器对于大规模并行训练来说速度太慢。
- 更快的触觉仿真器通常只建模局部压痕，无法捕捉弹性体上的形变传播，这会降低真实感，尤其是在曲面传感器上。
- 这一点很关键，因为现代触觉手依赖丰富的接触模式，而不只是二值接触或力信号，来实现稳定的灵巧操作。

## 方法
- ETac 将触觉传感器表面离散为 3D 节点，并用 signed distance fields 检测接触。处于接触中的节点称为“active”节点。
- 对未接触的“passive”节点，它用两部分来估计形变：一个指数距离衰减传播项，以及一个轻量残差网络。
- 衰减项提供了一个快速的物理先验，用来描述压痕如何沿弹性体表面扩散。
- 该残差网络由 PointNet 风格的编码器和 MLP 解码器组成，用来修正线性衰减模型的误差，并捕捉曲率、各向异性以及接触点之间相互作用等非线性效应。
- 传播参数通过拟合 FEM 生成的形变数据进行训练，随后得到的位移场被作为 ShadowHand 上盲抓任务中 PPO 的触觉输入。

## 结果
- 在相对 FEM 真值的形变估计上，ETac 在轻量级基线中报告了最低 RMSE：平面弹性体上为 **0.058 ± 0.034 mm**，曲面弹性体上为 **0.116 ± 0.049 mm**；相比之下，**TacSL: 0.194 / 0.445 mm**，**Taxim: 0.163 / 0.447 mm**。
- 完整模型优于其消融版本：仅线性模型在平面/曲面弹性体上的 RMSE 为 **0.151 / 0.256 mm**，仅残差模型为 **0.074 / 0.128 mm**。
- 在真实传感器响应预测中，使用 ETac 生成的数据时，平面传感器的 L1 loss 为 **3.94%**，曲面传感器为 **3.61%**；使用 FEM 数据时分别为 **2.46%** 和 **2.75%**。
- 在单张 RTX 4090 上的强化学习吞吐量测试中，ETac 支持 **4,096 个并行环境**，并在该规模下达到 **869 总 FPS**。论文称，在同一 GPU 上，这比 FEM 的 FPS 高 **11×**，并行环境数多 **128×**。
- 论文报告的 ETac 总 FPS 在 **64、256、1024、4096** 个环境下分别为 **669、956、878、869**。Taxim 在 **64、256、1024** 个环境下达到 **508、620、650**，在 **4096** 时显存耗尽；TacSL 分别达到 **698、975、918、886**。
- 在覆盖四类物体的盲抓任务中，全手触觉配置的平均成功率达到 **84.45% ± 13.09**，相比之下，指尖传感器配置为 **72.90% ± 21.06**，使用物体位姿的非触觉基线为 **62.97% ± 37.82**。论文强调，这比基线高出 **21.48 个百分点**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20295v1](http://arxiv.org/abs/2604.20295v1)
