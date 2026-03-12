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
relevance_score: 0.9
run_id: materialize-outputs
---

# Show HN: Jarvey - a local JARVIS for MacOS

## Summary
Jarvey 是一个面向 macOS 的本地语音优先桌面代理，可通过热键唤起后用自然语言控制电脑执行跨应用任务。它将原生桌面控制、语音实时交互、任务规划和本地记忆组合成一个可实际操作 GUI 的 computer-use agent。

## Problem
- 它要解决的问题是：用户在 macOS 上执行打开应用、填写表单、导航界面、管理文件等多步桌面操作时，流程繁琐、重复且跨应用切换成本高。
- 这很重要，因为真正有用的桌面智能体不仅要“会聊天”，还要能直接对图形界面采取行动，把自然语言指令变成真实的软件操作。
- 同时，电脑控制代理具有高风险，可能点击、输入、批准弹窗、删除数据，因此权限、本地部署和安全边界也成为关键问题。

## Approach
- 核心机制很简单：用户按下全局热键并说出任务，Jarvey 监听语音，把请求发送给模型做规划，再通过本地控制桥执行鼠标、键盘、截图等操作，完成桌面任务。
- 系统由原生 Swift 覆盖层应用、本地 Node sidecar、隐藏的 WKWebView 语音运行时、OpenAI Realtime 语音通道以及 GPT-5.4 规划/工具使用模块组成。
- 在代理架构上，它使用“GPT-5.4 supervisor + specialists”来拆解多步任务，并协调 GUI 操作与工作台类任务执行。
- 为了可用性与持续上下文，系统提供本地 SQLite 持久记忆、审批中心、设置持久化，以及麦克风/录屏/辅助功能权限引导。
- 为了收敛风险，它声明所有本地服务仅绑定到 127.0.0.1，无内置分析或第三方遥测，但会向 OpenAI 发送用户请求、上下文、截图和音频以完成模型交互。

## Results
- 文本未提供标准学术实验、基准数据或量化性能结果，因此没有可报告的准确率、成功率、延迟或 SOTA 数字。
- 它明确声称可执行的任务类型包括：打开应用、填写表单、浏览 UI、管理文件，以及更一般的多步桌面自动化操作。
- 系统给出了较具体的工程能力：全局热键 `Option+Space` 触发、基于 OpenAI Realtime 的低延迟音频流、两类本地 HTTP 服务分别运行在 `127.0.0.1:4818` 和 `127.0.0.1:4819`。
- 发布形态上，它提供自包含的 macOS 压缩包，内含 sidecar、voice runtime 和内置 Node runtime，意味着最终用户无需源码检出即可运行。
- 安全与部署声明是其较强的具体主张：仅限本机回环地址、不暴露到网络、无分析遥测，但它也强调 CUA 具有删除数据和代表用户操作账户的风险。

## Link
- [https://github.com/novynlabs-repo/Jarvey](https://github.com/novynlabs-repo/Jarvey)
