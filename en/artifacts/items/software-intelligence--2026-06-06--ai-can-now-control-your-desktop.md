---
source: hn
url: https://clawdcursor.com
published_at: '2026-06-06T23:14:25'
authors:
- AmDab
topics:
- desktop-automation
- mcp
- ai-agents
- human-ai-interaction
- code-intelligence
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# AI Can now control your desktop

## Summary
clawdcursor is an MCP desktop-control tool that lets an AI model operate local apps through accessibility APIs, OCR, screenshots, and guarded action calls. It targets editor-hosted agents and local automation without telemetry.

## Problem
- AI coding agents often stay inside the editor and cannot act on native desktop apps, browser windows, installers, or OS dialogs.
- Pixel-only control is costly and brittle because it sends screenshots to vision models even when app accessibility metadata can identify buttons, fields, and menus.
- Desktop automation needs one permission and safety path because clicks, typing, files, and destructive actions can affect the user's machine.

## Approach
- The system exposes one MCP entry that can run over stdio from Claude Code, Cursor, Windsurf, or Zed, or as an HTTP MCP daemon at 127.0.0.1:3847/mcp.
- It tries the accessibility tree first, then OCR, then screenshots and vision for canvas-style UIs.
- It offers 6 compact tool groups: computer, accessibility, window, system, browser, and task. A 94-tool granular surface remains available for compatibility and debugging.
- Every tool call passes through safety.evaluate(), and destructive actions require confirmation.
- It supports macOS, Windows, and Linux through native UIA, Windows.Media.Ocr, AT-SPI, Tesseract, X11, Wayland, and macOS Accessibility and Screen Recording permissions.

## Results
- The excerpt reports no benchmark accuracy, latency, cost, or task-completion results.
- The compact MCP catalog has 6 tools and is claimed to be about 12x smaller than the 94-tool granular catalog.
- The compact catalog is claimed to use about 1,500 tokens.
- Batched deterministic actions can collapse N tool calls into 1 guarded call.
- The product claims local-only operation, localhost access, no telemetry, and support for macOS, Windows, Linux, X11, and Wayland.

## Link
- [https://clawdcursor.com](https://clawdcursor.com)
