# Recoleta First Output Tour

Use this guide after your first `run --once`. It tells you where to look, what
to run next, and which public examples are closest to the local files you
should see.

## 1. Check that the first run worked

If you ran:

```bash
uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

or:

```bash
docker compose run --rm recoleta run --once --analyze-limit 50 --publish-limit 20
```

open these paths first:

- `MARKDOWN_OUTPUT_DIR/latest.md` or `./data/outputs/latest.md`: summary page
  for the latest run
- `MARKDOWN_OUTPUT_DIR/Inbox/`: one Markdown note per published item
- `RECOLETA_DB_PATH`: the SQLite database that later trend, idea, and site
  steps build from

If you started from a preset, use the output paths in that preset YAML file.

## 2. Add trends and the site

Once the first batch of item notes looks right, run:

```bash
uv run recoleta trends --granularity day
uv run recoleta site build
```

That should create:

- `MARKDOWN_OUTPUT_DIR/Trends/`: trend briefs in Markdown
- `MARKDOWN_OUTPUT_DIR/site/index.html`: a browsable static site

If you want idea briefs too, run:

```bash
uv run recoleta ideas --granularity day --date 2026-03-14
```

That writes to `MARKDOWN_OUTPUT_DIR/Ideas/`. Run `recoleta site build` again if
you want those pages included in the site.

## 3. Compare your output with the public examples

### Site home

Local path:

- `MARKDOWN_OUTPUT_DIR/site/index.html`

Public example:

- <https://neapolitanicecream.github.io/recoleta/>

![Recoleta site home](../assets/sample-output-site-home.png)

### Trend brief

Create it with:

```bash
uv run recoleta trends --granularity day
```

Local paths:

- `MARKDOWN_OUTPUT_DIR/Trends/*.md`
- `MARKDOWN_OUTPUT_DIR/site/trends/*.html`

Public examples:

- <https://neapolitanicecream.github.io/recoleta/trends/>
- <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>

![Recoleta trend brief](../assets/sample-output-trend-brief.png)

### Idea brief

Create it with:

```bash
uv run recoleta ideas --granularity day --date 2026-03-14
```

Local paths:

- `MARKDOWN_OUTPUT_DIR/Ideas/*.md`
- `MARKDOWN_OUTPUT_DIR/site/ideas/*.html`

Public examples:

- <https://neapolitanicecream.github.io/recoleta/ideas/>
- <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>

![Recoleta idea brief](../assets/sample-output-idea-brief.png)

## 4. Pick the closest preset example

### Agents radar

- Start from: [`presets/agents-radar.yaml`](../../presets/agents-radar.yaml)
- Closest public example:
  <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>
- Expect: `latest.md`, `Inbox/`, trend briefs, idea briefs, and the static site

### Robotics radar

- Start from: [`presets/robotics-radar.yaml`](../../presets/robotics-radar.yaml)
- Closest public example:
  <https://neapolitanicecream.github.io/recoleta/streams/embodied-ai.html>
- Expect the same output structure, but with robotics-heavy source material

### arXiv digest

- Start from: [`presets/arxiv-digest.yaml`](../../presets/arxiv-digest.yaml)
- Closest public example: <https://neapolitanicecream.github.io/recoleta/trends/>
- Expect the same output structure, but from a paper-only corpus
