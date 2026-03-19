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
- robot-learning
relevance_score: 0.29
run_id: materialize-outputs
language_code: zh-CN
---

# Contact-Grounded Policy: Dexterous Visuotactile Policy with Generative Contact Grounding

## Summary
本文提出 Contact-Grounded Policy（CGP），用于多指灵巧操作中的视觉-触觉联合控制。其关键点是先预测未来的机器人状态与触觉，再把它们转换成低层顺应控制器可执行的目标状态，从而让“想要的接触”真正落地。

## Problem
- 多指灵巧操作依赖持续变化的多点接触，受物体几何、摩擦转变和打滑影响很大，单靠视觉或纯运动学预测很难稳定完成任务。
- 以往触觉策略通常只把触觉当作额外输入，缺少对“接触状态本身”以及“策略输出如何被低层顺应/PD 控制器执行”的建模。
- 结果是模型也许能预测动作或触觉，但这些输出未必能在真实闭环控制中复现目标接触，导致滑移、过硬接触和执行不可靠。

## Approach
- CGP把问题表述为**contact grounding**：不直接输出动作，而是先预测未来一段时间内耦合的**实际机器人状态**和**触觉反馈**轨迹。
- 它包含两个核心模块：1）条件扩散模型，在压缩后的触觉潜空间里联合生成未来状态与触觉；2）接触一致性映射，将预测的“状态+触觉”转换为顺应控制器可执行的目标机器人状态。
- 接触一致性映射学习的是一个与具体机器人、传感器和控制器绑定的数据驱动映射，避免手工定义接触点、接触模式或显式动力学。
- 为了高效生成高维触觉，作者先用带 KL 正则的 VAE 压缩触觉，再在潜空间中进行扩散预测；该设计同时适用于模拟中的稠密触觉阵列和真实系统中的视觉式触觉图像。

## Results
- 在 5 个接触丰富任务上，CGP均优于两个 diffusion policy 基线（Visuotactile DP、Visuomotor DP）。
- 仿真 In-Hand Box Flipping（60 demos）：CGP **66.0%**，高于 Visuotactile DP **58.0%** 和 Visuomotor DP **53.2%**。
- 仿真 Fragile Egg Grasping（100 demos）：CGP **74.8%**，高于 Visuotactile DP **70.0%** 和 Visuomotor DP **53.2%**。
- 仿真 Dish Wiping（100 demos）：CGP **58.4%**，高于 Visuotactile DP **43.6%** 和 Visuomotor DP **42.4%**。
- 真实 Jar Opening（45 demos）：CGP **93.3%**，显著高于 Visuotactile DP **66.7%** 和 Visuomotor DP **73.3%**；真实 In-Hand Box Flipping（90 demos）：CGP **80.0%**，高于两种基线的 **60.0%**。
- 接触一致性映射的手部配置预测消融中，最佳“State+Tactile + ResNet1D + Residual” MAE 为 **5.94±0.20 ×10^-3 rad**，优于同设置的绝对预测 **8.80±0.24**，也优于仅状态残差 **10.64±0.38**，说明触觉输入和残差建模都有效。

## Link
- [http://arxiv.org/abs/2603.05687v2](http://arxiv.org/abs/2603.05687v2)
