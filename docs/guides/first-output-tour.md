# Recoleta First Output Tour

Use this guide right after the README quickstart or one of the starter presets.
The goal is simple: confirm that your first run worked, then see the three
output surfaces most users care about.

## 1. What success looks like after `run --once`

After:

```bash
uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

or:

```bash
docker compose run --rm recoleta run --once --analyze-limit 50 --publish-limit 20
```

check these local paths first:

- `MARKDOWN_OUTPUT_DIR/latest.md` or `./data/outputs/latest.md`: the run index
- `MARKDOWN_OUTPUT_DIR/Inbox/`: one Markdown note per published item
- `RECOLETA_DB_PATH`: the SQLite truth store for later trends, ideas, and site rebuilds

If you started from a preset, use the preset-specific output directory declared
in the YAML file.

## 2. The next two commands worth running

Once item publishing works, the shortest path to the "full Recoleta" experience
is:

```bash
uv run recoleta trends --granularity day
uv run recoleta site build
```

That gives you:

- `MARKDOWN_OUTPUT_DIR/Trends/`: canonical trend markdown
- `MARKDOWN_OUTPUT_DIR/site/index.html`: a browsable static site

After you have a trend window, add idea briefs with:

```bash
uv run recoleta ideas --granularity day --date 2026-03-14
```

That writes idea briefs under `MARKDOWN_OUTPUT_DIR/Ideas/` and refreshes the
site surface if you run `recoleta site build` again.

## 3. Sample output surfaces

### Public site home

Local output:

- `MARKDOWN_OUTPUT_DIR/site/index.html`

Public reference:

- <https://neapolitanicecream.github.io/recoleta/>

![Recoleta site home](../assets/sample-output-site-home.png)

### Trend brief

Generated after:

```bash
uv run recoleta trends --granularity day
```

Local output:

- `MARKDOWN_OUTPUT_DIR/Trends/*.md`
- `MARKDOWN_OUTPUT_DIR/site/trends/*.html`

Public references:

- <https://neapolitanicecream.github.io/recoleta/trends/>
- <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>

![Recoleta trend brief](../assets/sample-output-trend-brief.png)

### Idea brief

Generated after:

```bash
uv run recoleta ideas --granularity day --date 2026-03-14
```

Local output:

- `MARKDOWN_OUTPUT_DIR/Ideas/*.md`
- `MARKDOWN_OUTPUT_DIR/site/ideas/*.html`

Public references:

- <https://neapolitanicecream.github.io/recoleta/ideas/>
- <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>

![Recoleta idea brief](../assets/sample-output-idea-brief.png)

## 4. Preset-to-sample mapping

### Agents radar

- Start from: [`presets/agents-radar.yaml`](../../presets/agents-radar.yaml)
- Closest public reference: <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>
- Expect the same output surfaces shown above: `latest.md`, `Inbox/`, trend briefs, idea briefs, and the static site

### Robotics radar

- Start from: [`presets/robotics-radar.yaml`](../../presets/robotics-radar.yaml)
- Closest public reference: <https://neapolitanicecream.github.io/recoleta/streams/embodied-ai.html>
- Expect the same output surfaces, with robotics- and embodied-AI-heavy source material

### arXiv digest

- Start from: [`presets/arxiv-digest.yaml`](../../presets/arxiv-digest.yaml)
- Closest public reference: <https://neapolitanicecream.github.io/recoleta/trends/>
- Expect the same output surfaces, but from a paper-first corpus without HN or RSS turned on
