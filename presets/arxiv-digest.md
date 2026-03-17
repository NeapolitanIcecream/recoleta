# arXiv Digest Preset

## Who this is for

- users who want a simple paper-first monitoring setup
- anyone who wants to try Recoleta without mixing in HN or RSS noise first

## What it watches

- arXiv `cs.AI`
- arXiv `cs.LG`
- arXiv `cs.CL`

Config:

- [`arxiv-digest.yaml`](./arxiv-digest.yaml)

## What it produces

- local Markdown inbox notes
- trend briefs from a paper-first corpus
- a simple starting point for later adding RSS, HN, or topic streams

Default local paths:

- SQLite: `~/.local/share/recoleta/presets/arxiv-digest/recoleta.db`
- Markdown: `~/.local/share/recoleta/presets/arxiv-digest/outputs`

## Fast start

```bash
cp presets/arxiv-digest.yaml recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=./recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

## Good next commands

```bash
uv run recoleta trends --granularity day
uv run recoleta trends --granularity week --date 2026-03-02 --backfill
uv run recoleta site build
```

## What success looks like

After `run --once`, open:

- `~/.local/share/recoleta/presets/arxiv-digest/outputs/latest.md`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/Inbox/`

After `trends` and `site build`, expect:

- `~/.local/share/recoleta/presets/arxiv-digest/outputs/Trends/`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/site/index.html`

## Sample outputs

- First-output guide: [`../docs/guides/first-output-tour.md#arxiv-digest`](../docs/guides/first-output-tour.md#arxiv-digest)
- Closest live reference: <https://neapolitanicecream.github.io/recoleta/trends/>

## Live reference

- Demo site: <https://neapolitanicecream.github.io/recoleta/>

## Customization ideas

- narrow the arXiv queries to your exact field
- add RSS or OpenReview once the paper-only baseline feels good
- use the preset as a base for a lab-specific or topic-specific digest
