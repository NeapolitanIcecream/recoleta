---
source: arxiv
url: http://arxiv.org/abs/2603.28032v1
published_at: '2026-03-30T04:49:29'
authors:
- Tianle Zeng
- Hanxuan Chen
- Yanci Wen
- Hong Zhang
topics:
- air-ground-simulation
- uav-simulation
- embodied-ai
- vision-language-action
- reinforcement-learning
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# CARLA-Air: Fly Drones Inside a CARLA World -- A Unified Infrastructure for Air-Ground Embodied Intelligence

## Summary
## 摘要
CARLA-Air 是一个仿真平台，把 CARLA 和 AirSim 放在同一个 Unreal Engine 进程中运行，因此无人机和地面智能体共享同一世界状态、物理 tick 和渲染流水线。它面向空地具身智能任务，包括协作机器人、多模态数据采集、导航、视觉语言动作和强化学习。

## 问题
- 现有开源仿真器按领域分开：CARLA 有真实的城市交通和行人，但没有原生 UAV 飞行；AirSim 有多旋翼动力学和空中传感器，但缺少有活动主体的地面场景。
- 基于桥接的协同仿真可以连接多个独立仿真器，但跨进程消息传递会带来同步开销，也可能破坏传感器之间严格的时空对齐。
- 这会影响感知、学习和评估任务，因为这些任务需要在一个物理一致的环境中同步获取空中和地面的观测。

## 方法
- CARLA-Air 将 CARLA 和 AirSim 合并到同一个 Unreal Engine 4 进程中，同时保留两者原生的 Python API 和 ROS 2 接口，因此现有代码无需修改即可运行。
- 主要技术处理针对 UE4 每个 world 只能有一个 GameMode 的限制：系统继承 CARLA 的 GameMode 负责地面仿真，再在 `BeginPlay` 阶段把 AirSim 的空中飞行逻辑作为普通 actor 启动。
- 由于两个平台运行在同一进程内，它们共享同一个物理 tick 和渲染器，因此可以在空中与地面智能体之间实现同步感知。
- 平台支持在每个仿真 tick 采集最多 18 种传感器模态，包括 RGB、深度、语义分割、LiDAR、雷达、IMU、GNSS 和气压计。
- 它还包含一个资产流水线，用于自定义机器人、UAV 配置、车辆和地图，并内置支持空地协作、具身导航、视觉语言动作、数据集构建和 RL 策略训练。

## 结果
- 图 1 报告了并发传感器条件下的每帧跨进程数据传输开销：基于桥接的协同仿真会随着传感器数量增加而接近线性增长，而 CARLA-Air 基本保持不变，**每帧低于 0.5 ms**，因为没有跨进程序列化。
- 论文称该平台可以在每个仿真 tick 上，对空中和地面平台同步采集**最多 18 种传感器模态**。
- 在平台对比表中，CARLA-Air 是唯一同时支持**城市交通、行人、UAV 飞行、单进程执行、共享渲染、原生 API、联合传感器、预构建二进制文件、测试套件、自定义资产和开源发布**的系统。
- 这段摘录**没有提供任务层面的基准结果**，例如导航成功率、RL 回报、sim-to-real 迁移，或与基线相比的数据集规模对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28032v1](http://arxiv.org/abs/2603.28032v1)
