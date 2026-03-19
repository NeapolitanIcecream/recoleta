---
source: hn
url: https://bokuchi.com/
published_at: '2026-03-12T23:22:44'
authors:
- nogajun
topics:
- markdown-editor
- tauri
- rust
- cross-platform
- lightweight-app
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Bokuchi: A lightweight, cross-platform Markdown editor built with Tauri

## Summary
Bokuchi is a lightweight, cross-platform Markdown editor built with Tauri and Rust, emphasizing real-time preview, low memory usage, and fast startup. It targets users who need a simple and efficient writing tool, highlighting that it is lighter and faster than Electron-based editors.

## Problem
- Many Markdown editors are built on Electron, and common issues include high memory usage and slow startup, which affect the day-to-day writing experience.
- Users typically need a cross-platform, consistent editing experience, along with core productivity features such as real-time preview, multi-document support, and find and replace.
- Lightweight design is important because writing tools should minimize system resource consumption and be available whenever needed.

## Approach
- Build the application with **Tauri + Rust** rather than Electron, achieving a desktop Markdown editor with lower runtime overhead.
- Provide **split-view real-time preview**: editing on the left and instant rendering on the right, reducing the cost of switching between writing and checking formatting.
- Support common writing features such as **multi-document editing**, full-document find and replace, and export placeholders (such as `{{author}}`).
- Improve generality and usability through **cross-platform support** (macOS, Windows, Linux), multiple themes, and configurable settings.
- Offer **14 interface languages** to improve internationalization coverage.

## Results
- Claims that compared with **Electron-based editors**, memory usage is **less than one third** of theirs (that is, under about 33%).
- Claims that the application startup time is **under 1 second**.
- Supports **3 major desktop platforms**: macOS, Windows, Linux.
- Provides **14 UI languages**.
- The text does not provide standard benchmarks, datasets, controlled experiments, or more fine-grained evaluations, so it lacks independently verifiable, academically styled quantitative results.

## Link
- [https://bokuchi.com/](https://bokuchi.com/)
