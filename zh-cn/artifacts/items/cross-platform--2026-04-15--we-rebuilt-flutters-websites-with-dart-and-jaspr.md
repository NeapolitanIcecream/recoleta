---
source: rss
url: https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4
published_at: '2026-04-15T18:31:01'
authors:
- Parker Lougheed
topics:
- dart
- jaspr
- web-migration
- static-site-generation
- partial-hydration
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# We rebuilt Flutter’s websites with Dart and Jaspr

## Summary
## 摘要
Flutter 和 Dart 将 dart.dev、flutter.dev 和 docs.flutter.dev 迁移到 Jaspr，让这些网站统一使用一套基于 Dart 的技术栈，不再分别依赖 Node.js 和 Python 系统。文章认为，这样可以降低贡献门槛，也让构建以静态页面为主、带少量交互的网站更容易。

## 问题
- 这三个网站使用不同的技术栈：文档站点使用运行在 Node.js 上的 Eleventy，flutter.dev 使用基于 Python/Django 的 Wagtail。
- 这种拆分提高了维护成本，减少了代码共享，并迫使贡献者学习 Dart 之外的工具。
- 旧方案也让更丰富的代码示例和测验等交互功能更难加入，因为这些功能往往需要一次性的 DOM 代码。

## 方法
- 团队用 **Jaspr** 重建了这三个网站。Jaspr 是一个 Dart Web 框架，支持静态站点生成、服务端渲染和客户端渲染。
- 他们使用 **Jaspr Content** 处理基于 Markdown 的内容、模板和数据加载，这样现有的写作和内容流程可以基本保持接近原来的方式。
- Jaspr 的组件模型刻意做得让 Flutter 开发者感到熟悉，因此贡献者在构建基于 DOM 的网页时可以复用 Dart 和 Flutter 经验。
- 在交互方面，这些网站使用 **partial hydration**：页面先预渲染为静态 HTML，客户端逻辑只附加到需要交互的组件上。
- 这次迁移也让网站与 Dart 工具链保持一致，例如 `dart pub`、`dart format`、`dart analyze` 和 `dart test`，同时也受益于较新的 Dart 特性，例如 dot shorthands、null-aware collection elements、新的 JS interop、analyzer plugins，以及实验性的 WebAssembly 支持。

## 结果
- 文章提到的三个主要网站都已完成迁移：**dart.dev、flutter.dev 和 docs.flutter.dev**。
- 贡献者工具链被压缩到 **一个 SDK：Dart**，替代了此前某些站点需要 **Node.js**、另一个站点需要 **Python** 的混合方案。
- 文章称通过 **静态 HTML + partial hydration** 实现了更快的页面交付和良好的 SEO，但**没有给出**加载时间、Core Web Vitals 或搜索指标的基准数据。
- 文中说，由于 Jaspr Content 已经覆盖 Markdown、模板和数据加载，内容流程变化不大，但**没有提供**迁移时间或维护成本的数据。
- 文中还提到，**dart.dev 已经在兼容浏览器上使用实验性的 WebAssembly 支持**，但没有给出性能差值或浏览器覆盖范围数据。

## Problem

## Approach

## Results

## Link
- [https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4](https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4)
