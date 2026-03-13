---
name: research-site-design-language
description: Preserve the research-facing design language for Recoleta site and published trend pages. Use when changing site visuals, UI copy, badges, cards, section hierarchy, or markdown-to-site rendering so fixed UI chrome stays English while long-form narrative copy can follow the source language.
---

# Research Site Design Language

## Core Rules

- Keep fixed UI chrome in English: section titles, badges, controlled vocabulary, action labels, metadata pills, filters, and navigation.
- Let long-form narrative content follow the source language.
- Do not mix languages within the same semantic layer. If one badge set is English, all peer badges stay English.
- Preserve research-native terms as written: paper titles, method names, benchmark names, dataset names, topic tags, and taxonomy labels.
- Favor dense, scannable structure over marketing-style flourish. Comparative content should read like an analysis surface, not a landing page.

## Comparative Views

- Treat `Evolution` as a first-class comparison surface, not generic prose.
- Surface comparison signal counts early on index cards and detail heroes.
- Render controlled comparison terms in English, including `Continuing`, `Emerging`, `Fading`, `Shifting`, `Polarizing`, and `History`.
- Collapse long rationale behind progressive disclosure, especially for mobile layouts.

## Validation

- Check both desktop and mobile when changing visual hierarchy or density.
- If the change touches renderer output, update tests so terminology and ordering stay specified.
- Use Playwright or a local preview build when the user expects visual review rather than code-only reasoning.
