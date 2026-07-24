---
name: research-site-design-language
description: Guide Recoleta's reader-facing site, email, PDF, and published research surfaces toward clear editorial hierarchy, restrained visual design, and series-level prose quality without freezing a particular card, color, or hero treatment.
---

# Research Site Design Language

Use this skill when changing site or email visuals, UI copy, badges, cards,
section hierarchy, markdown-to-site rendering, or reader-facing generation rules.

## Product Posture

- Treat Recoleta as a research publication and reading tool. Evidence, findings,
  and navigation take priority over product marketing.
- Give each page one primary job. Do not make a research detail page double as a
  landing page or make an email reproduce the whole website.
- The current palette, card system, serif headings, gradients, and hero layouts
  are implementation choices, not permanent design rules.
- Share content models and terminology across web, email, and PDF, but design the
  layout separately for each reading medium.
- Prefer editorial selection over visual symmetry. Trends and Ideas remain peer
  destinations, but they do not need equal card counts, mirrored columns, or
  equal-height surfaces on every page.

## Editorial Hierarchy

- Show a summary once per reading surface. A card excerpt may derive from the
  Overview or Summary, but a detail page or full email must not repeat the same
  passage in both its hero and body.
- Present finished writing, not the model's worksheet. Hiding rubric labels is
  insufficient when every item still follows the same paragraph count, field
  order, opening, or closing formula.
- Let weak evidence produce a shorter artifact. Never add a third card, a fixed
  closing paragraph, a pilot threshold, or a counterpoint only to complete a
  template.
- Titles should name the observed mechanism, result, object, or decision. Review
  titles as a series and avoid recurring editorial frames such as `strongest signal`,
  `now needs`, `is becoming`, `being judged`, or `earns trust`.
- Distinguish Sources from Evidence. A linked paper is a source; call it evidence
  only when the page states the result, limitation, or relationship that supports
  the claim. Omit generic `Reports`, `Shows`, or `Describes` annotations. If no
  source can be rendered, omit the source heading as well as placeholders such as
  `(none)`.
- Keep metadata only when it helps a reader choose, understand, or trust the
  content. Do not expose pipeline status, internal enums, exclusive date bounds,
  repeated counts, or duplicate topic lists.
- Empty states describe the reader-visible fact, such as `No trends for this
  period`. They must not expose filtering, retention, publishing, or suppression
  workflow language.

## Visual Language

- Use a white reading canvas, neutral light-gray independent surfaces, quiet
  rules, and deep blue as the recurring accent. Do not mix warm beige surfaces
  with cool blue-gray text and controls. Add a decorative surface only when it
  clarifies hierarchy.
- Assign site colors through role-based tokens for canvas, surface, text, rules,
  controls, focus, and interaction states. A quiet divider color must not double
  as the only boundary for a control or focus state.
- Do not combine gradient backgrounds, glass blur, large soft shadows, oversized
  rounded corners, pill clouds, and card-within-card nesting as a default theme.
  That combination resembles a generic generated SaaS page.
- Use a card only for an independent object or interaction boundary. Use spacing,
  headings, and rules for consecutive parts of one article.
- Use rules only between adjacent peer content. Do not leave a terminal rule after
  the last article section, stack nested and outer rules at one boundary, or
  bracket an ordinary section heading with rules above and below.
- Use pills for compact interactive filters or a small number of categorical
  tags. Render dates, counts, language, and provenance as plain text when they do
  not behave like controls.
- Keep narrative reading order explicit. Long-form Trend and Idea detail content
  should normally use one main column; do not use masonry or balanced CSS columns
  when they make visual order differ from document order.
- Keep body text at least 16px in normal web and email reading contexts, with a
  line height near 1.5 to 1.7. Aim for roughly 45 to 75 Latin characters per line
  and no more than about 40 CJK glyphs for sustained prose.
- Give CJK display type its own metrics. Do not reuse tight negative tracking or
  sub-1.0 line heights from Latin display headings.
