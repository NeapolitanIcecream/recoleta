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

# Flutter 最清晰的信号是一场面向大型文档站点的真实 Jaspr 迁移

## 概览
这个时间段只有一个可发布的信号，而且很具体：Flutter 把主要网站重建到 Jaspr 上，把网页发布保留在纯 Dart 工具链里。最强的结论很实际。这是一次覆盖 dart.dev、flutter.dev 和 docs.flutter.dev 的真实迁移，部分 Hydration 是核心交付模式。文章给了有用的实现细节，但几乎没有性能或维护收益的量化证据。

## 研究发现

### 面向文档和网页站点的统一 Dart 技术栈
Flutter 在这个时期最明显的网页信号是一次技术栈整合。团队把 dart.dev、flutter.dev 和 docs.flutter.dev 迁到 Jaspr，这样站点工作就能留在 Dart 里完成。直接收益是贡献者配置负担更低，跨站点的代码共享更多。文章还说，Jaspr Content 让团队把 Markdown、模板和数据加载流程保留得和旧流程接近，这对需要迁移但不想重写整套内容的文档团队很重要。

#### 资料来源
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summary states the migration target, prior stack split, and workflow continuity via Jaspr Content.

### 部分 Hydration 是主要的架构结论
最能直接影响用户体验的技术点是部分 Hydration。页面先被预渲染成静态 HTML，只有需要交互的地方才挂载客户端代码。这里的目标是文档类站点，这类站点大多是静态页面，只在少数地方放更丰富的代码示例或测验等交互元素。对内容密集型站点来说，这给 Flutter 提供了一种可用的网页模式：先静态交付，再在有价值的地方加选择性交互。

#### 资料来源
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summary describes partial hydration and ties it to static sites with small interactive parts.

### 关于速度和 WebAssembly 的说法仍然缺少充分测量
证据最强的是开发流程和架构，不是实测性能。文章提到页面加载快、SEO 更好，以及 dart.dev 上的实验性 WebAssembly 用法，但没有公布加载时间、Core Web Vitals、搜索指标、性能差值或浏览器覆盖范围的数据。这限制了这段时间能支持的更大范围判断。这里能确认的是一次生产环境迁移，以及支撑这次迁移的实现选择。

#### 资料来源
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summary explicitly notes missing benchmark numbers, missing maintenance metrics, and missing WebAssembly deltas.
