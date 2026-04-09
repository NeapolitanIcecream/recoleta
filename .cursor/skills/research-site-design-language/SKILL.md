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
- Reader-facing research surfaces must present finished writing, not the model's internal worksheet. Analysis structure may guide generation, but the public page should show only the final prose and supporting evidence.
- Keep reader-facing block shapes sparse. Prefer a small repeated primitive such as `title`, `content`, and `evidence` over field-by-field cards that expose internal methodology labels.
- Do not expose prompt-method labels such as `Best bet`, `Alternate`, `Thesis`, `Anti-thesis`, `Why now`, `What changed`, `Validation next step`, `Top shifts`, or `Counter-signal` as public section chrome unless product direction explicitly reinstates them.
- Treat `Trends` and `Ideas` as peer collection surfaces: each should have its own index destination, parallel navigation affordance, and symmetric home-section labeling.
- When `Trends` and `Ideas` appear side by side, keep the pair visually symmetric: equal-width columns, one stacked card column per side, and mirrored section chrome.
- Use `Trends` and `Ideas` as the canonical peer collection labels on shared discovery surfaces. Do not keep legacy `Trend briefs` / `Idea briefs` chrome once the simplified reader-facing contract is in place.
- Use `Overview` as the canonical page summary for index cards and detail hero dek copy. Historical comparison can sharpen that writing, but it should not reappear as a dedicated public `Evolution` surface.
- On trend detail pages, keep the public reading surface centered on `Overview` plus supporting cluster blocks. If contradictory evidence matters, fold it into the finished prose of those remaining blocks instead of rendering a separate worksheet surface.
- On `Ideas` detail pages, keep the page structure minimal: a summary block plus idea blocks. Each idea block should read like a short finished note with a title, prose body, and evidence, not a stack of explicit method fields.
- On `Ideas` cards and detail pages, avoid legacy collection framing such as `Idea brief` or `Opportunities`. Use neutral chrome like `Ideas`, plain count strings, and supporting `Evidence`.
- For markdown-first `Ideas` detail flows, do not replace raw enum leakage with a different public worksheet. Hiding `User/job` while exposing `Role`, or hiding ranking enums while exposing `Best bet`, is still formalism if the reader sees the internal analysis template.
- On `Ideas` cards and detail heroes, omit empty topic rows entirely instead of rendering placeholder chrome for missing topics.
- On `Ideas` cards and detail heroes, keep metadata subordinate. If a metadata field is not directly useful to a reader deciding whether to open or trust the note, prefer removing it rather than inventing new pills or field blocks for it.
- Topic and stream discovery surfaces should aggregate both trends and ideas so idea-only topics/streams stay navigable and linked, rather than degrading into unlabeled plain text.
- Topic and stream entity pages should lead with a summary surface for the entity itself, then render symmetric `Trends` and `Ideas` collection panels below instead of pairing the entity name against only one collection.
- If a stream label originates from a machine slug such as `embedded_ai` or `research-ops`, render it as a readable title in the UI chrome rather than exposing the raw slug.

## Comparative Views

- Use historical comparison as internal analysis input or as supporting detail inside finished overview/cluster prose, not as a standalone reader-facing worksheet.
- If historical deltas matter on cards or detail heroes, summarize them as direct narrative signal rather than emitting a separate comparison taxonomy block.
- Keep PDF and HTML on the same simplified card hierarchy and terminology.

## Maintenance

- Treat this skill as the canonical record of project-level design language for research-facing site surfaces.
- If a change introduces a new fixed UI term, badge family, layout convention, or localization rule that should persist, update this skill in the same change.
- If user feedback or product direction invalidates an existing rule, revise or remove the stale rule here before treating the new pattern as canonical.
- Keep the skill concise: record stable project-wide rules, not one-off exceptions or temporary experiments.

## Validation

- Check both desktop and mobile when changing visual hierarchy or density.
- If the change touches renderer output, update tests so terminology and ordering stay specified.
- Use Playwright or a local preview build when the user expects visual review rather than code-only reasoning.
