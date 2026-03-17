---
source: arxiv
url: http://arxiv.org/abs/2603.12185v1
published_at: '2026-03-12T17:14:45'
authors:
- Chetan Borse
- Zhixian Xie
- Wei-Cheng Huang
- Wanxin Jin
topics:
- physics-simulation
- contact-rich-robotics
- gpu-parallelism
- analytical-contact-model
- dexterous-manipulation
relevance_score: 0.73
run_id: materialize-outputs
---

# ComFree-Sim: A GPU-Parallelized Analytical Contact Physics Engine for Scalable Contact-Rich Robotics Simulation and Control

## Summary
ComFree-Sim 是一个面向接触密集型机器人任务的 GPU 并行物理引擎，用解析式、非互补的接触求解替代传统迭代优化。它的核心价值是把接触分解成可并行的小问题，从而在保持接近 MuJoCo Warp 物理保真度的同时显著提升吞吐，并支持实时控制。

## Problem
- 现有接触丰富的机器人仿真常被**接触求解**拖慢：主流方法依赖互补约束或约束优化，每一步都要迭代求解，接触越多，代价通常超线性增长。
- 这会限制大规模并行数据生成、可微仿真、在线 MPC/MPPI，以及灵巧手这类高频、密集接触控制任务的实时部署。
- 需要一种既**更轻量、可线性扩展**，又不明显牺牲物理真实性和稳定性的接触后端，最好还能作为现有 MuJoCo/Warp 工作流的即插即用替代。

## Approach
- 核心机制是**complementarity-free** 接触建模：先预测在“无接触力”下的下一步速度，再根据违反非穿透/摩擦约束的程度，用一个**阻抗式预测-校正**公式直接算出接触冲量，不再做每步迭代优化。
- 它在**库仑摩擦对偶锥**里做解析闭式更新，并把摩擦锥做多面体近似，因此每个接触对、每个锥面都能独立计算，天然适合 GPU kernel 并行。
- 论文把原方法扩展为**统一 6D 接触模型**，同时覆盖切向摩擦、扭转摩擦和滚动摩擦，而不只是简单点接触滑动摩擦。
- 为了避免精确计算阻抗矩阵的高开销，作者提出了一个**实用的双锥阻抗启发式**：用少量全局用户参数 \(k_{user}, d_{user}\) 和 gap-dependent 缩放来控制接触“软硬度”，并保持 MuJoCo 兼容接口。
- 系统基于 Warp 实现，并通过 **MuJoCo-compatible interface** 暴露为 MJWarp 的 drop-in backend alternative，方便接入现有机器人仿真和控制栈。

## Results
- 在密集碰撞下落测试中，MJWarp 的平均穿透深度为 **1.7 ± 4.9 mm**；ComFree-Sim 经过调参可达到**相当或更低**的穿透，例如：
  - **0.3, 0.001** 时为 **1.6 ± 3.3 mm**；
  - **0.3, 0.005** 时为 **1.4 ± 2.5 mm**；
  - **0.5, 0.001** 时为 **1.0 ± 2.1 mm**；
  - **0.5, 0.005** 时为 **0.9 ± 1.5 mm**。
- 摘要声称在密集接触场景中，相比 MJWarp，ComFree-Sim 实现了**近线性 runtime scaling**，并带来 **2–3× higher throughput**，原因是接触求解跨接触对与锥面可分解并行。
- 稳定性方面，文中称 ComFree-Sim 在较宽参数范围内表现出**单调水平速度衰减**、无明显伪漂移或能量增长；在 **dt = 0.02 s** 这样相对较大的步长下仍可稳定，但通常比 MJWarp 更依赖较小步长。除特别说明外，基准默认使用 **dt = 0.002 s**。
- 在摩擦行为上，作者通过受控实验展示了**扭转摩擦**与**滚动摩擦**的耗散趋势会随对应摩擦系数单调变化，但摘录中**未给出具体数值指标**。
- 在真实机器人应用上，摘要声称该引擎已部署到**LEAP 多指灵巧手**的实时 MPC 与 dynamics-aware motion retargeting 中，并显示**更低延迟 rollout 可提升闭环成功率**、支持更实用的高频接触控制；但摘录中**未提供成功率百分比或具体对比数字**。

## Link
- [http://arxiv.org/abs/2603.12185v1](http://arxiv.org/abs/2603.12185v1)
