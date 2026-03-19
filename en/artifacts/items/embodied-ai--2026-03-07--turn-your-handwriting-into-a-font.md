---
source: hn
url: https://arcade.pirillo.com/fontcrafter.html
published_at: '2026-03-07T23:59:17'
authors:
- andonumb
topics:
- font-generation
- handwriting-vectorization
- opentype
- client-side-processing
- privacy-preserving
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Turn Your Handwriting into a Font

## Summary
FontCrafter is a purely browser-based tool that automatically converts scanned handwriting into installable fonts, emphasizing local privacy, zero signup, and multi-format export. Its core value is automating the complex process of glyph extraction, vectorization, and OpenType construction, allowing ordinary users to quickly generate usable personal fonts.

## Problem
- It solves the problem of **how to turn personal handwriting into a real installable font with a low barrier to entry**, which is important for design, education, content creation, and brand personalization.
- Traditional comparable tools often depend on **cloud processing, account registration, and paid feature gates**, creating privacy, cost, and usability friction.
- Simply cutting characters out of an image is not enough; a truly usable font also requires full font-engineering support such as **glyph outlines, spacing, ligatures, substitution rules, and standard font tables**.

## Approach
- After inputting a scanned handwriting image, the system runs a multi-stage image-processing pipeline locally in the browser: **adaptive threshold segmentation → connected-component detection → Suzuki-Abe contour tracing → RDP simplification → Chaikin smoothing → cubic Bézier fitting**, turning ink into clean vector glyphs.
- It **builds an OpenType font from scratch** rather than swapping images into a template; metrics such as cap height, ascender, descender, and x-height are estimated directly from the user's handwriting samples.
- To make the font feel more like real handwriting, the system adds **contextual substitutions (calt)** in GSUB, storing up to **3** handwriting variants per character and rotating them during continuous text input.
- It can also automatically generate **ligatures (such as ff, fi, th, st)**, class-based kerning, accented/extended characters, and supports local export to **OTF, TTF, WOFF2, Base64**.
- It additionally supports **COLR/CPAL color font** effects such as shadows, ink textures, and two-color layering, all generated client-side in JavaScript without servers or WebAssembly.

## Results
- The text **does not provide standard benchmarks or experimental data**, so there is no verifiable accuracy, speed, or quantitative comparison against academic baselines.
- Specific functional outcomes include generating a standard font with **more than 500 glyphs**, of which **100+** accented characters can be automatically composed from base letters.
- Up to **3** handwriting variants can be retained for each character and automatically rotated through **calt** rules to reduce the mechanical feel of repeated letters.
- It supports automatic ligatures, with examples including **ff, fi, fl, th, st**; it supports **4** output formats: OTF/TTF/WOFF2/Base64.
- The article claims that WOFF2 is **typically 30–50% smaller** than the original OTF, making it suitable for web embedding, but does not provide measured file statistics for this tool.
- Compared with Calligraphr, the author claims the differentiators are: **zero signup, 100% local processing, and free inclusion of ligatures/contextual substitutions/color font effects**, but provides no formal comparative experiments or user-study data.

## Link
- [https://arcade.pirillo.com/fontcrafter.html](https://arcade.pirillo.com/fontcrafter.html)
