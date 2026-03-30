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

With default workflow settings:

- Markdown inbox notes after `run now`
- Day-level trend briefs after `run now`
- Day-level idea briefs when the window has enough evidence
- Static site output after `run now`

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

uv run recoleta run now
```

## Check the first run

Open these paths after `run now`:

- `~/.local/share/recoleta/presets/agents-radar/outputs/latest.md`
- `~/.local/share/recoleta/presets/agents-radar/outputs/Inbox/`
- `~/.local/share/recoleta/presets/agents-radar/outputs/Trends/`
- `~/.local/share/recoleta/presets/agents-radar/outputs/site/index.html`
- If ideas were emitted:
  `~/.local/share/recoleta/presets/agents-radar/outputs/Ideas/`

Use these follow-up commands when you want a weekly workflow or a targeted
rebuild:

```bash
uv run recoleta run week --date 2026-03-09
uv run recoleta stage ideas --granularity day --date 2026-03-09
uv run recoleta run site build
```

## Compare with the public example

- First-output guide:
  [`../docs/guides/first-output-tour.md#agents-radar`](../docs/guides/first-output-tour.md#agents-radar)
- Closest live page:
  <https://neapolitanicecream.github.io/recoleta/en/streams/software-intelligence.html>
- Demo home: <https://neapolitanicecream.github.io/recoleta/>

## Common tweaks

- Add `obsidian` to `publish_targets`.
- Narrow or expand the arXiv queries.
- Copy this preset into a second child instance config and combine both under a
  `fleet.yaml` manifest if you want separate radars such as `agents` and
  `research-ops`.
