---
source: hn
url: https://github.com/arika0093/console2svg
published_at: '2026-03-05T23:48:22'
authors:
- arika0093
topics:
- terminal-svg
- developer-tools
- cli-visualization
- ci-automation
- documentation
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: Console2svg – Convert terminal output to crisp SVGs

## Summary
console2svg is a command-line tool that directly converts terminal output into crisp, scalable SVGs, primarily addressing blurry screenshots and the hassle of maintaining documentation. It also supports animation, cropping, replay, and CI integration, targeting developer documentation and demo scenarios.

## Problem
- Traditional terminal screenshots are usually saved as raster images such as PNG, and the text becomes blurry when zoomed in, which is not ideal for high-quality documentation, blogs, and presentations.
- Terminal content often needs to show dynamic execution, partial cropping, or a consistent appearance, and existing solutions are not convenient enough for these workflows.
- When automatically generating terminal images in CI, colors, environment variables, and reproducibility can easily cause problems, leading to inconsistencies between code and documentation screenshots.

## Approach
- The core method is simple: run a command or read terminal output from a pipe, capture text with colors/control sequences, and render it into vector SVG rather than a bitmap screenshot.
- It provides both static mode and video mode; video mode saves the command execution process as animated SVG, suitable for showing interactions or command execution.
- It provides a replay mechanism: first record keyboard input and timestamps to JSON, then regenerate SVG from that record, improving reproducibility and making it easier to rebuild demos in CI.
- It provides various post-processing capabilities, including cropping by pixel/character/text pattern, window frames and background styles, and custom colors/prompts/titles, making the output more suitable for publishing.
- For CI scenarios, it automatically sets `TERM=xterm-256color`, `COLORTERM=truecolor`, and `FORCE_COLOR=3`, and removes CI/TF_BUILD variables that might cause libraries to disable color, in order to preserve colored terminal output as much as possible.

## Results
- The text does not provide standard academic benchmarks or experimental data, so there are **no quantitative performance results, accuracy metrics, or systematic numerical comparisons with baselines**.
- Specific capability claims include support for **truecolor**, **animated SVG**, **text-pattern cropping**, **background/window decoration**, **replay JSON**, and **automatic CI generation**.
- Platform coverage claims: supports **Windows 10+ (ConPTY)**, **Linux**, **macOS**, and **v0.6.2+** has native support for macOS arm64.
- Some default/configurable parameters include explicit values: default width is **100 characters** (pty mode), height is **auto-fitted** in pty mode; if the total duration deviation in a replay file exceeds **1 second**, a timeout error is reported.
- The examples show animation recording and truncation capabilities, such as `--timeout 5` and `--sleep 0.5` for exporting animated SVGs of long-running commands, but they do not provide numerical improvements in speed, size, or quality compared with other tools.
- The main "breakthroughs" are better understood as a product feature combination: **zero-dependency distribution** (npm, dotnet tool, static binary), **animated SVG output**, **text-anchor-based cropping**, **replayable interaction recording**, and direct adaptation for documentation/blogs/social media.

## Link
- [https://github.com/arika0093/console2svg](https://github.com/arika0093/console2svg)
