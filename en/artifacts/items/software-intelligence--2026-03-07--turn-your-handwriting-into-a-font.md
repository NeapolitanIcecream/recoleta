---
source: hn
url: https://arcade.pirillo.com/fontcrafter.html
published_at: '2026-03-07T23:59:17'
authors:
- andonumb
topics:
- font-generation
- handwriting-recognition
- browser-based-tool
- opentype
- privacy-preserving
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# Turn Your Handwriting into a Font

## Summary
FontCrafter is a pure browser-based tool that directly converts handwritten scans into installable fonts, with a focus on **local privacy-preserving processing** and **full OpenType font generation**. It not only extracts glyphs, but also automatically adds ligatures, contextual alternates, kerning adjustments, and multi-format export.

## Problem
- Existing handwriting-to-font tools often rely on **cloud uploads, account registration, or paid subscriptions**, making them unfriendly to privacy, usability, and cost.
- Simply swapping images into a template is not enough; a truly usable font also requires complete font engineering such as **vector outlines, glyph metrics, kerning, ligatures, extended characters, and export formats**.
- This matters because users want to use their own handwriting for design, teaching, content creation, and commercial purposes, while not wanting to expose their original handwriting data.

## Approach
- After the user uploads a handwritten scan, the system runs a multi-stage image-processing pipeline locally in the browser: **adaptive thresholding → connected-component detection → Suzuki-Abe contour tracing → RDP simplification → Chaikin smoothing → cubic Bézier fitting**, turning each character into a clean vector path.
- Rather than replacing glyphs in a template, it **constructs OpenType font tables from scratch**: using CFF outlines, 1000 UPM, and estimating real metrics such as ascender, descender, cap height, and x-height from the scan results.
- To make the font feel more like natural handwriting, it keeps up to **3 variants** for each character and rotates them during input via **GSUB contextual alternates (`calt`)**, preventing repeated letters from looking exactly the same.
- It also automatically generates **ligatures (`liga`)**, kerning-like adjustments, 100+ accented/extended characters, and optional **COLR/CPAL color font effects**; finally exporting **OTF, TTF, WOFF2, Base64** locally.

## Results
- The article **does not provide formal experiments, benchmark data, or academic evaluation metrics**, so there are no verifiable accuracy, speed, or quality scores.
- Specific capability claim: a standard font can generate **500+ glyphs**, including **100+** automatically composed accented and extended characters.
- Variant mechanism claim: each character can retain up to **3 handwritten versions**, automatically rotated through `calt` to reduce the mechanical feel of repeated characters.
- Format capability claim: it supports export in **4 formats** (**OTF / TTF / WOFF2 / Base64**), all **generated locally**; WOFF2 is described as typically **30–50% smaller** than the original OTF.
- Feature comparison claim: compared with Calligraphr, the author claims FontCrafter **requires no account, is completely free, and processes everything locally**, while also providing ligatures, contextual alternates, color font effects, and **WOFF2/Base64** export for free.
- Boundary-condition claim: it currently **does not support** variable fonts, hinting, RTL scripts, CJK character sets, or multi-page template scans.

## Link
- [https://arcade.pirillo.com/fontcrafter.html](https://arcade.pirillo.com/fontcrafter.html)
