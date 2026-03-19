---
source: arxiv
url: http://arxiv.org/abs/2603.01741v2
published_at: '2026-03-02T11:06:40'
authors:
- Naoki Shitanda
- Motoki Omura
- Tatsuya Harada
- Takayuki Osa
topics:
- reinforcement-learning
- policy-optimization
- ensemble-rl
- exploration
- importance-sampling
relevance_score: 0.19
run_id: materialize-outputs
language_code: zh-CN
---

# Rethinking Policy Diversity in Ensemble Policy Gradient in Large-Scale Reinforcement Learning

## Summary
本文研究大规模并行强化学习中的多策略集成探索，指出“策略越分散越好”并不成立。作者提出 CPO，通过约束跟随者与领导者之间的 KL 距离，在保持探索多样性的同时提升稳定性和样本效率。

## Problem
- 在拥有 **24,576** 个并行环境的大规模 on-policy RL 中，单一策略的探索不足，简单增加数据量并不能有效提升学习效率。
- 现有集成方法（如 SAPG）虽能扩大探索范围，但**过大的策略间差异**会让 leader 使用 follower 数据时的 importance sampling 比率偏离 1，降低有效样本量并增加 PPO clipping 偏差。
- 这很重要，因为机器人灵巧操作等高维任务既需要足够探索，又极度依赖训练稳定性和样本效率。

## Approach
- 提出 **Coupled Policy Optimization (CPO)**：在 leader-follower 框架中，对 follower 更新加入与 leader 的 **KL divergence constraint**，让 follower 在 leader 周围“有控制地分散探索”。
- 理论上给出三点：过大的策略差异会降低 **effective sample size (ESS)**、增大 PPO clipping 引入的梯度偏差；而 follower-leader 的 KL 距离可上界 IS ratio 偏离程度。
- 在实现上，把 follower 的更新写成带 KL 约束的优化问题，并用一个带优势加权的目标近似求解，再与原 SAPG/PPO 风格目标联合训练。
- 为避免所有 follower 因 KL 约束而过度聚集，加入一个 **adversarial reward**：训练判别器根据状态-动作识别策略身份，鼓励不同 follower 覆盖不同区域。

## Results
- 实验覆盖 **10 个任务**：**6** 个灵巧操作、**2** 个夹爪操作、**2** 个 locomotion 任务；使用 **24,576** 并行环境、**5** 个随机种子，对比 **PPO、DexPBT、SAPG**。
- 在灵巧操作任务、训练 **2×10^10** environment steps 后，CPO 在多项任务上取得最佳或并列最佳最终性能：**ShadowHand 13762±414**（vs SAPG **12882±343**, PPO **10661±1050**）、**AllegroHand 14421±885**（vs DexPBT **13239±239**, SAPG **11989±817**）、**Reorientation 43.75±0.65**（vs SAPG **38.79±1.66**, PPO **1.04±0.98**）、**Two-Arms Reorientation 35.30±2.77**（vs DexPBT **26.43±11.12**, SAPG **5.11±3.41**）。
- 在 **Regrasping** 上，CPO **37.44±1.21**，与 SAPG **37.20±0.65**、DexPBT **35.26±2.82** 接近，仍属最优组；在 **Throw** 上 CPO **21.69±2.44**，略低于 SAPG **22.51±1.15**，但作者称整体上仍保持稳定高表现。
- 作者声称在许多任务中，CPO 用**约一半环境步数**即可达到 SAPG 的最终表现，说明样本效率更高；摘录中未给出更完整逐任务曲线数值。
- 机制分析上，作者报告 KL 约束使 IS ratio 更接近 **1**、提升 ESS，并让 follower 自然围绕 leader 形成更结构化分布；这些是论文的强实证主张，但摘录未提供对应 ESS 或 KL 的完整数表。

## Link
- [http://arxiv.org/abs/2603.01741v2](http://arxiv.org/abs/2603.01741v2)
