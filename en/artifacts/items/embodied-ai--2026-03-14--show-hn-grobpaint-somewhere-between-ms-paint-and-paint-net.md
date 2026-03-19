---
source: hn
url: https://github.com/groverburger/grobpaint
published_at: '2026-03-14T22:41:28'
authors:
- __grob
topics:
- image-editor
- cross-platform
- vanilla-javascript
- pywebview
- layered-editing
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: GrobPaint: Somewhere Between MS Paint and Paint.net

## Summary
GrobPaint is a lightweight, cross-platform image editor positioned somewhere between MS Paint and Paint.NET, focused on being “useful without bloat.” It is implemented with native web technologies and a tiny Python backend, providing an alternative on platforms such as macOS where Paint.NET is not supported.

## Problem
- The problem it solves is that Paint.NET does not support macOS, while heavier editors are too complex or bloated, leaving users without a cross-platform, lightweight, yet feature-complete middle option.
- This matters because many users only need common capabilities such as layers, selections, basic drawing, and file export, not Photoshop-level complexity.
- The project also attempts to reduce development and distribution complexity by avoiding npm, bundlers, and heavy dependencies.

## Approach
- The core approach is simple: the frontend uses **vanilla JavaScript + ES modules** to implement the editor itself, while the backend is only a very small **Python + pywebview** shell to provide native window capabilities.
- If pywebview is not available, it automatically falls back to browser mode; you can also open `index.html` directly, using browser file input/download in place of native file dialogs.
- The feature design focuses on “the tools you actually need”: layers, 16 blend modes, rectangular/magic-wand selection, common drawing tools, canvas zoom/pan, clipboard paste, multi-document tabs, sprite sheet handling, and so on.
- The project format `.gbp` uses a **ZIP + manifest.json + layered PNGs** structure to store layers, opacity, visibility, and blend modes, making the mechanism direct and easy to port.
- The engineering implementation emphasizes minimalism: about **2,500 lines** of vanilla JavaScript split into **4 modules**, with almost no extra dependencies beyond JSZip on the browser side, and no npm, bundler, or build step.

## Results
- The text **does not provide formal benchmark tests or quantitative results from user studies**, so there are no precise performance, efficiency, or comparative metrics to report.
- The most concrete result given is feature coverage: support for **16 blend modes**, a variety of drawing/selection/transformation tools, and **PNG/JPEG/BMP/GIF** plus the native `.gbp` format.
- In terms of engineering scale, the application is about **2,500 lines of vanilla JavaScript**, split into **4 modules**, with a Python dependency requirement of **Python 3.9+**.
- For distribution, `build.sh` can generate `dist/GrobPaint.app` on macOS or a binary version, indicating that cross-platform availability and deployability are key selling points.
- Compared with Paint.NET/Photoshop, the core claim of this work is not a performance breakthrough, but achieving a balance between **cross-platform support, lightweight implementation, low dependency overhead** and **practical editing capabilities**.

## Link
- [https://github.com/groverburger/grobpaint](https://github.com/groverburger/grobpaint)
