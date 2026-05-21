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
Octopus Protocol 使用编码代理从一条引导命令开始，发现已连接硬件、生成 MCP 工具，并部署一个实时硬件服务器。论文针对的是阻碍代理控制新设备的驱动和 SDK 工作。

## 问题
- Code-as-Policies 和 VLA 策略等代理式机器人系统通常假定已有 ROS 节点、SDK、驱动或动作 API。
- 新硬件启动仍需要人工检查设备、编写胶水代码、安装依赖、暴露控制原语，并修复故障。
- 这一点很重要，因为在 AI 代理能够作用于物理世界之前，硬件集成可能占据主要工程成本。

## 方法
- 系统运行五阶段流水线：探测 OS 设备、识别能力、生成带类型的 MCP 工具模式、编写 FastMCP 服务器，然后部署 HTTP/SSE 端点。
- 编码代理在设置时把 markdown 硬件规格和实时探测结果编译为面向具体平台的驱动代码。
- 生成的工具可以包括 `set_servo_angle` 和 `capture_image` 等动作，并向任何兼容 MCP 的客户端暴露带类型的输入。
- 常驻守护进程监视日志，在故障后修复生成的代码或依赖，并使用生成的相机工具汇总物理状态。

## 结果
- 一条引导命令可在约 10-15 分钟内完成硬件接入，并根据检测到的平台和设备暴露最多 30 个 MCP 工具。
- 同一份 markdown 规格在 3 台主机上可用：Windows/WSL PC、Apple Silicon macOS 和 Raspberry Pi 4。
- Raspberry Pi 设置通常暴露约 18 个工具；Mac 设置接近 30 个工具的上限。
- 在带 USB 相机反馈的台式 SO-ARM101 6-DOF 机械臂上，MCP 客户端通过拍摄图像、观察姿态、移动关节，并用第二次拍摄验证，执行闭环视觉-运动控制。
- 自修复阶段处理了 3 个诱发故障：缺失 Python 依赖、USB 机械臂热拔插，以及故意破坏生成的服务器。
- 编排器通过了 14 项集成测试中的 14 项，并使用约 640 行 Python 和约 560 行 markdown 规格；运行时 MCP 服务器在设置期间生成。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09055v1](https://arxiv.org/abs/2605.09055v1)
