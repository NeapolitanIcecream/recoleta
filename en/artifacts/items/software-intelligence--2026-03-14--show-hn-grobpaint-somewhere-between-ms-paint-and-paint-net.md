---
source: hn
url: https://github.com/groverburger/grobpaint
published_at: '2026-03-14T22:41:28'
authors:
- __grob
topics:
- image-editor
- cross-platform
- vanilla-js
- python-backend
- desktop-app
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Show HN: GrobPaint: Somewhere Between MS Paint and Paint.net

## Summary
GrobPaint is a lightweight cross-platform image editor that sits somewhere between MS Paint and Paint.NET, with a focus on providing sufficiently practical drawing and layer capabilities on platforms such as macOS. It is implemented with native web technologies and a very small Python backend, emphasizing no build step, low dependencies, and direct runnability.

## Problem
- It addresses the issue that Paint.NET cannot run on macOS, while heavier tools are too bloated.
- It targets users who only need common drawing, layer, selection, and export features, lowering the barrier to installation, building, and use.
- This matters because a lightweight cross-platform image editor can fill the practical gap for a tool that is “capable enough without being complex.”

## Approach
- The core approach is to build the frontend with **vanilla JavaScript + ES modules**, then use a very small **Python + pywebview** wrapper to provide a native window; there is no npm, no bundler, and no build step.
- At the simplest level, it turns common image-editing capabilities into a directly runnable web app, then wraps it with Python on desktop for a more native experience.
- Feature-wise, it provides a layer system, 16 blend modes, common drawing/selection/transformation tools, color tools, zoom/pan, multi-document support, and clipboard paste.
- It preserves layer information through the native `.gbp` project format; this format is essentially a ZIP containing `manifest.json` and PNGs for each layer, making persistence and export straightforward.
- It can run in pywebview, or fall back to browser mode; you can even open `index.html` directly, though file dialogs will fall back to browser upload/download.

## Results
- It provides a fairly complete set of “good-enough” editor capabilities: **16 blend modes**, various drawing and selection tools, layer add/delete/edit/merge, opacity control, cropping, scaling, flipping, sprite sheet processing, and more.
- The codebase is about **2,500 lines of vanilla JavaScript**, split into **4 modules**, with very few dependencies; aside from optional `pywebview`, the browser side mentions only **1 CDN dependency (JSZip)**.
- Runtime requirement is **Python 3.9+**; it can be launched directly via `python grobpaint.py`, and can be packaged into a **macOS app** or binary version.
- The text **does not provide standard datasets, benchmarks, or quantitative performance metrics**, so there are no verifiable numerical results for accuracy, speed, or user studies.
- The strongest concrete claim is that, under the constraints of **cross-platform support, low dependencies, and no build pipeline**, it covers most core editing needs between MS Paint and Paint.NET, especially filling the Paint.NET-like gap on macOS.

## Link
- [https://github.com/groverburger/grobpaint](https://github.com/groverburger/grobpaint)
