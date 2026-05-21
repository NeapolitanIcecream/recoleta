---
source: arxiv
url: https://arxiv.org/abs/2604.24086v1
published_at: '2026-04-27T06:20:15'
authors:
- Kai Yang
- Zedong Chu
- Yingnan Guo
- Zhengbo Wang
- Shichao Xie
- Yanfen Shen
- Xiaolong Wu
- Xing Li
- Mu Xu
topics:
- vision-language-action
- mobile-robot-navigation
- cloud-edge-control
- latency-compensation
- safe-rl
- robot-foundation-models
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AsyncShield: A Plug-and-Play Edge Adapter for Asynchronous Cloud-based VLA Navigation

## Summary
## 摘要
AsyncShield 是用于云端 VLA 机器人导航的边缘侧适配器。它用 SE(2) 位姿重对齐校正延迟的 VLA 路径点，然后使用带安全约束的 RL 策略，根据 LiDAR 和校正后的路径输入选择局部子目标。

## 问题
- 云端 VLA 模型通常在机器人外部运行，因此网络延迟、抖动、丢包和中断会使导航命令延迟到达。
- 移动机器人在延迟期间会继续运动，因此在旧自我坐标系中生成的路径点，可能在当前自我坐标系中指向错误位置并导致碰撞。
- 这个问题很重要，因为当过期意图遇到动态障碍物时，直接执行、时间平滑和残差校正都可能失效。

## 方法
- 边缘设备维护带时间戳的位姿缓冲区，并取回 VLA 数据包锚定时刻的机器人位姿。
- 它使用解析 SE(2) 变换，将每个延迟的 VLA 路径点映射到当前自我坐标系，把时间滞后转换为可测量的空间偏移。
- 适配器输入 5 个重对齐后的前视路径点，间距为 0.2 m，同时输入 144 个 LiDAR 距离值。
- PPO-Lagrangian 策略输出通用局部子目标；奖励项用于路径跟踪，当最小障碍物距离低于安全半径时，还会加入基于 LiDAR 的代价。
- 训练使用随机化的 10 m × 10 m 场景、6 个静态障碍物和 6 个动态障碍物，延迟从 0.3 到 1.5 s 采样，丢包率最高 0.2，并加入执行器滞后、加速度限制、噪声和角度偏置。

## 结果
- 在理想网络条件下的 600 个评估 episode 中，AsyncShield 达到 80.0% 成功率、0.717 m CTE、1.2% 风险暴露率和 8.87 s 到达目标时间。A2C2 达到 56.7% SR，RTC 达到 40.0%，Naive 达到 20.0%。
- 在混合退化条件下，AsyncShield 达到 76.7% SR、0.725 m CTE、1.3% RER 和 9.29 s TTG。A2C2 降至 43.3% SR，RTC 降至 30.0%，Naive 降至 16.7%。
- 在混合退化条件下，AsyncShield 将相对于 A2C2 的 CTE 从 1.146 m 降至 0.725 m，将相对于 Naive 的 CTE 从 1.272 m 降至 0.725 m。
- 去掉时间对齐的消融版本在混合退化条件下 SR 从 76.7% 降至 36.7%，CTE 从 0.725 m 升至 1.194 m。
- 去掉 RL 适配器的消融版本在混合退化条件下达到 53.3% SR 和 1.443 m CTE，这支持了学习式意图-安全权衡的必要性。
- 去掉安全约束的消融版本在混合退化条件下只达到 23.3% SR，虽然 CTE 较低，为 0.692 m，但 RER 为 4.7%，说明命令过期时，贴近路径跟踪可能并不安全。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24086v1](https://arxiv.org/abs/2604.24086v1)
