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
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# Bokuchi: A lightweight, cross-platform Markdown editor built with Tauri

## Summary
Bokuchi is a lightweight, cross-platform Markdown editor built with Tauri and Rust, emphasizing low memory usage, fast startup, and real-time preview. It targets users who need a simple and efficient writing tool, using a lighter technology stack in place of the common Electron approach.

## Problem
- Many Markdown editors rely on Electron, which often brings higher memory usage and heavier runtime overhead.
- Users need a writing tool that runs consistently across macOS, Windows, and Linux, while also launching quickly.
- Beyond basic editing, users also need practical capabilities such as real-time preview, multi-document handling, find and replace, and export placeholders.

## Approach
- Built the application with **Tauri + Rust** rather than Electron to reduce resource consumption and improve startup speed.
- Provides **split editing/preview**: edit Markdown on the left and view a live rendered preview on the right.
- Integrates common writing workflow features such as multi-document support, document-wide find and replace, and variable placeholder expansion during export.
- Offers customizable interface and behavior settings, including multiple themes and support for 14 UI languages.

## Results
- Claims memory usage is **less than one-third** that of **Electron-based editors** (i.e. it uses under 1/3 of the memory).
- Claims startup time is **under 1 second**.
- Supports **3 major desktop platforms**: macOS, Windows, and Linux.
- Provides **14 UI languages**.
- The text does not provide standard benchmarks, datasets, experimental setup, or reproducible results against specific competitors.

## Link
- [https://bokuchi.com/](https://bokuchi.com/)
