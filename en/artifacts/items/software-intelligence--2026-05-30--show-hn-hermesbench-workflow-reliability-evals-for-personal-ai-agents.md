---
source: hn
url: https://verkyyi.github.io/hermesbench/
published_at: '2026-05-30T23:03:40'
authors:
- verkyyi26
topics:
- agent-evaluation
- personal-ai-agents
- workflow-reliability
- code-agent-runner
- human-ai-interaction
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Show HN: HermesBench – workflow reliability evals for personal AI agents

## Summary
HermesBench evaluates full personal-agent configurations across real workflow recipes and publishes trace-backed scores. The current public baseline is 78.2 across 27 recipes, so the main value is transparent reliability testing for agent deployments.

## Problem
- Personal-agent quality depends on prompts, model/provider choice, tools, memory, safety behavior, delegation, latency, and stability, so model-only tests miss many user-visible failures.
- Personal agents can cause harm when they finish the wrong task, use unsafe side effects, hide uncertainty, or become too slow for normal use.
- Early agent benchmarks often lack inspectable traces and clear limits, which makes setup comparisons hard to trust.

## Approach
- HermesBench runs scenario recipes against a complete Hermes configuration, including prompt, model/provider, tools, AgentSkills, memory, gateway behavior, delegation, safety, latency, and stability.
- Each recipe has scenario definitions, public score axes, driver closure decisions, deterministic checks, and redacted trace timelines.
- Users can run a default single-recipe path through Codex, Claude, or another coding agent by loading the HermesBench skill and saving artifacts.
- Full bundle runs are optional because they cost more and take longer.
- Scoring rewards useful completion, truthful uncertainty, safe behavior, stability, prompt responses, and clear communication; lopsided scores receive penalties.

## Results
- The published baseline score is 78.2 across 27 personal-agent recipes.
- The bundled catalog covers 10 workflow areas: context, calendar, web, reports, communication, location, travel, finance, safety, and power-user integrations.
- The public site has 3 evidence tabs for recipes, profiles, and traces.
- The excerpt reports 1 early public baseline and says this is not a base-model leaderboard.
- No per-axis scores, confidence intervals, failure counts, or comparisons against other agent benchmarks are provided in the excerpt.

## Link
- [https://verkyyi.github.io/hermesbench/](https://verkyyi.github.io/hermesbench/)
