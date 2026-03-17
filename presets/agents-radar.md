# Agents Radar Preset

Use this preset when you want to follow agent tooling, code agents, evals, and
AI builder workflow from one local workspace.

## Sources

- Hacker News RSS
- arXiv `cs.AI` and `cs.SE`
- Hugging Face Daily Papers

Config file:

- [`agents-radar.yaml`](./agents-radar.yaml)

## Default outputs

- Markdown inbox notes after `run --once`
- Trend briefs after `recoleta trends`
- Idea briefs after `recoleta ideas`
- Optional static site after `recoleta site build`

Default local paths:

- SQLite: `~/.local/share/recoleta/presets/agents-radar/recoleta.db`
- Markdown: `~/.local/share/recoleta/presets/agents-radar/outputs`

## Run it

```bash
cp presets/agents-radar.yaml recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=./recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

## Check the first run

Open these paths after `run --once`:

- `~/.local/share/recoleta/presets/agents-radar/outputs/latest.md`
- `~/.local/share/recoleta/presets/agents-radar/outputs/Inbox/`

Then run:

```bash
uv run recoleta trends --granularity day
uv run recoleta ideas --granularity day --date 2026-03-09
uv run recoleta site build
```

That should create:

- `~/.local/share/recoleta/presets/agents-radar/outputs/Trends/`
- `~/.local/share/recoleta/presets/agents-radar/outputs/Ideas/`
- `~/.local/share/recoleta/presets/agents-radar/outputs/site/index.html`

## Compare with the public example

- First-output guide:
  [`../docs/guides/first-output-tour.md#agents-radar`](../docs/guides/first-output-tour.md#agents-radar)
- Closest live page:
  <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>
- Demo home: <https://neapolitanicecream.github.io/recoleta/>

## Common tweaks

- Add `obsidian` to `publish_targets`.
- Narrow or expand the arXiv queries.
- Enable `topic_streams` if you want separate scopes such as `agents` and
  `research-ops`.
