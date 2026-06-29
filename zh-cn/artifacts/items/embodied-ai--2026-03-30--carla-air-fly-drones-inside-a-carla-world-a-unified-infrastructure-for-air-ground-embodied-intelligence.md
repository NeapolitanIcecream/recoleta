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
## 概述
CARLA-Air 是一个仿真平台，把 CARLA 和 AirSim 运行在同一个 Unreal Engine 进程里，让无人机和地面智能体共享同一个世界状态、物理步进和渲染管线。它面向空地具身智能任务，包括协同机器人、多模态数据采集、导航、视觉语言动作，以及强化学习。

## 问题
- 现有开源仿真器沿着领域分开：CARLA 有逼真的城市交通和行人，但没有原生的无人机飞行；AirSim 有多旋翼动力学和空中传感器，但缺少有人员活动的地面场景。
- 基于桥接的协同仿真可以把分开的仿真器连起来，但跨进程消息传递会增加同步开销，也可能破坏传感器之间严格的时空对齐。
- 这会影响那些需要来自同一个物理一致环境、并且同步采集空中和地面观测的感知、学习和评估任务。

## 方法
- CARLA-Air 将 CARLA 和 AirSim 合并到一个 Unreal Engine 4 进程中，同时保留两者原生的 Python API 和 ROS 2 接口，这样现有代码可以直接运行，不用修改。
- 主要技术处理针对 UE4 每个世界只能有一个 GameMode 的限制：系统继承 CARLA 的 GameMode 来进行地面仿真，然后在 `BeginPlay` 时把 AirSim 的空中飞行逻辑作为普通 actor 生成出来。
- 因为两个平台在同一个进程里运行，它们共享同一个物理步进和同一个渲染器，因此空中和地面智能体的感知是同步的。
- 平台支持每个仿真 tick 最多采集 18 种传感器模态，包括 RGB、深度、语义分割、LiDAR、雷达、IMU、GNSS 和气压计。
- 它还提供自定义机器人、无人机配置、车辆和地图的资产管线，并内置支持空地协同、具身导航、视觉语言动作、数据集构建和强化学习策略训练。

## 结果
- 图 1 报告了并发传感器下每帧的进程间数据传输：基于桥接的协同仿真会随着传感器数量接近线性增长，而 CARLA-Air 基本保持不变，**每帧低于 0.5 ms**，因为它没有跨进程序列化。
- 论文声称在每个仿真 tick 都能在空中和地面平台之间同步采集**最多 18 种传感器模态**。
- 在平台对比表中，CARLA-Air 是唯一一个同时支持**城市交通、行人、无人机飞行、单进程执行、共享渲染、原生 API、联合传感器、预编译二进制、测试套件、自定义资产和开源发布**的系统。
- 摘要片段**没有提供任务级基准数值**，例如导航成功率、强化学习回报、仿真到现实迁移，或与基线相比的数据集规模差异。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28032v1](http://arxiv.org/abs/2603.28032v1)
