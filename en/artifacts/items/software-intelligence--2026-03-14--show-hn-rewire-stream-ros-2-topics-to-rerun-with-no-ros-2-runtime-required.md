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
language_code: en
---

# Show HN: Rewire – Stream ROS 2 topics to Rerun with no ROS 2 runtime required

## Summary
Rewire is a visualization bridge tool for robotics development that can stream ROS 2 topics into Rerun in real time, without requiring ROS 2 runtime to be installed or running on the target machine. It emphasizes zero intrusion, single-binary deployment, and direct compatibility with multiple middleware protocols, lowering the barrier to observing and debugging ROS 2 data.

## Problem
- In robotics development, real-time viewing of ROS 2 topics, TF, images, point clouds, and other data usually depends on a full ROS 2 environment, making installation, builds, and workspace management complex.
- Existing debugging/visualization workflows often introduce ROS nodes, workspaces, or additional toolchains, increasing deployment burden and potentially interfering with the existing ROS graph.
- Cross-DDS/Zenoh protocol support, dynamic topic discovery, QoS handling, and performance monitoring are scattered across multiple tools, making rapid diagnosis of real-world robotic systems harder.

## Approach
- The core approach is to provide a **pure Rust single-binary bridge** that directly "observes" ROS 2 communication at the network layer, with native support for DDS and Zenoh, so there is no need for colcon, ament, sourcing, or a full ROS 2 runtime.
- It automatically maps common ROS 2 messages to Rerun visualization archetypes, with out-of-the-box support for data such as images, point clouds, TF, poses, laser scans, and odometry.
- For non-default or custom types, users can map ROS 2 types to Rerun archetypes via JSON5 configuration, without writing code or recompiling; sourcing the workspace is only needed when using custom message types.
- The system automatically discovers new topics, subscribes/unsubscribes automatically, and handles CycloneDDS, FastDDS, Zenoh, QoS negotiation, TransientLocal late-joiner data, and large-buffer BestEffort UDP support.
- In addition to data visualization, it also outputs each topic's Hz, bandwidth, drops, and latency as Rerun entities, unifying observability and performance diagnostics.

## Results
- The text **does not provide formal paper-style quantitative experimental results**; it does not give benchmark datasets, comparison methods, or standard evaluation metrics such as accuracy or throughput.
- Its strongest concrete product claim is that ROS 2 topics can be streamed into the Rerun viewer within **seconds**, with full recording/visualization via `rewire record -a`.
- Deployment complexity is reduced to a **single Rust binary**, and it claims **no ROS 2 runtime required**, with no need for colcon/ament/workspace, which is a significant engineering simplification compared with traditional ROS 2 toolchains.
- In terms of protocol compatibility, it claims simultaneous support for **3 transport/middleware families**: CycloneDDS, FastDDS, and Zenoh, with topic discovery across underlying protocols.
- The covered data types include **at least 6 common robotics data types**: images, pointclouds, TF, poses, laser scans, and odometry, plus automatic robot model visualization and a full transform tree generated from `/robot_description`.
- For monitoring, it claims to provide 4 runtime metrics for **every subscribed topic**: Hz, bandwidth, drops, and latency, all viewable in the same viewer without additional tools.

## Link
- [https://rewire.run](https://rewire.run)
