---
source: arxiv
url: http://arxiv.org/abs/2603.05687v2
published_at: '2026-03-05T21:22:49'
authors:
- Zhengtong Xu
- Yeping Wang
- Ben Abbatematteo
- Jom Preechayasomboon
- Sonny Chan
- Nick Colonnese
- Amirhossein H. Memar
topics:
- dexterous-manipulation
- visuotactile-policy
- diffusion-policy
- contact-modeling
- compliance-control
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Contact-Grounded Policy: Dexterous Visuotactile Policy with Generative Contact Grounding

## Summary
CGP面向多指灵巧手的接触丰富操作，核心是把“期望接触”先表示为未来机器人状态与触觉的联合轨迹，再映射成底层顺应控制器可执行的目标状态。它不是把触觉仅当作额外输入，而是把触觉与控制执行显式绑定，从而提升复杂接触任务的稳定性与成功率。

## Problem
- 现有灵巧操作策略常只预测运动学轨迹，难以显式表示和维持不断变化的多点接触，因此容易打滑、过硬接触或执行不稳定。
- 许多触觉方法虽然使用了触觉观测，但没有建模“预测到的接触”如何通过底层顺应/PD控制器真正落地执行。
- 这很重要，因为多指手的接触结果高度依赖物体几何、摩擦变化和滑移；如果策略输出与控制器动力学不一致，真实操作成功率会明显下降。

## Approach
- 提出 **Contact-Grounded Policy (CGP)**：先预测未来的**实际机器人状态**和**触觉反馈**的联合轨迹，而不是直接回归动作。
- 用一个**条件扩散模型**在压缩后的触觉潜空间中生成未来轨迹；触觉先经带 KL 正则的 VAE 压缩，以降低高维触觉生成成本并稳定训练。
- 学习一个**contact-consistency mapping**，把预测得到的“状态+触觉”对映射为底层顺应控制器可执行的**目标机器人状态**，使控制器更可能复现预期接触。
- 该映射采用**残差形式**预测目标状态偏移，相比直接回归更稳健；测试时采用滚动时域重规划，逐步执行预测目标。

## Results
- 在 **5 个接触丰富任务**上，CGP均优于基线扩散策略（表 II）。
- **模拟 In-Hand Box Flipping（60 demos）**：CGP **66.0%**，高于 Visuotactile DP **58.0%** 和 Visuomotor DP **53.2%**。
- **模拟 Fragile Egg Grasping（100 demos）**：CGP **74.8%**，高于 Visuotactile DP **70.0%** 和 Visuomotor DP **53.2%**。
- **模拟 Dish Wiping（100 demos）**：CGP **58.4%**，高于 Visuotactile DP **43.6%** 和 Visuomotor DP **42.4%**。
- **真实 Jar Opening（45 demos）**：CGP **93.3%**，显著高于 Visuotactile DP **66.7%** 和 Visuomotor DP **73.3%**。
- **真实 In-Hand Box Flipping（90 demos）**：CGP **80.0%**，高于两种基线的 **60.0%**。另一个消融显示，在手部构型预测上，`State+Tactile` 的残差映射 MAE 为 **5.94±0.20 ×10^-3 rad**，优于仅状态 **10.64±0.38**、仅触觉 **12.15±0.20** 及绝对回归 **8.80±0.24**。

## Link
- [http://arxiv.org/abs/2603.05687v2](http://arxiv.org/abs/2603.05687v2)
