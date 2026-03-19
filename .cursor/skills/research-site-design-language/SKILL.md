---
name: research-site-design-language
description: Preserve the research-facing design language for Recoleta site and published trend pages. Use when changing site visuals, UI copy, badges, cards, section hierarchy, or markdown-to-site rendering so fixed UI chrome stays English while long-form narrative copy can follow the source language.
---

# Research Site Design Language

Use this skill when changing site visuals, UI copy, badges, card hierarchy, section ordering, or markdown-to-site rendering for research-facing pages.

## Core Rules

- Keep fixed UI chrome in English: section titles, badges, controlled vocabulary, action labels, metadata pills, filters, and navigation.
- Let long-form narrative content follow the source language.
- Do not mix languages within the same semantic layer. If one badge set is English, all peer badges stay English.
- Public site chrome should keep a direct repo-return CTA so readers can open the source repo or first-run path from the rendered site.
- When a header includes language switching, treat the switcher as a utility control and keep the repo-return CTA visually subordinate rather than styling both as peer primary pills.
- When the header already exposes the repo-return CTA, keep the home hero focused on in-product browsing and onboarding actions rather than repeating a GitHub pill there.
- At medium widths, split dense header chrome into an intentional top utility row and a separate navigation row instead of relying on incidental link wrapping.
- On the way from medium to mobile, let brand and utility controls separate into their own row before collapsing navigation into the full mobile grid.
- First-contact promo assets should lead with the user-visible outcome before qualifiers such as `local-first` or detailed source/input taxonomy.
- First-contact promo cards should show the shape of the produced artifact with nested surfaces or grouped sub-sections, not just a flat stack of left-aligned copy and pills.
- Preserve research-native terms as written: paper titles, method names, benchmark names, dataset names, topic tags, and taxonomy labels.
- Favor dense, scannable structure over marketing-style flourish. Comparative content should read like an analysis surface, not a landing page.
- Treat `Trends` and `Ideas` as peer collection surfaces: each should have its own index destination, parallel navigation affordance, and symmetric home-section labeling.
- When `Trends` and `Ideas` appear side by side, keep the pair visually symmetric: equal-width columns, one stacked card column per side, and mirrored section chrome.
- Use `Overview` as the canonical page summary for index cards and detail hero dek copy. Keep `Evolution` as a secondary comparison surface rather than replacing the primary summary.
- On `Ideas` detail pages, keep `Summary` and `Opportunities` as separate surfaces; render each opportunity as its own readable card with English field labels instead of collapsing multiple ideas into one long prose block.
- On `Ideas` cards and detail heroes, omit empty topic rows entirely instead of rendering placeholder chrome for missing topics.
- On `Ideas` opportunity cards, keep only short metadata in pills; render the longer user/role audience as a separate `Role` field block instead of a wrapping pill.
- On `Ideas` opportunity cards, `Role` field copy must fully expand; do not clamp or truncate multi-line role/audience text.
- Topic and stream discovery surfaces should aggregate both trend briefs and idea briefs so idea-only topics/streams stay navigable and linked, rather than degrading into unlabeled plain text.
- Topic and stream entity pages should lead with a summary surface for the entity itself, then render symmetric `Trend briefs` and `Idea briefs` collection panels below instead of pairing the entity name against only one collection.
- If a stream label originates from a machine slug such as `embedded_ai` or `research-ops`, render it as a readable title in the UI chrome rather than exposing the raw slug.

## Comparative Views

- Treat `Evolution` as a first-class comparison surface, not generic prose.
- Surface comparison signal counts early on index cards and detail heroes.
- Render controlled comparison terms in English, including `Continuing`, `Emerging`, `Fading`, `Shifting`, `Polarizing`, and `History`.
- Collapse long rationale behind progressive disclosure, especially for mobile layouts.
- Keep PDF and HTML on the same card hierarchy and terminology, but expand rationale inline in PDF instead of carrying over interactive disclosure patterns.

## Maintenance

- Treat this skill as the canonical record of project-level design language for research-facing site surfaces.
- If a change introduces a new fixed UI term, badge family, layout convention, or localization rule that should persist, update this skill in the same change.
- If user feedback or product direction invalidates an existing rule, revise or remove the stale rule here before treating the new pattern as canonical.
- Keep the skill concise: record stable project-wide rules, not one-off exceptions or temporary experiments.

## Validation

- Check both desktop and mobile when changing visual hierarchy or density.
- If the change touches renderer output, update tests so terminology and ordering stay specified.
- Use Playwright or a local preview build when the user expects visual review rather than code-only reasoning.
