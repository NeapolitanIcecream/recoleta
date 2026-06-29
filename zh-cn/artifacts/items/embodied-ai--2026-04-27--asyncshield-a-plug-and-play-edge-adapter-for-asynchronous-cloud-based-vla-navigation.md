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
AsyncShield 是一个面向云端 VLA 机器人导航的边侧适配器。它先用 SE(2) 位姿重对齐修正延迟的 VLA 航点，再用带安全约束的强化学习策略，从 LiDAR 和校正后的路径输入中选择局部子目标。

## 问题
- 云端 VLA 模型通常在车载设备外运行，因此网络延迟、抖动、丢包和中断会让导航指令晚到。
- 移动机器人在这段延迟里仍会继续运动，所以在旧的自我坐标系里生成的航点到了当前坐标系里可能指向错误位置并引发碰撞。
- 这个问题很重要，因为直接执行、时间平滑和残差修正在过时意图遇到动态障碍物时都可能失效。

## 方法
- 边侧设备维护一个带时间戳的位姿缓冲区，并取回 VLA 数据包锚点时刻的机器人位姿。
- 它用解析的 SE(2) 变换把每个延迟的 VLA 航点映射到当前自我坐标系，把时间滞后转成可测量的空间偏移。
- 适配器接收 5 个重对齐的前瞻航点，间隔 0.2 m，以及 144 个 LiDAR 接近值。
- PPO-Lagrangian 策略输出一个通用局部子目标，奖励项包含路径跟踪；当最近障碍物距离低于安全半径时，使用基于 LiDAR 的代价项。
- 训练使用随机生成的 10 m × 10 m 场景、6 个静态障碍物和 6 个动态障碍物、0.3 到 1.5 s 的延迟采样、最高 0.2 的丢包率、执行器滞后、加速度限制、噪声和角度偏差。

## 结果
- 在理想网络条件下的 600 个评估回合中，AsyncShield 的成功率达到 80.0%，CTE 为 0.717 m，风险暴露率为 1.2%，到达目标时间为 8.87 s。A2C2 的成功率为 56.7%，RTC 为 40.0%，Naive 为 20.0%。
- 在混合退化条件下，AsyncShield 的成功率达到 76.7%，CTE 为 0.725 m，RER 为 1.3%，TTG 为 9.29 s。A2C2 降到 43.3% 成功率，RTC 降到 30.0%，Naive 降到 16.7%。
- 在混合退化条件下，AsyncShield 的 CTE 从 1.146 m 降到 0.725 m，相比 A2C2；相比 Naive，则从 1.272 m 降到 0.725 m。
- 去掉时间对齐的消融版本在混合退化条件下，成功率从 76.7% 降到 36.7%，CTE 从 0.725 m 升到 1.194 m。
- 去掉 RL 适配器的消融版本在混合退化条件下达到 53.3% 的成功率和 1.443 m 的 CTE，这说明需要学习到的意图与安全权衡。
- 去掉安全约束的消融版本在混合退化条件下的成功率只有 23.3%，尽管 CTE 只有 0.692 m，但 RER 达到 4.7%，说明命令过时时，贴近路径跟踪也可能不安全。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24086v1](https://arxiv.org/abs/2604.24086v1)
