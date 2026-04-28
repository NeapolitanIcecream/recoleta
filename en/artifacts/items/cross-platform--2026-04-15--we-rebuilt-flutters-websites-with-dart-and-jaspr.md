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
language_code: en
---

# We rebuilt Flutter’s websites with Dart and Jaspr

## Summary
Flutter and Dart migrated dart.dev, flutter.dev, and docs.flutter.dev to Jaspr so their web properties use one Dart-based stack instead of separate Node.js and Python systems. The post argues this cuts contributor friction and makes static sites with small interactive parts easier to build.

## Problem
- The three sites used different stacks: Eleventy on Node.js for documentation sites and Wagtail on Python/Django for flutter.dev.
- That split raised maintenance cost, reduced code sharing, and forced contributors to learn tools outside Dart.
- The older setup made interactive features such as richer code samples and quizzes harder to add because they often needed one-off DOM code.

## Approach
- The team rebuilt all three sites with **Jaspr**, a Dart web framework that supports static site generation, server-side rendering, and client-side rendering.
- They used **Jaspr Content** for Markdown-driven content, templating, and data loading so existing writing and content workflows could stay close to the old process.
- Jaspr’s component model is designed to feel familiar to Flutter developers, which lets contributors reuse Dart and Flutter knowledge when building DOM-based web pages.
- For interactivity, the sites use **partial hydration**: pages are prerendered as static HTML, and client logic attaches only to components that need interaction.
- The migration also aligned the sites with Dart tooling such as `dart pub`, `dart format`, `dart analyze`, and `dart test`, and benefited from newer Dart features like dot shorthands, null-aware collection elements, new JS interop, analyzer plugins, and experimental WebAssembly support.

## Results
- All three major sites named in the post were migrated: **dart.dev, flutter.dev, and docs.flutter.dev**.
- The contributor toolchain was reduced to **one SDK: Dart**, replacing a mixed setup that previously required **Node.js** for some sites and **Python** for another.
- The article claims faster page delivery and good SEO through **static HTML + partial hydration**, but it gives **no benchmark numbers** for load time, Core Web Vitals, or search metrics.
- The post says content workflows changed little because Jaspr Content already covered Markdown, templating, and data loading, but it provides **no migration-time or maintenance-cost numbers**.
- It reports that **dart.dev already uses experimental WebAssembly support on compatible browsers**, but does not give performance deltas or browser coverage figures.

## Link
- [https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4](https://blog.flutter.dev/we-rebuilt-flutters-websites-with-dart-and-jaspr-317c00e8b400?source=rss----4da7dfd21a33---4)
