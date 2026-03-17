# Recoleta Starter Presets

These presets are non-secret starting points you can copy into your own
workspace. Keep API keys and delivery credentials in environment variables only.

See [`../docs/guides/first-output-tour.md`](../docs/guides/first-output-tour.md)
when you want sample screenshots and a concrete "what should I see after the
first run?" reference.

## Presets

### Agents radar

- Best for: AI builders, agent infra tracking, tool-use and code-agent monitoring
- Sources: Hacker News, arXiv, Hugging Face Daily Papers
- Outputs: local Markdown by default
- Config: [`agents-radar.yaml`](./agents-radar.yaml)
- Guide: [`agents-radar.md`](./agents-radar.md)
- Sample outputs: [`../docs/guides/first-output-tour.md#agents-radar`](../docs/guides/first-output-tour.md#agents-radar)
- Live demo: <https://neapolitanicecream.github.io/recoleta/>

### Robotics radar

- Best for: embodied AI, VLA, manipulation, and robotics research watching
- Sources: arXiv, Hugging Face Daily Papers
- Outputs: local Markdown by default
- Config: [`robotics-radar.yaml`](./robotics-radar.yaml)
- Guide: [`robotics-radar.md`](./robotics-radar.md)
- Sample outputs: [`../docs/guides/first-output-tour.md#robotics-radar`](../docs/guides/first-output-tour.md#robotics-radar)
- Live demo: <https://neapolitanicecream.github.io/recoleta/>

### arXiv digest

- Best for: paper-first tracking without HN or RSS noise
- Sources: arXiv only
- Outputs: local Markdown by default
- Config: [`arxiv-digest.yaml`](./arxiv-digest.yaml)
- Guide: [`arxiv-digest.md`](./arxiv-digest.md)
- Sample outputs: [`../docs/guides/first-output-tour.md#arxiv-digest`](../docs/guides/first-output-tour.md#arxiv-digest)
- Live demo: <https://neapolitanicecream.github.io/recoleta/>

## How To Use One

1. Copy the preset you want into `recoleta.yaml`.
2. Set `RECOLETA_CONFIG_PATH` and your LLM credentials in `.env`.
3. Run `uv run recoleta run --once` or `docker compose run --rm recoleta run --once`.
4. Check the preset-specific output directory shown in the YAML file.

Each preset uses its own local SQLite and Markdown output paths so you can test
them side by side without mixing state.
