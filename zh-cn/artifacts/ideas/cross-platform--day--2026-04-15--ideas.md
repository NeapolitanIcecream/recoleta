---
kind: ideas
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- flutter
- dart
- jaspr
- documentation-sites
- partial-hydration
- webassembly
tags:
- recoleta/ideas
- topic/flutter
- topic/dart
- topic/jaspr
- topic/documentation-sites
- topic/partial-hydration
- topic/webassembly
language_code: zh-CN
---

# Dart documentation stack migration

## Summary
Flutter 的 Jaspr 迁移支持 Dart 团队运行文档站点时做三件具体的事：为一个内容属性测试只用 Dart 的迁移路径，围绕部分水合封装交互式文档元素，以及为实验性 WebAssembly 使用增加明确的兼容性检查。现有证据最强的是贡献者工作流、栈整合，以及静态 HTML 加交互岛的架构。它在可测量性能、维护成本和浏览器覆盖方面证据很少，这些结论需要本地验证。

## Jaspr migration starter for Dart-owned documentation sites
对于已经用 Flutter 开发、文档却放在单独的 Node.js 或 Python 工具链上的团队来说，Dart 优先的文档栈迁移现在是一个可行选择。Flutter 把 dart.dev、flutter.dev 和 docs.flutter.dev 迁到 Jaspr，保留了通过 Jaspr Content 处理 Markdown 和数据加载的工作流，并把贡献者环境简化为只需要 Dart。这里的实际问题是内容站点的贡献者摩擦，这类站点通常由产品工程师和文档团队维护，他们本来就用 Dart，却要在 Web 层切换工具。

更实际的做法是先把单个文档站点作为迁移起点，而不是直接重写整个站点。保留 Markdown 内容，用 Jaspr 重建共享页面模板和文档交互组件，并测试新贡献者在只安装 Dart SDK 的情况下，是否能完成克隆、运行、编辑和发布。这最适合内容密集、交互量少、而且多个 Web 属性之间维护工作重复的团队。现有证据支持工作流和栈整合这条路。它还不能证明站点性能更好，或者长期成本更低，除非做本地测量。

### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 确认 dart.dev、flutter.dev 和 docs.flutter.dev 生产迁移到 Jaspr，以及统一为 Dart-only 贡献者体验的目标。
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 描述了之前 Node.js 和 Python 分开的栈、更高的设置摩擦、更少的代码共享，以及对更丰富文档交互功能的需求。
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 总结 Jaspr Content 让 Markdown、模板和数据加载工作流保持接近原有流程。

## Partially hydrated interactive documentation components in Jaspr
文档页面里带少量交互元素的部分水合，现在在 Dart 生态里有了一个明确的生产参考。Flutter 的做法是把页面预渲染成静态 HTML，只给需要交互的组件附加客户端逻辑。目标场景很清楚：文档页、教程页和参考页，大部分内容是静态的，但有些部分需要更丰富的代码示例、测验，或其他小型客户端行为。

下一步可以给文档团队做一个小而专的组件库：代码示例运行器、可展开的 API 示例、测验块，或版本感知提示，全部做成只在使用处水合的 Jaspr 组件。低成本的验证方式是页面级检查：先看没有 JavaScript 时的 HTML 输出，再确认只有那些交互岛加载了客户端代码。现有证据足以支持内容密集站点采用这种架构。它还不足以说明 Core Web Vitals 会具体变好，因为文章没有公布基准数据。

### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 说明 Jaspr 支持部分水合，页面先静态 HTML 预渲染，再只给需要交互的组件附加客户端逻辑。
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 把更丰富的代码示例和测验点名为在旧方案里难加上的具体交互功能。
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 指出文章声称加载快、SEO 更好，但没有提供量化性能指标。

## WebAssembly compatibility checks for Jaspr documentation features
dart.dev 上的实验性 WebAssembly 支持，说明在更大范围推广前应该先加一条浏览器覆盖和回退测试线，而不是直接据此宣称性能更好。文章说 dart.dev 已经在兼容浏览器上使用实验性的 WebAssembly 支持，但没有公布性能差值或覆盖数据。对于考虑走同样路线的团队，眼下最缺的是可观测性：哪些浏览器走 WebAssembly 路径、它们如何回退，以及文档交互是否会出错。

这里具体要做的是围绕一个文档交互组件加一项发布检查。记录浏览器家族、选择的运行时路径、水合成功情况和可见故障。在兼容性检查通过之前，把功能留在受限范围内，直到数据证明它在文档受众实际使用的浏览器上都稳定。这是给在公开文档站点上采用 Jaspr 的团队准备的支持层工作，浏览器差异比基准演示更重要。

### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 说明 dart.dev 已在兼容浏览器上使用实验性 WebAssembly 支持，而文章没有提供性能差值或浏览器覆盖数据。
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): 确认文章讨论了 Jaspr 的持续投入和试用准备度，同时把部署细节留给采用者。
