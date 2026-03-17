# Recoleta Starter Presets

Use a preset when you want a working config without editing the full example
file first.

Each preset uses its own SQLite database and Markdown output directory, so you
can try them side by side without mixing state.

If you want screenshots and sample pages for comparison, start with
[`../docs/guides/first-output-tour.md`](../docs/guides/first-output-tour.md).

## Pick a preset

### Agents radar

- Best for: tracking agent tooling, code agents, evals, and AI builder workflow
- Sources: Hacker News, arXiv, Hugging Face Daily Papers
- Config: [`agents-radar.yaml`](./agents-radar.yaml)
- Guide: [`agents-radar.md`](./agents-radar.md)
- Public example:
  [`first-output-tour.md#agents-radar`](../docs/guides/first-output-tour.md#agents-radar)

### Robotics radar

- Best for: embodied AI, VLA, manipulation, and robotics research
- Sources: arXiv, Hugging Face Daily Papers
- Config: [`robotics-radar.yaml`](./robotics-radar.yaml)
- Guide: [`robotics-radar.md`](./robotics-radar.md)
- Public example:
  [`first-output-tour.md#robotics-radar`](../docs/guides/first-output-tour.md#robotics-radar)

### arXiv digest

- Best for: a paper-only first run without HN or RSS
- Sources: arXiv only
- Config: [`arxiv-digest.yaml`](./arxiv-digest.yaml)
- Guide: [`arxiv-digest.md`](./arxiv-digest.md)
- Public example:
  [`first-output-tour.md#arxiv-digest`](../docs/guides/first-output-tour.md#arxiv-digest)

## Use one in four steps

1. Copy the preset you want to `recoleta.yaml`.
2. Set `RECOLETA_CONFIG_PATH` and your LLM credentials in `.env`.
3. Run `uv run recoleta run --once` or
   `docker compose run --rm recoleta run --once`.
4. Open the preset guide and check the output paths listed there.
