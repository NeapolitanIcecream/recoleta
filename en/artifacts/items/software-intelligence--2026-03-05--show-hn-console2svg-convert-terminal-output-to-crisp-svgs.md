---
source: hn
url: https://github.com/arika0093/console2svg
published_at: '2026-03-05T23:48:22'
authors:
- arika0093
topics:
- terminal-rendering
- svg-generation
- developer-tooling
- ci-automation
- command-line-interface
relevance_score: 0.52
run_id: materialize-outputs
language_code: en
---

# Show HN: Console2svg – Convert terminal output to crisp SVGs

## Summary
console2svg is a command-line tool that converts terminal output into crisp, scalable SVGs, primarily addressing the problems of blurry terminal screenshots and the difficulty of automatically generating documentation assets. It also supports animated SVGs, cropping, replay, and CI integration, targeting developer documentation and demo use cases.

## Problem
- Terminal content is usually saved as raster images such as PNG, and text becomes blurry when zoomed in, making it unsuitable for high-quality documentation, blogs, and social media presentation.
- Existing solutions often depend on extra software, are hard to reproduce reliably in CI, and are not friendly enough for dynamic command execution, precise cropping, and cross-platform support.
- For developers, being able to repeatedly generate terminal demo assets that stay consistent with the code state is important, because outdated or distorted documentation screenshots reduce readability and credibility.

## Approach
- The core method is to directly capture terminal output or the command execution process and render it as vector SVG rather than first taking a pixel-based screenshot; therefore text stays sharp at any zoom level.
- It provides both static mode and video mode (`-v`), allowing command execution animations to be saved as SVG; it also supports `--timeout` and `--sleep` to control the recording display for long-running or non-terminating commands.
- Through `--replay-save` / `--replay`, terminal interactions can be recorded as simple JSON and then replayed to generate SVG, making results more reproducible and making it easier to generate consistent assets in CI.
- It supports cropping output by pixels, characters, or text patterns, and can add window frames, backgrounds, gradients, image backgrounds, prompts, and titles as appearance options, directly producing presentation-ready images.
- The tool emphasizes “no dependencies” and cross-platform distribution, and can be used as an npm package, dotnet tool, static binary, and GitHub Action, while automatically adjusting CI environment variables to preserve colored output.

## Results
- The paper/project description does not provide standard benchmarks, public datasets, or quantitative comparisons with other tools, so there are **no quantitative performance or quality metrics** to report.
- The strongest specific claim given is that the output is **vector SVG**, and the text “remains sharp at any scale,” avoiding the blur of raster screenshots such as PNG.
- Functional results include support for **TrueColor**, **animated SVG**, **text-pattern-based cropping**, **background/window decoration**, **CI-friendly replay**, and cross-platform operation on **Windows/macOS/Linux**.
- Compatibility claims include Windows 10+ (requires ConPTY), Linux, and macOS; it also notes that **v0.6.2 and later** natively support macOS arm64.
- In terms of reproducibility, replay files contain execution durations such as `totalDuration: 10.9530099` and per-keystroke event timestamps, indicating that they preserve not only the final output but also the interactive process, though this is still a feature demonstration rather than a comparative experimental result.

## Link
- [https://github.com/arika0093/console2svg](https://github.com/arika0093/console2svg)
