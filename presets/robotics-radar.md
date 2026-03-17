# Robotics Radar Preset

Use this preset when you want a robotics-focused feed with embodied AI, VLA,
manipulation, and lab-paper coverage.

## Sources

- arXiv `cs.RO`
- arXiv `cs.AI AND all:robot`
- Hugging Face Daily Papers

Config file:

- [`robotics-radar.yaml`](./robotics-radar.yaml)

## Default outputs

- Markdown inbox notes after `run --once`
- Robotics-oriented trend briefs after `recoleta trends`
- Optional static site after `recoleta site build`

Default local paths:

- SQLite: `~/.local/share/recoleta/presets/robotics-radar/recoleta.db`
- Markdown: `~/.local/share/recoleta/presets/robotics-radar/outputs`

## Run it

```bash
cp presets/robotics-radar.yaml recoleta.yaml

cat <<'ENV' > .env
RECOLETA_CONFIG_PATH=./recoleta.yaml
RECOLETA_LLM_API_KEY="sk-replace-me"
ENV

uv run recoleta run --once --analyze-limit 50 --publish-limit 20
```

## Check the first run

Open these paths after `run --once`:

- `~/.local/share/recoleta/presets/robotics-radar/outputs/latest.md`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/Inbox/`

Then run:

```bash
uv run recoleta trends --granularity day
uv run recoleta trends-week --date 2026-03-02
uv run recoleta site build
```

That should create:

- `~/.local/share/recoleta/presets/robotics-radar/outputs/Trends/`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/site/index.html`

## Compare with the public example

- First-output guide:
  [`../docs/guides/first-output-tour.md#robotics-radar`](../docs/guides/first-output-tour.md#robotics-radar)
- Closest live page:
  <https://neapolitanicecream.github.io/recoleta/streams/embodied-ai.html>
- Demo home: <https://neapolitanicecream.github.io/recoleta/>

## Common tweaks

- Add RSS feeds from robotics labs or newsletters.
- Add `obsidian` or `telegram` to `publish_targets`.
- Split the preset into stream-local scopes such as `robotics` and
  `embodied-ai`.
