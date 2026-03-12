---
source: hn
url: https://github.com/novynlabs-repo/Jarvey
published_at: '2026-03-07T23:04:06'
authors:
- AhmedAshraf
topics:
- desktop-agent
- computer-use-agent
- voice-interface
- macos-automation
- gui-agent
relevance_score: 0.16
run_id: materialize-outputs
---

# Show HN: Jarvey - a local JARVIS for MacOS

## Summary
Jarvey 是一个本地运行的 macOS 语音优先桌面代理，可通过语音控制电脑完成跨应用的图形界面操作。它把原生 macOS 控制、语音流式交互、任务规划和本地记忆结合在一起，但本质上是一个工程系统展示而非学术论文。

## Problem
- 解决的问题是：让用户用自然语音直接操作 macOS 桌面，而不必手动点击、输入和切换应用。
- 这很重要，因为许多桌面工作流是跨应用、多步骤、基于 GUI 的，传统语音助手通常缺乏可靠的桌面执行能力。
- 同时，电脑使用代理具有高风险，会涉及点击、输入、文件修改和账户操作，因此需要本地化部署、权限控制和审批机制。

## Approach
- 核心机制很简单：用户按下全局热键并说出指令，Jarvey 监听语音，把请求送入语音模型与规划模型，再调用本地鼠标、键盘和截图工具去执行桌面操作。
- 系统由原生 Swift 覆盖层应用、本地 Node sidecar、隐藏的 WKWebView 语音运行时、以及本地输入桥组成，均在用户机器上运行。
- 语音部分通过 OpenAI Realtime 进行低延迟音频流；任务规划部分使用 GPT-5.4 supervisor 协调 GUI 与 workbench specialists 执行多步任务。
- 它提供本地 SQLite 持久记忆、审批中心、权限引导，以及仅绑定到 127.0.0.1 的本地服务，以减少暴露面。

## Results
- 文本未提供标准学术实验、基准数据集或量化指标，因此没有可报告的准确率、成功率、延迟对比或基线比较数字。
- 具体能力声明包括：可执行打开应用、填写表单、导航 UI、管理文件、鼠标点击、拖拽、滚动、键盘输入和截图等桌面操作。
- 架构层面的明确实现细节包括 **2 个本地 HTTP 服务**（`127.0.0.1:4818` sidecar 与 `127.0.0.1:4819` input bridge），以及本地状态目录 `~/Library/Application Support/Jarvey/`。
- 构建与运行要求中给出了 **Node.js 20 或 22**、**Swift 6** 等工程约束；发布产物是自包含的 macOS zip/app，内置 sidecar、voice runtime 和 vendored Node runtime。
- 最强的实际主张不是性能突破，而是产品化集成：语音优先、本地桌面控制、持久记忆、审批与权限管理被打包为一个可直接运行的 macOS 代理。

## Link
- [https://github.com/novynlabs-repo/Jarvey](https://github.com/novynlabs-repo/Jarvey)
