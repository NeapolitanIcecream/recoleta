# arXiv Digest Preset

Use this preset when you want the simplest first run: papers first, other
sources later.

## Sources

- arXiv `cs.AI`
- arXiv `cs.LG`
- arXiv `cs.CL`

Config file:

- [`arxiv-digest.yaml`](./arxiv-digest.yaml)

## Default outputs

- Markdown inbox notes after `run --once`
- Trend briefs from a paper-only corpus
- A clean base for adding RSS, OpenReview, or topic streams later

Default local paths:

- SQLite: `~/.local/share/recoleta/presets/arxiv-digest/recoleta.db`
- Markdown: `~/.local/share/recoleta/presets/arxiv-digest/outputs`

## Run it

```bash
cp presets/arxiv-digest.yaml recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=./recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

## Check the first run

Open these paths after `run --once`:

- `~/.local/share/recoleta/presets/arxiv-digest/outputs/latest.md`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/Inbox/`

Then run:

```bash
uv run recoleta trends --granularity day
uv run recoleta trends --granularity week --date 2026-03-02 --backfill
uv run recoleta site build
```

That should create:

- `~/.local/share/recoleta/presets/arxiv-digest/outputs/Trends/`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/site/index.html`

## Compare with the public example

- First-output guide:
  [`../docs/guides/first-output-tour.md#arxiv-digest`](../docs/guides/first-output-tour.md#arxiv-digest)
- Closest live page: <https://neapolitanicecream.github.io/recoleta/trends/>
- Demo home: <https://neapolitanicecream.github.io/recoleta/>

## Common tweaks

- Narrow the arXiv queries to your exact field.
- Add RSS or OpenReview once the paper-only baseline feels right.
- Use the preset as the base for a lab-specific or topic-specific digest.
