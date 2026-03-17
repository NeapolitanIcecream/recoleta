---
source: hn
url: https://rewire.run
published_at: '2026-03-14T23:22:38'
authors:
- alvgaona
topics:
- ros2-tooling
- robot-visualization
- rerun
- real-time-debugging
- dds
- zenoh
relevance_score: 0.29
run_id: materialize-outputs
---

# Show HN: Rewire – Stream ROS 2 topics to Rerun with no ROS 2 runtime required

## Summary
Rewire 是一个面向机器人开发的 ROS 2 到 Rerun 的实时可视化桥接工具，主打无需 ROS 2 运行时即可直接观察网络中的主题数据。它强调零侵入部署、开箱即用的消息映射，以及对真实机器人调试工作流的统一监控能力。

## Problem
- 机器人开发中，实时查看 ROS 2 主题、传感器数据和 TF 关系通常依赖完整 ROS 2 环境，安装、编译和工作区配置成本高。
- 现有可视化/调试链路容易对 ROS 图产生额外干扰，且不同 DDS/传输协议、QoS 和自定义消息会增加使用复杂度。
- 在真实机器人工作流里，开发者不仅需要看数据，还需要同时看 Hz、带宽、丢包和延迟等运行状态，这通常需要额外工具拼接。

## Approach
- 核心方法是提供一个**独立的纯 Rust 二进制桥接器**，直接在网络层原生接入 DDS 和 Zenoh，而不是作为 ROS 2 节点加入系统，因此无需 colcon、ament 或 source ROS 2 工作区。
- 它会自动发现 ROS 2 主题，并把常见消息类型直接映射为 Rerun 的可视化 archetypes，例如图像、点云、TF、位姿、激光扫描和里程计。
- 对于未默认支持的类型，用户可通过 JSON5 配置把 ROS 2 类型映射到 Rerun，无需写代码或重新编译。
- 系统还会自动读取 `/robot_description` 做机器人模型可视化，并维护完整变换树，同时对新出现/消失的主题自动订阅与退订。
- 除数据流外，它把每个主题的 Hz、带宽、丢包和延迟也一起流入 Rerun，实现单界面观测与调试。

## Results
- 文本**没有提供正式论文式定量基准结果**，未报告在公开数据集、标准任务或与基线方法相比的数值提升。
- 明确的产品级能力声明包括：**几秒内**将 ROS 2 主题流式传到 Rerun viewer，并可通过 `rewire record -a` 进行全量记录。
- 支持同时原生接入 **3 类协议/实现**：CycloneDDS、FastDDS、Zenoh，并声明可跨底层协议发现主题。
- 支持的监控指标包括 **4 类每主题运行指标**：Hz、bandwidth、drops、latency，且与原始数据一起可视化。
- 开箱即用覆盖多种常见消息：images、pointclouds、TF、poses、laser scans、odometry 等，并支持从 `/robot_description` 自动生成机器人模型可视化。
- 其最强具体主张是：**无需 ROS 2 runtime、无需工作区编译、不会作为 ROS 2 节点干扰 ROS graph、可自动处理 QoS 协商与 TransientLocal late-joiner 数据。**

## Link
- [https://rewire.run](https://rewire.run)
