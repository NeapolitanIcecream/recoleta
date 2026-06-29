---
source: arxiv
url: https://arxiv.org/abs/2605.26379v1
published_at: '2026-05-25T22:56:26'
authors:
- David Klindt
- Yann LeCun
- Randall Balestriero
topics:
- world-models
- jepa
- linear-identifiability
- self-supervised-learning
- latent-planning
- robot-control
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# When Does LeJEPA Learn a World Model?

## Summary
## 总结
这篇论文给出 LeJEPA 何时学到线性世界模型的条件：当潜变量是高斯分布、正样本对来自平稳的加性噪声转移时，最优解会在正交变换下恢复潜变量。

## 问题
- 非线性观测会掩盖规划和组合泛化所需的潜状态。
- 现有 JEPA 工作没有证明学到的嵌入何时能恢复真实潜变量，因此线性探针和潜空间规划缺少可辨识性保证。
- 论文要问的是：在独立、平稳的加性噪声转移下，哪种潜变量分布会让 LeJEPA 具有线性可辨识性。

## 方法
- 将观测建模为 `x = g(z)`，其中 `g` 可以是非线性的，并用 LeJEPA 训练 `h = f ∘ g`，目标是对齐项 `E||h(z') - h(z)||²` 加上高斯正则项 `h(z) ~ N(0, I_n)`。
- 对于高斯潜变量，使用 Ornstein-Uhlenbeck 正样本对转移 `z' = ρz + sqrt(1 - ρ²)η`，其中 `η ~ N(0, I_n)`。
- 把学到的函数分解为 Hermite 多项式的阶数。`d` 阶项的相关性是 `ρ^d`，所以非线性项的相关性低于一次项。
- 对逆向结论使用 Sturm-Liouville 分析：在加性噪声下，如果要求第一特征函数是仿射函数，就会推出潜变量密度必须是高斯分布。
- 通过证明当代价对正交变换不变时，最优有限时域控制在正交潜变量恢复下保持不变，把正交恢复和规划联系起来。

## 结果
- 定理 5.1：在高斯世界中，任何可测的 `h` 只要满足 `h(z) ~ N(0, I_n)`，就有损失 `L(h) ≥ 2(1 - ρ)n`；只有当 `h(z) = Qz`，其中 `Q ∈ O(n)` 为某个正交矩阵时，才取等号。
- 在最优点，学到的转移在表示空间中具有相同形式：`h(z') | h(z) ~ N(ρh(z), (1 - ρ²)I_n)`。
- 定理 5.2：在独立、平稳、加性噪声的世界中，高斯潜变量是唯一一种使所有白化后的 LeJEPA 极小解都为线性的情况。
- 定理 5.3：近似恢复满足界 `E||h(z) - Qz||² ≤ D + (ε + D)²`，其中 `D = δ / (2ρ(1 - ρ))`，`δ` 是对齐松弛量，`ε` 是白化误差。
- 定理 5.4：如果 `h(z)=Qz`，对于 `O(n)` 不变的代价，潜空间规划给出的最优值和动作序列与在真实潜状态中规划相同。
- 提供的摘录提到在 2D 非线性混合、分布消融、1024 维潜变量、近似界测试和基于像素的机器人控制上做了实验，但没有给出任务分数表或经验指标值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26379v1](https://arxiv.org/abs/2605.26379v1)
