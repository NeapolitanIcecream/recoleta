---
kind: trend
trend_doc_id: 22
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
topics:
- flutter
- dart
- jaspr
- documentation-sites
- partial-hydration
- webassembly
run_id: materialize-outputs
aliases:
- recoleta-trend-22
tags:
- recoleta/trend
- topic/flutter
- topic/dart
- topic/jaspr
- topic/documentation-sites
- topic/partial-hydration
- topic/webassembly
language_code: zh-CN
---

# Flutter 最明确的信号，是 Jaspr 在大型文档站点中的一次真实迁移

## Overview
这一时期有一个可以发布的明确信号：Flutter 用 Jaspr 重建了其主要网站，把 Web 发布工作放进纯 Dart 工具链。最重要的结论很实际。这是一次覆盖 dart.dev、flutter.dev 和 docs.flutter.dev 的真实迁移，核心交付模式是部分水合。文章提供了有用的实现细节，但几乎没有关于性能或维护收益的量化证据。

## Clusters

### 面向文档与 Web 站点的统一 Dart 技术栈
这一时期 Flutter 在 Web 端最明确的信号是技术栈整合。团队把 dart.dev、flutter.dev 和 docs.flutter.dev 迁移到 Jaspr 上，让网站工作可以留在纯 Dart 工具链内。直接收益是降低了贡献者的环境配置门槛，也提高了不同站点之间的代码复用。文章还提到，Jaspr Content 让团队继续使用与旧流程接近的 Markdown、模板和数据加载工作流，这对需要迁移但不想全面重写内容的文档团队很重要。

#### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 摘要说明了迁移目标、此前分裂的技术栈，以及通过 Jaspr Content 保持工作流连续性。

### 部分水合是最主要的架构结论
对用户影响最直接的技术思路是部分水合。页面先预渲染为静态 HTML，客户端代码只在需要交互的地方附加。在这里，目标场景是以文档为主的网站：大部分页面是静态的，只包含少量交互元素，比如更丰富的代码示例或测验。这给 Flutter 提供了一种适合内容型站点的实用 Web 模式：先用静态方式交付，再只在能带来价值的地方加入交互。

#### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 摘要描述了部分水合，并将它与带有少量交互部分的静态站点联系起来。

### 关于速度和 WebAssembly 的说法仍缺少充分测量
现有证据最有力地支持开发者工作流和架构变化，不足以支持已量化的性能结论。文章提到页面加载更快、SEO 有收益，以及 dart.dev 使用了实验性的 WebAssembly，但没有公布加载时间、Core Web Vitals、搜索指标、性能变化幅度或浏览器覆盖范围的数据。这限制了这一时期材料对更宽泛结论的支撑力度。当前能确定的是一次已在生产环境完成的迁移，以及其背后的实现选择。

#### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 摘要明确指出缺少基准测试数据、缺少维护指标，也缺少 WebAssembly 性能变化数据。
