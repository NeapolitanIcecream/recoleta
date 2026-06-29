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
## 总结
Flutter 和 Dart 把 dart.dev、flutter.dev 和 docs.flutter.dev 迁移到 Jaspr，让这些网站改用一套基于 Dart 的技术栈，替代原先分开的 Node.js 和 Python 系统。文章认为，这样可以降低贡献门槛，也让带少量交互的静态站点更容易构建。

## 问题
- 这三个站点原来用的技术栈不同：文档站点用的是运行在 Node.js 上的 Eleventy，flutter.dev 用的是基于 Python/Django 的 Wagtail。
- 这种分裂提高了维护成本，减少了代码共享，也要求贡献者学习 Dart 之外的工具。
- 旧方案让富代码示例和测验这类交互功能更难加入，因为它们往往需要一次性的 DOM 代码。

## 方法
- 团队用 **Jaspr** 重建了这三个站点。Jaspr 是一个 Dart Web 框架，支持静态站点生成、服务端渲染和客户端渲染。
- 他们用 **Jaspr Content** 处理基于 Markdown 的内容、模板和数据加载，这样现有的写作和内容流程就能尽量保持和旧流程接近。
- Jaspr 的组件模型按设计会让 Flutter 开发者感到熟悉，这样贡献者在构建基于 DOM 的网页时，可以复用 Dart 和 Flutter 的知识。
- 在交互部分，这些站点使用 **partial hydration**：页面先预渲染成静态 HTML，客户端逻辑只连接到需要交互的组件。
- 这次迁移也让这些站点和 Dart 工具链保持一致，例如 `dart pub`、`dart format`、`dart analyze` 和 `dart test`，并用到了较新的 Dart 特性，比如点号简写、空安全集合元素、新的 JS 互操作、analyzer 插件以及实验性的 WebAssembly 支持。

## 结果
- 文中提到的三个主要站点都完成了迁移：**dart.dev、flutter.dev 和 docs.flutter.dev**。
- 贡献者工具链收敛成了 **一个 SDK：Dart**，替代了之前某些站点用 **Node.js**、另一些站点用 **Python** 的混合方案。
- 文章称，借助 **静态 HTML + partial hydration**，页面交付更快，SEO 也更好，但没有提供加载时间、Core Web Vitals 或搜索指标的基准数据。
- 文章说内容工作流变化不大，因为 Jaspr Content 已经覆盖了 Markdown、模板和数据加载，但没有给出迁移时间或维护成本的数据。
- 文中提到，**dart.dev** 已经在兼容浏览器上使用实验性的 WebAssembly 支持，但没有给出性能差异或浏览器覆盖率数据。

## Problem

## Approach

## Results

## Link
- [https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4](https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4)
