---
source: hn
url: https://www.gethopp.app/blog/hate-webkit
published_at: '2026-03-09T23:38:35'
authors:
- birdculture
topics:
- tauri
- webkit
- rust-native-ui
- webrtc
- cross-platform-apps
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# The Cost of 'Lightweight' Frameworks: From Tauri to Native Rust

## Summary
这篇文章不是学术论文，而是一篇工程复盘：作者说明为何基于 Tauri/WebKit 的“轻量级”桌面方案在低延迟远程协作场景中反而带来高成本，并论证将关键窗口迁移到原生 Rust。核心观点是，对依赖 WebRTC、音视频和跨平台一致性的产品，WebKit 的限制会抵消轻量框架的优势。

## Problem
- 文章要解决的问题是：**Tauri + WebKit 是否适合构建超低延迟（目标 **<100ms**）的远程结对编程/屏幕共享应用**，以及当其不适合时应如何替代。
- 这很重要，因为 Hopp 这类产品对 **WebRTC、音视频稳定性、编解码器支持、跨平台一致性和资源占用** 都高度敏感；一旦浏览器内核行为异常，用户会直接感知卡顿、崩溃或功能缺失。
- 作者列举的痛点包括 Safari/WebKit 渲染问题、iOS 页面无日志崩溃、陈旧 user agent 版本、音频异常、AV1 支持受限，以及 **WebKitGTK 默认不支持 WebRTC** 从而阻塞 Linux 支持。

## Approach
- 核心方法很简单：**不再把关键实时交互界面继续建立在 WebKit 窗口上，而是把关键窗口和流媒体逻辑迁到原生 Rust（iced）实现**。
- 这样做的机制是：把原先分散在多个 WebKit 窗口里的 WebRTC/显示/音视频处理，**集中到后端侧统一管理**，减少前后端和多窗口同步复杂度。
- 具体上，作者不选择直接切到 Electron，也不等待 Tauri 的 CEF 支持，而是选择 **局部原生化**：先把最关键的 screensharing/UI 窗口改成 Rust 原生窗口。
- 迁移后，作者预计每个用户不再需要为不同窗口生成 **3 个 LiveKit token**、以 **3 个 participant** 身份入会，而是可以收敛为 **每人 1 个 participant**。
- 另外，后端直接拿到流和缓冲区后，可以绕开浏览器 codec 限制，使用 **libwebrtc 支持的任意 codec**，并探索如 macOS 神经引擎图像超分等能力。

## Results
- 文中**没有正式实验、基准数据或系统性定量对比结果**，因此没有可报告的论文式 SOTA 指标。
- 唯一明确的产品目标数字是：远程控制交互延迟需保持在 **<100ms**，作者引用 Apple 的经验阈值说明高于该水平会让交互显得“clunky”。
- 作者报告了一个具体故障案例：在 iOS Safari 中，页面放置 **3 个 GIF** 就可能触发 “**A problem repeatedly occurred**” 崩溃，且**没有控制台错误或可追踪线索**；他们通过 **IntersectionObserver** 延迟渲染规避。
- 在现有架构中，每个用户需要生成 **3 个 LiveKit tokens**，分别服务于屏幕共享、音频/摄像头、摄像头视图，因此**每个人以 3 个不同参与者身份**加入通话；迁移后宣称可降为 **1 人 1 participant**。
- 作者的最强工程性结论是：对于依赖 WebRTC 和低延迟流媒体的复杂桌面应用，Tauri/WebKit 的“轻量”并不等于低总成本，**原生 Rust 窗口有望提升代码简洁性、codec 自由度、Linux 可行性和可扩展特性空间**。

## Link
- [https://www.gethopp.app/blog/hate-webkit](https://www.gethopp.app/blog/hate-webkit)
