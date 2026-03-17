---
source: hn
url: https://www.brown.edu/news/2026-03-04/kitchen-fluid-dynamics
published_at: '2026-03-12T22:51:04'
authors:
- hhs
topics:
- fluid-dynamics
- thin-film-flow
- navier-stokes
- kitchen-physics
relevance_score: 0.01
run_id: materialize-outputs
---

# How long does it take to get last liquid drops from kitchen containers?

## Summary
这项研究用薄液膜流动的物理模型回答了一个日常但普遍的问题：把容器倾斜后，最后那些液体到底要等多久才会流下来。作者结合 Navier-Stokes 方程与简单实验，给出了不同黏度液体在厨房场景中的排空时间估计。

## Problem
- 研究要解决的是：倾斜容器表面的**薄液膜**需要多长时间才能排出大部分液体，以及洗锅后残余水膜何时会汇聚到可再次倒掉。
- 这个问题重要，是因为薄液膜流动不仅出现在厨房，也广泛存在于生物物理和表面流体研究中，是更一般流体力学问题的现实例子。
- 难点在于排液时间会随液体黏度显著变化，直觉很难准确判断等待时间。

## Approach
- 核心方法是使用 **Navier-Stokes 方程的黏性主导（viscous regime）近似**，来描述薄液膜在倾斜表面上因重力缓慢流动的过程。
- 作者把问题简化成“液体在一块以 45° 倾斜的表面上流动”，据此预测不同黏度液体达到一定排出比例所需的时间。
- 他们进行了配套实验：让液体沿 45° 斜板流下，并通过称重来判断何时已有 **90%** 的液体被排出（decanted）。
- 对于洗完的铁锅/炒锅问题，作者进一步做了计算机模拟，估计残余水膜汇聚到底部、适合再次倒水的最佳等待时间。

## Results
- 实验与理论计算**总体一致**，说明该薄液膜流动模型能够较好预测厨房容器中的排液等待时间。
- 在 **45° 倾角** 下，像牛奶这样的较低黏度液体，排出薄液膜中 **90%** 的液体大约需要 **30 秒**。
- 对于更黏的液体，如橄榄油，达到 **90% 回收率** 需要 **超过 9 分钟**。
- 水达到 **90% decanting** 只需**几秒钟**。
- 冷枫糖浆则可能需要**数小时**才能达到同样的 **90%** 排出水平。
- 对于洗锅后的残余水膜，模拟给出的最佳再次倒水等待时间约为 **15 分钟**；研究者原先通常只等 **1–2 分钟**。

## Link
- [https://www.brown.edu/news/2026-03-04/kitchen-fluid-dynamics](https://www.brown.edu/news/2026-03-04/kitchen-fluid-dynamics)
