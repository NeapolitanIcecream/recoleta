---
source: arxiv
url: https://arxiv.org/abs/2605.09055v1
published_at: '2026-05-09T16:57:11'
authors:
- Quilee Simeon
- Justin M. Wei
- Yile Fan
topics:
- hardware-discovery
- mcp-tools
- robot-control
- agentic-robotics
- self-healing-systems
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Octopus Protocol: One-Shot Hardware Discovery and Control for AI Agents via Infrastructure-as-Prompts

## Summary
## 摘要
Octopus Protocol 让一个编码代理去发现已连接的硬件，生成 MCP 工具，并通过一条启动命令部署一个可用的硬件服务器。论文针对的是阻碍代理控制新设备的驱动和 SDK 工作。

## 问题
- 像 Code-as-Policies 和 VLA 策略这样的 agentic robotics 系统，通常默认已经存在 ROS 节点、SDK、驱动或动作 API。
- 新硬件的初始化仍然需要人去检查设备、编写胶水代码、安装依赖、暴露控制原语，并在故障后修复。
- 这很重要，因为在 AI 代理真正能在物理世界中行动之前，硬件集成往往会占掉主要工程成本。

## 方法
- 系统运行一个五阶段流水线：探测 OS 设备、识别能力、生成带类型的 MCP 工具 schema、编写 FastMCP 服务器，然后部署一个 HTTP/SSE 端点。
- 编码代理在设置时把 markdown 硬件规格和实时探测结果编译成平台特定的驱动代码。
- 生成的工具可以包括 `set_servo_angle` 和 `capture_image` 这类动作，带类型的输入会暴露给任何兼容 MCP 的客户端。
- 一个持久运行的守护进程监控日志，在失败后修复生成的代码或依赖，并使用生成出来的相机工具总结物理状态。

## 结果
- 一条启动命令让硬件在大约 10-15 分钟内完成接入，并根据检测到的平台和设备暴露最多 30 个 MCP 工具。
- 同一份 markdown 规格可在 3 台主机上运行：Windows/WSL PC、Apple Silicon macOS 和 Raspberry Pi 4。
- Raspberry Pi 配置通常暴露约 18 个工具；Mac 配置接近 30 个工具上限。
- 在带 USB 相机反馈的台式 SO-ARM101 6 自由度机械臂上，MCP 客户端通过拍摄图像、观察姿态、移动关节、再拍一次图像来完成闭环视觉-运动控制。
- 自修复阶段处理了 3 个人为引入的故障：缺少 Python 依赖、USB 机械臂热插拔、以及故意破坏生成的服务器代码。
- 编排器通过了 14/14 个集成测试，使用了大约 640 行 Python 代码和大约 560 行 markdown 规格；运行时 MCP 服务器在设置期间生成。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09055v1](https://arxiv.org/abs/2605.09055v1)
