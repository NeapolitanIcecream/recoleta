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

With default workflow settings:

- Markdown inbox notes after `run now`
- Day-level trend briefs after `run now`
- Day-level idea briefs when the window has enough evidence
- Static site output after `run now`

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

uv run recoleta run now
```

## Check the first run

Open these paths after `run now`:

- `~/.local/share/recoleta/presets/arxiv-digest/outputs/latest.md`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/Inbox/`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/Trends/`
- `~/.local/share/recoleta/presets/arxiv-digest/outputs/site/index.html`
- If ideas were emitted:
  `~/.local/share/recoleta/presets/arxiv-digest/outputs/Ideas/`

Use these follow-up commands when you want a weekly workflow or a targeted
rebuild:

```bash
uv run recoleta run week --date 2026-03-02
uv run recoleta stage trends --granularity day --date 2026-03-02
uv run recoleta run site build
```

## Compare with the public example

- First-output guide:
  [`../docs/guides/first-output-tour.md#arxiv-digest`](../docs/guides/first-output-tour.md#arxiv-digest)
- Closest live page: <https://neapolitanicecream.github.io/recoleta/en/trends/index.html>
- Demo home: <https://neapolitanicecream.github.io/recoleta/>

## Common tweaks

- Narrow the arXiv queries to your exact field.
- Add RSS or OpenReview once the paper-only baseline feels right.
- Use the preset as the base for a lab-specific or topic-specific digest.
