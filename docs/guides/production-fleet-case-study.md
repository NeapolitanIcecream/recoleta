# Production fleet case study

Snapshot date: 2026-07-24

Latest selected output: 2026-07-23

## What is running

The public Recoleta site is generated from one fleet manifest and three
isolated child instances:

| Stream | Scope | Independent state |
| --- | --- | --- |
| Embodied AI | robotics, world models, and embodied learning | config, SQLite DB, outputs, delivery state |
| Software Intelligence | coding agents, software engineering, and developer tools | config, SQLite DB, outputs, delivery state |
| Cross Platform | signals that cross the two primary scopes | config, SQLite DB, outputs, delivery state |

The children share a Huldra arXiv metadata service but do not share Recoleta
state. The aggregate site builder combines their generated artifacts and
localized projections.

The public snapshot contained:

- 244 trend briefs;
- 244 idea briefs;
- 1,362 linked source notes selected from 7,902 available item notes;
- 575 topic labels;
- English and Simplified Chinese publication trees.

These counts describe the project maintainers’ production deployment. They are
evidence of sustained dogfooding, not evidence of independent adoption.

## One real output and its source trail

The selected Software Intelligence brief is
[“Agent evaluation reaches ambiguous projects as reliability moves into the harness”](https://neapolitanicecream.github.io/recoleta/en/trends/software-intelligence--day--2026-07-23--trend--2079.html).

It brings together five public preprints:

- [ICAE Bench](https://arxiv.org/abs/2607.21217v1), which evaluates coding
  agents as interactive project builders;
- [Tencent WorkBuddy-Bench](https://arxiv.org/abs/2607.20911v1), a multi-domain
  coding-agent benchmark;
- [Delivery, Not Storage](https://arxiv.org/abs/2607.20972v1), on cue-anchored
  working memory as a harness property;
- [Euclid MCP](https://arxiv.org/abs/2607.21412v1), a deterministic logical
  reasoning server using the Model Context Protocol;
- [pAI Econ Claude](https://arxiv.org/abs/2607.21268v1), a gated
  human-in-the-loop multi-agent workflow.

The brief demonstrates the intended reading path: start with a cross-paper
claim, inspect its grouped findings, then follow the attached source notes and
original papers. An attached read trace establishes which material the
synthesis used; it does not prove that every generated sentence is entailed by
that material.

## Reproduce the evaluation path

The fastest check uses one curated copy of that production brief. It requires no
source account, Huldra process, API key, or model call:

```bash
uv run recoleta demo --output-dir recoleta-demo
uv run --no-project --python 3.14 python -m http.server 8000 --directory recoleta-demo
```

Open <http://127.0.0.1:8000/>. This checks package data, Markdown rendering,
site generation, and local serving. It does not reproduce ingestion or
synthesis.

To operate a comparable three-child topology, start from the
[redacted fleet shape](../../examples/production-fleet/README.md). The example
keeps the stream boundaries and isolation model but omits private operational
paths, recipients, costs, and team-specific settings.

## What this case does not establish

- It is not a blind comparison against another research system.
- It is not an external-user retention result.
- It does not publish private costs, failure records, recipient data, or team
  identity.
- A public brief can still contain synthesis errors; readers should inspect the
  cited material before relying on a claim.
- The bundled offline brief is a fixed evaluation artifact, not evidence that a
  new user generated a new output.

Independent activations and retained external use are tracked separately from
site visits, package downloads, stars, and this internal production deployment.
