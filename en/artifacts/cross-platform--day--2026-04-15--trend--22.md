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
language_code: en
pass_output_id: 51
pass_kind: trend_synthesis
---

# Flutter’s clearest signal is a real-world Jaspr migration for large documentation sites

## Overview
The period has one publishable signal, and it is concrete: Flutter rebuilt its main websites on Jaspr to keep web publishing inside a Dart-only toolchain. The strongest takeaway is practical. This is a real migration across dart.dev, flutter.dev, and docs.flutter.dev, with partial hydration as the core delivery pattern. The article gives useful implementation detail, but little quantitative evidence on performance or maintenance gains.

## Clusters

### Unified Dart stack for documentation and web properties
Flutter’s web signal for the period is a stack consolidation story. The team moved dart.dev, flutter.dev, and docs.flutter.dev onto Jaspr so site work can stay inside Dart. The concrete benefit is lower contributor setup friction and more code sharing across properties. The post also says Jaspr Content let the team keep Markdown, templating, and data-loading workflows close to the old process, which matters for documentation teams that need migration without a full content rewrite.

#### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summary states the migration target, prior stack split, and workflow continuity via Jaspr Content.

### Partial hydration is the main architectural takeaway
The technical idea with the clearest user-facing effect is partial hydration. Pages are prerendered as static HTML, and client code attaches only where interaction is needed. In this case, the target is documentation-style sites with mostly static pages and small interactive elements such as richer code samples or quizzes. That gives Flutter a practical web pattern for content-heavy sites: static delivery first, selective interactivity where it adds value.

#### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summary describes partial hydration and ties it to static sites with small interactive parts.

### Claims on speed and WebAssembly remain lightly measured
The evidence is strongest on developer workflow and architecture, not on measured performance. The post claims quick page loading, SEO benefits, and experimental WebAssembly use on dart.dev, but it does not publish load-time numbers, Core Web Vitals, search metrics, performance deltas, or browser coverage. That limits how far the period supports broader claims. What is grounded here is a production migration and the shape of the implementation choices behind it.

#### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summary explicitly notes missing benchmark numbers, missing maintenance metrics, and missing WebAssembly deltas.
