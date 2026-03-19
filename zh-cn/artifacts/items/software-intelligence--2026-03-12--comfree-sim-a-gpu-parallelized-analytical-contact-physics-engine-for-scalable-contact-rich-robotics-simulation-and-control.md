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
- robotics
- contact-dynamics
- gpu-parallelism
- model-predictive-control
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# ComFree-Sim: A GPU-Parallelized Analytical Contact Physics Engine for Scalable Contact-Rich Robotics Simulation and Control

## Summary
ComFree-Sim 是一个面向接触密集型机器人任务的 GPU 并行解析接触物理引擎，目标是替代需要迭代求解的传统接触解析方式。它通过无互补约束的闭式冲量计算，将接触求解变成天然适合 GPU 的并行任务，从而提升大规模仿真与实时控制效率。

## Problem
- 传统机器人物理引擎在接触解析时，通常要解互补约束或优化问题，单步计算成本会随接触数**超线性增长**。
- 这会拖慢接触密集场景下的并行仿真、可微仿真、MPC 和在线规划，尤其不利于高频闭环控制。
- 需要一种既保持接触物理可信度，又能随接触数近线性扩展、适合 GPU 的轻量接触后端。

## Approach
- 核心方法是**complementarity-free** 接触建模：先预测“无接触时”物体下一步速度，再根据违反接触约束的程度做一次**阻抗式 prediction-correction 修正**，直接闭式算出接触冲量，不再做每步迭代求解。
- 该方法在**库仑摩擦对偶锥**中工作，并把摩擦锥做成多面体近似，因此每个接触对、每个锥面都可以**彼此解耦**独立计算。
- 论文把模型扩展到**统一 6D 接触**，同时覆盖切向摩擦、扭转摩擦、滚动摩擦，而不只是普通点接触滑动摩擦。
- 实现上基于 Warp，分成平滑速度预测、逐接触逐面求冲量、广义冲量累积、速度修正四个 GPU kernel；并提供 **MuJoCo-compatible** 接口，可作为 MJWarp 的替代后端。
- 为避免精确阻抗矩阵代价过高，作者提出一个实用的**dual-cone impedance heuristic**，用少量全局参数控制接触“软硬度”，同时保留学习式参数化可能性。

## Results
- 在碰撞密集下落测试中，MJWarp 的平均穿透深度为 **1.7 ± 4.9 mm**；ComFree-Sim 在不同参数下从 **3.9 ± 6.9 mm** 改善到 **0.9 ± 1.5 mm**，最佳设置下**低于 MJWarp**。
- 论文声称在密集接触场景中，ComFree-Sim 相比 MJWarp 实现**近线性 runtime scaling**，并取得 **2–3× 更高吞吐量**，同时保持**可比 physical fidelity**。
- 在扭转摩擦与滚动摩擦测试中，作者报告角速度/质心速度随摩擦系数变化呈**单调衰减趋势**，表明 6D 摩擦建模能一致地捕捉耗散行为；但摘录中**未给出具体数值指标**。
- 在稳定性测试中，ComFree-Sim 在较宽参数范围内表现为**水平速度单调衰减**、无明显漂移或能量增长；并称在 **dt = 0.02 s** 时仍可稳定，但通常比 MJWarp 更需要较小时间步。默认基准多使用 **dt = 0.002 s**。
- 系统还被部署到真实 **LEAP 多指灵巧手** 的实时 MPPI/MPC 和动作重定向任务中，作者声称更低延迟仿真带来**更高闭环成功率**与更实用的高频控制，但摘录中**未提供具体成功率数字**。

## Link
- [http://arxiv.org/abs/2603.12185v1](http://arxiv.org/abs/2603.12185v1)
