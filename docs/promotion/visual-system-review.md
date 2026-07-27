# Promotion visual system review

Status: structure approved; themed replacement set awaiting review

Reviewed: 2026-07-27

This note translates three established design systems into constraints for
Recoleta's repository banner, social preview, diagrams, and fleet screenshots.
It does not adopt their brand styling.

## What the references establish

### GOV.UK Design System

The useful lesson is content discipline. GOV.UK advises against images used for
unnecessary decoration, asks that an image serve a real user need, recommends
keeping essential meaning available outside the image, and treats contrast and
alternative text as part of the design rather than later remediation.

Implication for Recoleta:

- a banner should explain the product model or show real output;
- visual texture alone is not enough to justify an element;
- generated raster text should not carry the product claim;
- the surrounding page must retain the same meaning without the image.

Sources:

- <https://design-system.service.gov.uk/styles/images/>
- <https://design-system.service.gov.uk/styles/colour/>
- <https://design-system.service.gov.uk/styles/layout/>

### Carbon Design System

The useful lesson is a reproducible visual grammar. Carbon uses an 8-pixel mini
unit, visible alignment lines, constrained spacing and aspect ratios, and
role-based tokens whose values can change between themes without changing their
meaning.

Implication for Recoleta:

- build promotional layouts on an 8-pixel rhythm and explicit key lines;
- name colour roles such as canvas, surface, ink, signal, and evidence instead
  of making a particular hex value part of the concept;
- keep the same structure usable in light, dark, or future themes;
- use contrast as a deliberate focal moment, not as decoration everywhere.

Sources:

- <https://preview.carbondesignsystem.com/building-blocks/foundations/2x-grid/overview>
- <https://preview.carbondesignsystem.com/building-blocks/foundations/color/overview>
- <https://preview.carbondesignsystem.com/building-blocks/foundations/themes/overview>

### Primer

The useful lesson is consistent grouping with explicit hierarchy. Primer Brand
UI uses a 12-column grid, recommends equal spans for repeated peer elements, and
uses unequal spans when hierarchy is intentional. Its image guidance asks for
consistent dimensions, descriptive context, alternative text, and optimized
files.

Implication for Recoleta:

- render the three fleet streams as peers with the same visual weight;
- give the resulting publication more space because it is the intended focal
  point;
- use one stable aspect ratio for repository and social variants;
- optimize the approved SVG and PNG rather than shipping an oversized art
  source.

Sources:

- <https://primer.style/brand/layout/Grid/>
- <https://primer.style/brand/components/Image/>
- <https://primer.style/accessibility/>

## Limits of this guidance

These references govern services, product interfaces, and brand components.
They do not determine whether Recoleta should use a light or dark background,
nor do they prescribe a unique illustration style. Their role here is to make a
chosen direction legible, accessible, repeatable, and inexpensive to maintain.

## Reading the first two candidates

Candidate B has a stronger information topology than Candidate A:

- three independent source paths remain visible;
- the paths travel directly toward one dominant publication;
- the intended reading order survives at thumbnail size.

Candidate B also has costs that should not become the default system:

- cyanotype, torn paper, maps, and unique miniatures compete with the topology;
- the large number of bespoke details is difficult to reproduce consistently;
- the texture leaves less reliable space for exact release copy and responsive
  crops.

The maintainer's reference to Candidate B as “the dark-blue one” only
disambiguated which file was selected. It is not evidence for a dark palette.

## Proposed Recoleta rules

1. Show one product claim: independent research streams become a traceable,
   readable publication.
2. Preserve three equal input lanes and one clearly dominant output.
3. Use a 12-column layout, 8-pixel spacing rhythm, and a fixed 2:1 master
   aspect ratio.
4. Limit visible roles to canvas, surface, primary ink, secondary ink, rules,
   operational signal, and evidence anchor.
5. Keep palette values replaceable. Structure must remain legible in grayscale.
6. Use flat vector geometry for the core asset. Avoid filters, gradients,
   simulated paper, collage fragments, and ornamental micro-illustrations.
7. Add exact product text deterministically in SVG, HTML, or a layout tool only
   after the structure is approved.
8. Treat real fleet screenshots as product evidence, not as texture inside an
   illustration.
9. Verify the master at full size, at 240 by 120 pixels, and in grayscale.
10. Publish nothing until the maintainer reviews the complete replacement set.

## Current structure test

`visuals/banner-candidate-c-structure.svg` is a deliberately neutral structure
study rather than a palette proposal. It retains Candidate B's three-lane
topology while removing the artistic collage layer. A browser-rendered PNG and
thumbnail checks exist only in the maintainer workspace.

The test is:

- if the structure still works, preserve it and explore theme values later;
- if it no longer works, identify whether the missing quality is tactility,
  contrast, irregular rhythm, or another specific property before revising it.

The draft is not referenced by the README, site, package metadata, or social
metadata.

## Approved direction and second review

The maintainer approved the structure direction on 2026-07-27. The second
review set applies the existing fleet-site roles rather than treating either
earlier candidate as a palette request:

| Role | Current value |
| --- | --- |
| Reading canvas | `#ffffff` |
| Independent surface | `#f5f6f8` |
| Primary ink | `#172033` |
| Body text | `#354052` |
| Muted text | `#5f6875` |
| Quiet rule | `#e2e5ea` |
| Strong rule | `#c8ced6` |
| Operational signal | `#145da0` |
| Signal emphasis | `#0e477d` |

The set contains:

- a 2400 by 1200 repository banner without embedded marketing text;
- a 1200 by 630 social card with the exact claim “Research radars that publish
  traceable trends and ideas” plus a direct invitation to inspect Software
  Intelligence and Embodied AI and try the demo without an API key;
- a 1440 by 960 proof board built from the live fleet home, one real Trend, and
  its linked source trail.

The maintainer approved all three after the social-card and proof-board copy was
simplified. Stable copies are staged for a separate versioned change; later
visual revisions return to review.
