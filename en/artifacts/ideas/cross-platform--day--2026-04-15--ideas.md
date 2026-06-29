---
kind: ideas
granularity: day
period_start: '2026-04-15T00:00:00'
period_end: '2026-04-16T00:00:00'
run_id: 95ddfeb3-8596-47d3-a754-1f06f3ce2df9
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
language_code: en
pass_output_id: 52
pass_kind: trend_ideas
upstream_pass_output_id: 51
upstream_pass_kind: trend_synthesis
---

# Dart documentation stack migration

## Summary
Flutter’s Jaspr migration supports three concrete moves for Dart teams running documentation sites: test a Dart-only migration path for one content property, package interactive doc elements around partial hydration, and add explicit compatibility checks around experimental WebAssembly use. The evidence is strongest on contributor workflow, stack consolidation, and the static-HTML-plus-interactive-islands architecture. It is thin on measured performance, maintenance cost, and browser coverage, so those claims need local validation.

## Jaspr migration starter for Dart-owned documentation sites
A Dart-first documentation stack migration is now a concrete option for teams that already build with Flutter and keep docs on separate Node.js or Python tooling. Flutter moved dart.dev, flutter.dev, and docs.flutter.dev onto Jaspr, kept Markdown and data-loading workflows through Jaspr Content, and reduced contributor setup to Dart alone. The operational pain here is contributor friction on content sites owned by product engineers and docs teams who already work in Dart but have to switch tools for the web layer.

The practical build is a migration starter for one documentation property, not a full site rewrite pitch. Keep Markdown content, rebuild shared page templates and interactive doc widgets in Jaspr, and measure whether a new contributor can clone, run, edit, and ship with only the Dart SDK installed. This is most relevant for teams with content-heavy sites, a small amount of interactivity, and repeated maintenance work across multiple web properties. The evidence supports the workflow and stack-consolidation case. It does not yet support a claim about better site performance or lower long-term cost without local measurement.

### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Confirms the production migration of dart.dev, flutter.dev, and docs.flutter.dev to Jaspr and the goal of a unified Dart-only contributor experience.
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Describes the prior Node.js and Python split, higher setup friction, reduced code sharing, and the need for richer interactive documentation features.
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Summarizes that Jaspr Content preserved Markdown, templating, and data-loading workflows close to the previous process.

## Partially hydrated interactive documentation components in Jaspr
Partial hydration for documentation pages with small interactive elements now has a named production reference inside the Dart ecosystem. Flutter describes prerendering pages as static HTML and attaching client logic only to components that need interaction. The target use case is clear: documentation pages, tutorial pages, and reference pages where most content is static but some sections need richer code samples, quizzes, or other small client-side behavior.

A useful next step is a narrow component library for documentation teams: code sample runners, expandable API examples, quiz blocks, or version-aware notices built as Jaspr components that hydrate only where used. The cheap validation is page-level: check HTML output without JavaScript, then confirm that only the interactive islands load client code. The current evidence is enough for this architecture on content-heavy sites. It is not enough to claim specific Core Web Vitals gains because the post does not publish benchmark numbers.

### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): States that Jaspr supports partial hydration, with static HTML prerendering and client logic attached only to components that need interaction.
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Names richer code samples and quizzes as concrete interactive features that were hard to add in the older setup.
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Notes that the post claims quick loading and SEO benefits but does not provide quantitative performance metrics.

## WebAssembly compatibility checks for Jaspr documentation features
Experimental WebAssembly support on dart.dev is a reason to add a browser-coverage and fallback test lane before wider rollout, not a reason to make performance claims. The article says dart.dev already uses experimental WebAssembly support on compatible browsers, but it does not publish performance deltas or coverage data. For teams considering the same path, the immediate operational gap is observability: which browsers receive the WebAssembly path, what fallback path they take, and whether any documentation interaction breaks.

The concrete build here is a release check around one interactive documentation component. Record browser family, selected runtime path, hydration success, and visible failures. Keep the feature behind compatibility checks until the data shows stable behavior across the browsers your documentation audience actually uses. This is a support-layer task for teams adopting Jaspr on public docs sites where browser variance matters more than benchmark demos.

### Evidence
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): States that dart.dev already uses experimental WebAssembly support on compatible browsers and that the post provides no performance deltas or browser coverage figures.
- [We rebuilt Flutter’s websites with Dart and Jaspr](../Inbox/2026-04-15--we-rebuilt-flutters-websites-with-dart-and-jaspr.md): Confirms the article’s discussion of ongoing investment in Jaspr and its readiness to try, while leaving deployment details to adopters.