- Size compact text controls with a real text line box, not only a tall outer hit
  area. Autonyms and translated labels must leave room for Latin descenders and
  the full metrics of their own scripts without clipping at default or zoomed
  text sizes.
- Use small uppercase labels sparingly. Do not make 10px or 11px all-caps labels
  carry information that a plain heading or metadata line could express.
- Keep all small reader-facing text at a contrast ratio of at least 4.5:1 against
  its rendered background.
- Links inside prose and source lists must remain recognizable without relying
  only on subtle color differences.

## Site Surface Contracts

- Home should help readers find the latest useful work. Prefer a compact latest
  feed or editorially selected feature plus list over mirrored card walls,
  product statistics, and duplicated archive previews.
- Give the home introduction and latest-item section one direct heading each.
  Do not stack synonymous kicker and title pairs, or describe an item as selected
  or curated when the renderer only chooses the newest item by time.
- Keep a direct repository or first-run path available, but do not interrupt every
  detail page with a promotional card when the header or footer already provides
  that route.
- Collection pages may use restrained cards or rows. A linked title is usually
  enough; avoid a repeated `Open brief` button on every entry.
- Detail pages should lead with title, a compact date or stream line, and one
  summary. Render findings as article sections and sources as compact lists.
- On source-note pages, give authorship its own row and group short provenance,
  publication date, and collection facts with semantic labels. Do not concatenate
  long names and unrelated facts into one separator sentence or expose an
  unexplained internal ranking score. Keep the title-area topic set small enough
  to scan as one supporting group.
- Keep the mobile header within two compact rows. Give detail-page titles a
  restrained responsive scale of their own instead of inheriting a landing-page
  display size; long research titles, metadata, and utilities should not consume
  most of the initial viewport. At 390px and 1024px widths, the first
  non-repeated body paragraph should normally begin within the initial viewport
  on a representative detail page.
- Trends and Ideas remain peer navigation destinations. Topic and stream pages
  aggregate both so idea-only entities remain discoverable.
- Convert machine slugs such as `embedded_ai` or `research-ops` to readable UI
  labels. Do not apply slug humanization to research-native hyphenated names such
  as `R-CNN`, `GPT-4o`, or `CLIP-based`.
- Bound growing collections with static pagination. Preserve canonical first-page
  URLs, newest-first order, relative links, and clear Previous/Next controls.
- Render mathematical notation as semantic, selectable content on the web. When
  the home page's latest-item excerpt contains math, render the expression there
  as well and treat it as an atomic unit during truncation; discard unrelated
  rich markup instead of copying the source fragment. Keep the source
  representation available for fallback, show malformed expressions rather than
  dropping them, and let long display equations scroll inside their own reading
  block instead of widening or clipping the page.

## Email Surface Contract

- Email is an edited research dispatch, not a miniature site or dashboard.
- Keep the email's canvas, text, rule, and accent roles aligned with the current
  site palette. Adapt layout and density to the medium without reviving a separate
  warm or cool color system for email.
- Use a content-bearing subject and a complementary preheader. Do not repeat the
  sender name, date, summary, or topics in several blocks.
- Select the strongest two or three findings for the message, with the smallest
  useful source set. Deduplicate sources across the message before applying the
  per-finding limit; URL paths and queries remain case-sensitive. Link to the site
  for the complete artifact.
- Use one primary CTA. Keep secondary navigation as ordinary descriptive links.
  The message must remain coherent if rounded corners, background colors, and
  decorative containers disappear.
- Email chrome follows the message language. A Chinese message should not be
  forced to expose `Window`, `Overview`, `Cluster`, and `Evidence` merely because
  the website currently uses English chrome.
- Keep the layout single-column and email-safe. Set `lang` and `dir`, preserve a
  logical heading order, mark layout tables as presentational, use explicit
  Outlook-safe line heights and spacing, and keep the primary touch target at
  least 44px high.
- Put vertical spacing on content-bearing table cells. Do not place a standalone
  full-width empty table below a decorative rule, where Outlook can repaint the
  spacer as a visible band.
