---
source: rss
url: https://blog.flutter.dev/vibe-once-run-anywhere-with-antigravity-and-flutter-25af06e60a91?source=rss----4da7dfd21a33---4
published_at: '2026-06-29T16:01:02'
authors:
- Craig Labenz
topics:
- flutter
- cross-platform-ui
- ai-coding-agents
- dart
- firebase
- game-development
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Vibe once, run anywhere with Antigravity and Flutter

## Summary
## 摘要
这篇文章认为，Flutter 适合作为 AI 编码代理的目标，因为一个 Dart 代码库可以发布到 Web、移动端和桌面端。文章以 DashLander 为完整示例：这是一个用 Google Antigravity 和 Gemini 工具构建的 Flutter 与 Flame 游戏。

## 问题
- AI 代理可以生成彼此独立的原生应用，但分开的 Android、iOS 和 Web 代码库会增加平台差异、重复 bug 和 token 成本。
- 游戏原型需要在玩法、素材、物理、后端和发布页面之间快速迭代；这些环节都靠人工处理会拖慢验证。
- 当数学、物理、回放时序或碰撞逻辑以难以检查的方式出错时，代理编写的代码很难让人放心。

## 方法
- 构建一个使用 Dart 的跨平台 Flutter 应用，让代理在单一代码库面向多个平台时获得类型错误和 analysis-server 反馈。
- 使用 Antigravity 规划、编辑代码、运行测试、点击 UI，并把后端、UI 和游戏逻辑分给子代理处理。
- 用 Google 工具生成配套素材：Lyria 生成音乐，Stitch 和 Google Canvas 生成 UI 设计，Gemini 生成粒子效果，Nano Banana 生成图标，Gemini Deep Research 查找 RCS 物理公式。
- 先在 AI Studio 中制作原型，再把选定想法迁移到 Flutter、Flame、Firebase、Gemini API 和 Jaspr，用于游戏、后端、AI 功能和营销网站。
- 添加调试叠加层和回放检查点，让人类开发者能检查地形数据、倾斜角、碰撞箱和回放漂移，而不是只凭目视相信代理的数学计算。

## 结果
- 作者称 Antigravity 在约 5 分钟内生成了一个初始的 Flutter 与 Flame 游戏；这类工作通常需要数天，但第一版只有 3 个硬编码关卡，并且存在主要玩法问题。
- 最终版本还需要约 100 条提示，其中很多提示用于代码组织和测试，而不是新增玩法。
- Challenge Mode 没有使用实时多人基础设施，而是回放过去的高分幽灵；作者估计，这用静态存储和更简单的后端实现了约 90% 的目标竞技感。
- 一个回放 bug 来自毫秒级调度漂移；在推进器事件处存储完整着陆器状态后，修复了原本可能在一次运行接近结束时崩溃的幽灵回放。
- 发布流程使用 Antigravity CLI 构建 Flutter Web 应用，把输出复制到 Jaspr，运行构建，并在一个终端工作流中部署到 Firebase Hosting。
- 文章没有提供受控基准测试、用户研究或成本测量。它最具体的主张是已经端到端发布了 dashlander.com 上的 Web 游戏，并且同一个 Flutter 代码库被定位为可构建 iOS、Android、macOS、Windows 和 Linux 版本。

## Problem

## Approach

## Results

## Link
- [https://blog.flutter.dev/vibe-once-run-anywhere-with-antigravity-and-flutter-25af06e60a91?source=rss----4da7dfd21a33---4](https://blog.flutter.dev/vibe-once-run-anywhere-with-antigravity-and-flutter-25af06e60a91?source=rss----4da7dfd21a33---4)
