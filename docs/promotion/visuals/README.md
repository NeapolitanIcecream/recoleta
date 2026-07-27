# Visual review candidates

Status: maintainer review required

Generated: 2026-07-25; structure study added 2026-07-27

Published or referenced by product surfaces: no

These files are local review artifacts. Do not replace the README banner,
social preview, screenshots, or site assets until the maintainer selects or
rejects a direction.

## Candidate A — light evidence field

File: `banner-candidate-a-light.png`

Direction:

- warm archival paper and editorial scientific illustration;
- three source fields stay visibly separate before becoming evidence-linked
  briefs and an open publication;
- navy, cobalt, teal, and one small coral registration accent;
- no product text, logo, device UI, or AI iconography.

## Candidate B — dark cyanotype atlas

File: `banner-candidate-b-dark.png`

Direction:

- midnight archive table with cyanotype and letterpress texture;
- three linked research ribbons remain inspectable as they enter an open atlas;
- more distinctive and atmospheric, with stronger contrast at thumbnail size;
- no product text, logo, device UI, or AI iconography.

Review note:

- the maintainer preferred this complete candidate to Candidate A;
- the description “dark blue” only identified the file and is not a final
  palette requirement;
- the artistic complexity and bespoke texture should not be assumed approved.

## Candidate C — neutral structure study

Files:

- `banner-candidate-c-structure.svg`
- `banner-candidate-c-structure.png`

Direction:

- preserve Candidate B's three equal input paths and one dominant publication;
- remove maps, paper texture, collage fragments, and ornamental detail;
- use a 12-column grid, 8-pixel rhythm, flat vector geometry, and role-based
  colour classes;
- keep the light canvas explicitly non-final so structure can be evaluated
  independently from palette.

Validation:

- rendered in a Chromium browser at 2400 × 1200;
- remained legible at 240 × 120;
- remained structurally legible in grayscale;
- includes SVG title and description metadata;
- SVG SHA-256:
  `8232a85e2a2a95b95daffda22e35cd0c1fd0f4e8fa9d6ce7036d3c76911bfefd`;
- browser-rendered PNG SHA-256:
  `e6efa08df4f77562ff970345f84dc616639637460dc59ac13a043c073132714a`;
- is not referenced by any public product surface.

See [`../visual-system-review.md`](../visual-system-review.md) for the sourced
constraints and the exact question this candidate tests.

## Generation records

Candidates A and B used the built-in image generation tool. The prompts
specified a wide 2:1 repository banner, three traceable research streams, an
editorial archive or atlas metaphor, and explicit avoidance of AI chips, robots,
brains, literal radar screens, magnifying glasses, paper airplanes, magic
particles, cyberpunk styling, and generic dashboard imagery.

Candidate C was authored as deterministic SVG. A generated raster was rejected
for this test because the design-system evidence called for repeatable geometry,
replaceable theme values, and exact small-size behavior.

After the structure test is resolved, the next review round should:

1. make one targeted structural revision if requested;
2. explore role-based theme values without treating the current light or dark
   candidates as a fixed palette;
3. create a deterministic social card with exact typography and current fleet
   facts over or beside the approved artwork;
4. select from the fresh live-fleet captures recorded below;
5. present the complete replacement set before changing any public reference.

## Live fleet capture set

Captured: 2026-07-25

Source: <https://neapolitanicecream.github.io/recoleta/>

Publication status: local review only

The raw PNGs are intentionally kept in the ignored `output/playwright/`
directory until the maintainer approves a replacement set. This avoids
accidentally shipping screenshots merely because they were captured. Promote
only the selected files into versioned assets after review.

| Local capture | Viewport | SHA-256 |
| --- | --- | --- |
| `output/playwright/fleet-home-desktop-2026-07-25.png` | 1440 × 960 | `a2bc436c3c70cc0aad253906614ff4d12ac1dd917437d9a6f9c17e840c711c50` |
| `output/playwright/fleet-home-zh-desktop-2026-07-25.png` | 1440 × 960 | `a97fdc8c501c79d8b63672f517e5d1cd6db408dccb82c091a54aa83a7923b474` |
| `output/playwright/fleet-trend-desktop-2026-07-25.png` | 1440 × 960 | `844318dc13cd4db90716a2b7f792c70b277d64fbad05cc9072c58d7a65c1efd8` |
| `output/playwright/fleet-trend-source-card-2026-07-25.png` | 680 × 711 | `de313f56987e3e2e60a73cb46a9505bc85daa6bff76c01930a6cdd81ed6317da` |
| `output/playwright/fleet-home-mobile-2026-07-25.png` | 390 × 844 | `64430ea2666d7541380ace86369556a9bd733c3ca7e24e6935781821690a10c6` |

The selected Trend is the public Software Intelligence brief dated 2026-07-23.
The source-card capture shows the finding text and the two linked papers in one
frame, making the traceability mechanism visible without a mock interface.
