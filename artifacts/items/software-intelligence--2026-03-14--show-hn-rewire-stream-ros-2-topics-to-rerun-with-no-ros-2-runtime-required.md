---
source: hn
url: https://rewire.run
published_at: '2026-03-14T23:22:38'
authors:
- alvgaona
topics:
- ros2-tooling
- robotics-visualization
- rerun
- dds-zenoh
- rust-systems
relevance_score: 0.49
run_id: materialize-outputs
---

# Show HN: Rewire – Stream ROS 2 topics to Rerun with no ROS 2 runtime required

## Summary
Rewire 是一个面向机器人开发的可视化桥接工具，可将 ROS 2 主题实时流入 Rerun，并且不需要在目标机器上安装或运行 ROS 2 运行时。它强调零侵入、单二进制部署和对多种中间件协议的直接兼容，降低了 ROS 2 数据观测与调试门槛。

## Problem
- 机器人开发中，实时查看 ROS 2 topics、TF、图像、点云等数据通常依赖完整 ROS 2 环境，安装、构建和工作区管理复杂。
- 现有调试/可视化流程往往会引入 ROS 节点、工作区或额外工具链，增加部署负担，并可能干扰现有 ROS graph。
- 跨 DDS/Zenoh 协议、动态 topic 发现、QoS 处理和性能监控分散在多工具中，不利于快速诊断真实机器人系统。

## Approach
- 核心方法是提供一个**纯 Rust 单二进制桥接器**，直接在网络层“观察”ROS 2 通信，原生支持 DDS 和 Zenoh，因此无需 colcon、ament、sourcing 或完整 ROS 2 runtime。
- 它将常见 ROS 2 消息自动映射到 Rerun 的可视化 archetypes，开箱即用支持图像、点云、TF、位姿、激光扫描、里程计等数据。
- 对非默认或自定义类型，用户可通过 JSON5 配置把 ROS 2 类型映射到 Rerun archetypes，无需写代码或重新编译；仅在自定义消息类型场景下才需要 source workspace。
- 系统会自动发现新 topic、自动订阅/退订，并处理 CycloneDDS、FastDDS、Zenoh、QoS 协商、TransientLocal late-joiner 数据以及 BestEffort UDP 大缓冲支持。
- 除数据可视化外，它还把每个 topic 的 Hz、带宽、丢包和延迟作为 Rerun 实体一并输出，实现观测与性能诊断统一。

## Results
- 文本**没有提供正式论文式定量实验结果**，没有给出基准数据集、对照方法、准确率/吞吐等标准评测数字。
- 其最强的具体产品化主张是：**几秒内**即可将 ROS 2 topic 流入 Rerun viewer，并通过 `rewire record -a` 进行全量记录/可视化。
- 部署复杂度被压缩为**单个 Rust 二进制**，并宣称**不需要 ROS 2 runtime**、不需要 colcon/ament/workspace，这相对传统 ROS 2 工具链是显著的工程简化。
- 协议兼容方面，宣称可同时支持**3 类传输/中间件族**：CycloneDDS、FastDDS、Zenoh，并能跨底层协议发现 topic。
- 覆盖的数据类型包括**至少 6 类常见机器人数据**：images、pointclouds、TF、poses、laser scans、odometry，外加自动从 `/robot_description` 生成机器人模型可视化与完整变换树。
- 监控方面，宣称对**每个订阅 topic**提供 4 类运行指标：Hz、bandwidth、drops、latency，可在同一 viewer 中统一查看，无需额外工具。

## Link
- [https://rewire.run](https://rewire.run)
