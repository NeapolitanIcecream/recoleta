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
language_code: en
---

# Show HN: Rewire – Stream ROS 2 topics to Rerun with no ROS 2 runtime required

## Summary
Rewire is a real-time visualization bridge from ROS 2 to Rerun for robotics development, positioned around directly observing topic data on the network without requiring a ROS 2 runtime. It emphasizes zero-intrusion deployment, out-of-the-box message mapping, and unified monitoring capabilities for real-world robot debugging workflows.

## Problem
- In robotics development, real-time inspection of ROS 2 topics, sensor data, and TF relationships usually depends on a full ROS 2 environment, with high setup costs for installation, compilation, and workspace configuration.
- Existing visualization/debugging pipelines can easily introduce additional interference into the ROS graph, and different DDS/transport protocols, QoS, and custom messages further increase usage complexity.
- In real-world robotics workflows, developers need not only to view data, but also to monitor runtime status such as Hz, bandwidth, packet drops, and latency at the same time, which usually requires stitching together extra tools.

## Approach
- The core approach is to provide a **standalone pure Rust binary bridge** that connects natively to DDS and Zenoh at the network layer, rather than joining the system as a ROS 2 node, so it does not require colcon, ament, or sourcing a ROS 2 workspace.
- It automatically discovers ROS 2 topics and directly maps common message types to Rerun visualization archetypes, such as images, pointclouds, TF, poses, laser scans, and odometry.
- For types not supported by default, users can map ROS 2 types to Rerun through JSON5 configuration, without writing code or recompiling.
- The system also automatically reads `/robot_description` for robot model visualization, maintains the full transform tree, and automatically subscribes and unsubscribes as topics appear and disappear.
- In addition to the data streams, it also streams each topic’s Hz, bandwidth, drops, and latency into Rerun, enabling observation and debugging in a single interface.

## Results
- The text **does not provide formal paper-style quantitative benchmark results** and does not report numerical improvements on public datasets, standard tasks, or against baseline methods.
- Explicit product-level capability claims include streaming ROS 2 topics to the Rerun viewer within **seconds**, and full-recording via `rewire record -a`.
- It supports native connectivity to **3 protocol/implementation types** at the same time: CycloneDDS, FastDDS, and Zenoh, and claims topic discovery across underlying protocols.
- Supported monitoring metrics include **4 per-topic runtime metrics**: Hz, bandwidth, drops, and latency, all visualized alongside the raw data.
- Out-of-the-box support covers many common message types: images, pointclouds, TF, poses, laser scans, odometry, etc., and it supports automatically generating robot model visualization from `/robot_description`.
- Its strongest concrete claim is: **no ROS 2 runtime required, no workspace compilation required, no interference with the ROS graph as a ROS 2 node, and automatic handling of QoS negotiation and TransientLocal late-joiner data.**

## Link
- [https://rewire.run](https://rewire.run)