- Use an Outlook-safe VML fallback when a button is necessary, without making a
  large rounded branded button part of the visual identity.
- Treat the Outlook/Word button branch as a separate renderer. Let the VML shape
  height and vertical anchor center its label; do not copy the browser anchor's
  full-height exact line box into the VML text container, where Word can clip it.
- Treat plain text as a first-class edited output with readable link placement and
  punctuation, not as HTML stripped into a debug transcript.
- Do not rely on JavaScript, MathML, SVG, data URLs, or web-font substitution for
  email equations. Preserve readable TeX in HTML and plain text as the baseline.
  Use generated equation images only when their delivery and retention are part
  of the publishing contract; include equivalent alt text and keep the message
  useful when remote images are blocked. Never enable arbitrary source images or
  math markup merely to admit renderer-generated output.

## Language

- Use one UI language within each page and peer control set. Fixed chrome follows
  the selected site or message locale; English is only a fallback when a localized
  label is unavailable, not a permanent design requirement.
- On a two-language site, show one independent link to the alternate language,
  named in that language and script. Do not expose raw locale codes or style the
  current and alternate languages as pseudo-tabs. For three or more languages,
  use a compact menu whose options form a semantic list and whose current option
  is identified without relying only on color. Use `lang` and `hreflang`, avoid
  flags, and keep language controls at least 44px high. Resolve language names
  from CLDR autonyms rather than a short hard-coded locale table, using the
  concise product label `中文` for `zh-CN`; fail the site build with an
  actionable error when no native display name is available.
- Localize only explicit chrome and metadata nodes. Never run UI phrase or count
  replacement across article prose, excerpts, source reasons, or research titles.
- Let long-form prose follow the selected output language. Translation may reflow
  sentences and paragraphs to read naturally while preserving facts, numbers,
  uncertainty, names, and links.
- Preserve research-native names as written: paper titles, method names,
  benchmarks, datasets, product names, and acronyms unless a stable translation
  exists.

## Anti-Slop Review

- Review output as a rolling series, not only one artifact at a time. Compare
  recent titles, first sentences, paragraph counts, section order, and closing
  sentences for repeated skeletons.
- Check semantic duplication separately from exact strings. An excerpt followed by
  a paraphrased Overview can still repeat the same information.
- Treat arbitrary sample sizes and decision thresholds as unsupported specificity
  unless a source or an explicit editorial policy justifies them.
- Count visible controls, labels, links, cards, and rendered page height during
  visual review. Remove elements that do not help navigation, comprehension, or
  trust.
- Prefer a small positive writing contract plus corpus-level evaluation over a
  growing prompt list of banned phrases.

## Validation

- Inspect representative real artifacts, not only synthetic short fixtures.
- Check short and long English and Chinese samples at 1440px, 1024px, 390px, and
  200% zoom. For email, also check 320px, 375px, and 600px widths.
- Include inline and long display equations, currency using dollar signs, code
  containing math delimiters, and malformed TeX in rendering checks. Confirm
  excerpts and plain text contain each equation once, and inspect the email with
  external images disabled whenever equation images are introduced.
- Use Playwright or equivalent browser rendering for site changes. Validate email
  in Outlook Classic, a modern Outlook client, Gmail, and Apple Mail when the
  change affects production delivery.
- Test stable reader contracts such as unique summary rendering, semantic heading
  order, useful metadata, source identity deduplication, and mobile reflow. Avoid
  tests that freeze ornamental markup or a particular card count.
- Add rolling quality metrics for repeated title frames, opening n-grams,
  boilerplate sentences, summary overlap, and generic source annotations. Use
  English and Chinese golden sets plus periodic blind human review.

## Maintenance

- Treat this skill as the current design decision record, not a museum of every
  layout exception.
- When product direction changes a stable rule, replace the stale rule instead of
  appending a contradictory bullet.
- Keep rules about durable reader outcomes. Leave one-off implementation details in
  plans, tests, or code comments.
