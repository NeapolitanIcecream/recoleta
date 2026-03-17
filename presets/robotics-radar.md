# Robotics Radar Preset

## Who this is for

- embodied AI and robotics researchers
- teams tracking VLA systems, manipulation, and robotics learning

## What it watches

- arXiv `cs.RO`
- arXiv `cs.AI AND all:robot`
- Hugging Face Daily Papers

Config:

- [`robotics-radar.yaml`](./robotics-radar.yaml)

## What it produces

- local Markdown inbox notes
- robotics-oriented trend briefs after `recoleta trends`
- optional public-site output derived from the generated trend markdown

Default local paths:

- SQLite: `~/.local/share/recoleta/presets/robotics-radar/recoleta.db`
- Markdown: `~/.local/share/recoleta/presets/robotics-radar/outputs`

## Fast start

```bash
cp presets/robotics-radar.yaml recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=./recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

## Good next commands

```bash
uv run recoleta trends --granularity day
uv run recoleta trends-week --date 2026-03-02
uv run recoleta site build
```

## What success looks like

After `run --once`, open:

- `~/.local/share/recoleta/presets/robotics-radar/outputs/latest.md`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/Inbox/`

After `trends` and `site build`, expect:

- `~/.local/share/recoleta/presets/robotics-radar/outputs/Trends/`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/site/index.html`

## Sample outputs

- First-output guide: [`../docs/guides/first-output-tour.md#robotics-radar`](../docs/guides/first-output-tour.md#robotics-radar)
- Closest live reference: <https://neapolitanicecream.github.io/recoleta/streams/embodied-ai.html>

## Live reference

- Demo site: <https://neapolitanicecream.github.io/recoleta/>

## Customization ideas

- add RSS feeds from robotics labs or newsletters
- add `obsidian` or `telegram` to `publish_targets`
- split the preset into stream-local scopes for `robotics` and `embodied-ai`
