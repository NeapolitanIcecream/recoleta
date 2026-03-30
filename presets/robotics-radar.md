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

With default workflow settings:

- Markdown inbox notes after `run now`
- Day-level trend briefs after `run now`
- Day-level idea briefs when the window has enough evidence
- Static site output after `run now`

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

uv run recoleta run now
```

## Check the first run

Open these paths after `run now`:

- `~/.local/share/recoleta/presets/robotics-radar/outputs/latest.md`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/Inbox/`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/Trends/`
- `~/.local/share/recoleta/presets/robotics-radar/outputs/site/index.html`
- If ideas were emitted:
  `~/.local/share/recoleta/presets/robotics-radar/outputs/Ideas/`

Use these follow-up commands when you want a weekly workflow or a targeted
rebuild:

```bash
uv run recoleta run week --date 2026-03-02
uv run recoleta stage trends --granularity day --date 2026-03-02
uv run recoleta run site build
```

## Compare with the public example

- First-output guide:
  [`../docs/guides/first-output-tour.md#robotics-radar`](../docs/guides/first-output-tour.md#robotics-radar)
- Closest live page:
  <https://neapolitanicecream.github.io/recoleta/en/streams/embodied-ai.html>
- Demo home: <https://neapolitanicecream.github.io/recoleta/>

## Common tweaks

- Add RSS feeds from robotics labs or newsletters.
- Add `obsidian` or `telegram` to `publish_targets`.
- Copy this preset into one child instance config and pair it with another
  child config under a `fleet.yaml` manifest if you want separate robotics and
  embodied-AI radars.
