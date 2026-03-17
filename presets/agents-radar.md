# Agents Radar Preset

## Who this is for

- AI builders tracking agent systems, tool use, evaluation, and code agents
- teams that want a local-first daily brief instead of a browser-tab backlog

## What it watches

- Hacker News RSS
- arXiv `cs.AI` and `cs.SE`
- Hugging Face Daily Papers

Config:

- [`agents-radar.yaml`](./agents-radar.yaml)

## What it produces

- local Markdown inbox notes
- trend briefs and idea briefs when you run the downstream commands
- optional static-site output if you build the site from the generated notes

Default local paths:

- SQLite: `~/.local/share/recoleta/presets/agents-radar/recoleta.db`
- Markdown: `~/.local/share/recoleta/presets/agents-radar/outputs`

## Fast start

```bash
cp presets/agents-radar.yaml recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=./recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

## Good next commands

```bash
uv run recoleta trends --granularity day
uv run recoleta ideas --granularity day --date 2026-03-09
uv run recoleta site build
```

## What success looks like

After `run --once`, open:

- `~/.local/share/recoleta/presets/agents-radar/outputs/latest.md`
- `~/.local/share/recoleta/presets/agents-radar/outputs/Inbox/`

After `trends`, `ideas`, and `site build`, expect:

- `~/.local/share/recoleta/presets/agents-radar/outputs/Trends/`
- `~/.local/share/recoleta/presets/agents-radar/outputs/Ideas/`
- `~/.local/share/recoleta/presets/agents-radar/outputs/site/index.html`

## Sample outputs

- First-output guide: [`../docs/guides/first-output-tour.md#agents-radar`](../docs/guides/first-output-tour.md#agents-radar)
- Closest live reference: <https://neapolitanicecream.github.io/recoleta/streams/software-intelligence.html>

## Live reference

- Demo site: <https://neapolitanicecream.github.io/recoleta/>

## Customization ideas

- add `obsidian` to `publish_targets`
- narrow or expand the arXiv queries
- turn on `topic_streams` if you want separate scopes such as `agents` and
  `research-ops`
