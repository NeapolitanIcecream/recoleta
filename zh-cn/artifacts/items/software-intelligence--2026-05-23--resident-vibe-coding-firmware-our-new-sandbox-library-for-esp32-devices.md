---
source: hn
url: https://interconnected.org/home/2026/05/20/resident
published_at: '2026-05-23T23:41:37'
authors:
- bertwagner
topics:
- ai-authored-code
- firmware-sandbox
- esp32
- embedded-agents
- human-ai-interaction
- edge-software
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)

## Summary
## 摘要
Resident 让 AI 代理和用户通过沙箱把 Lua 应用热加载到 ESP32 设备上，不需要编译或刷写固件。核心主张是，AI 应该编写在本地运行的小型设备应用，而不是在物理交互的实时事件循环里直接介入。

## 问题
- 物理设备界面需要快速的本地响应；作者把 150 毫秒作为交互是否“立刻响应”的阈值。
- 云端 LLM 调用会增加网络延迟；即使更快的边缘推理，也仍然需要云端保存的个人上下文，比如记忆、Gmail 或 Wikipedia。
- 让 AI 编写完整固件有风险，因为固件可以控制硬件、网络栈和其他底层设备能力。

## 方法
- Resident 在 ESP32 设备上加入了一个嵌入式 Lua 运行时。
- 设备开发者把选定的硬件功能暴露成驱动 API，例如按钮事件和显示写入，而处于沙箱中的应用不能访问未受限制的能力，例如网络栈。
- 应用可以通过 websocket 经由 Wi‑Fi 推送到设备上，并立即在沙箱中运行，不需要编译步骤，也不需要刷写固件。
- 这次发布包含 Claude skills，用来为兼容设备创建、验证并推送应用，还提供示例和一个面向 M5StickS3 风格设备的浏览器模拟器。
- Resident 使用 Courier 做本地设备间消息传递，包括在网络连接中断时使用 UDP 组播。

## 结果
- 摘要没有给出 Resident 的基准测试结果，也没有提供应用加载延迟、内存占用、安全测试通过率或设备兼容数量的实测数据。
- Resident 以 MIT 许可证发布，版本为 alpha v0.5.0。
- 作者说他们在 Inanimate 的所有产品原型工作中都使用 Resident。
- 这个库面向 ESP32 设备，并在 M5StickS3 硬件上展示，该设备包含 ESP32、屏幕、电池、按钮、蜂鸣器和 IMU。
- 最明确的能力主张是热加载：应用代码可以通过 websocket 到达，并在设备上的沙箱里立刻运行，不需要重新编译或重新刷写固件。
- 引用的动机点提到 Taalas 在 Llama 3.1 8B 上为每个用户提供每秒 17k token，但那是外部硬件性能，不是 Resident 的结果。

## Problem

## Approach

## Results

## Link
- [https://interconnected.org/home/2026/05/20/resident](https://interconnected.org/home/2026/05/20/resident)
