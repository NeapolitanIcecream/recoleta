---
source: arxiv
url: https://arxiv.org/abs/2605.05138v1
published_at: '2026-05-06T17:12:36'
authors:
- Sergey Rodionov
topics:
- coding-agents
- executable-world-models
- arc-agi-3
- model-based-planning
- agent-verification
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Executable World Models for ARC-AGI-3 in the Era of Coding Agents

## Summary
The paper tests a coding-agent baseline for ARC-AGI-3 that writes and checks an executable Python model of each game before acting. It reports useful public-set results, but performance varies widely and private validation is still untested.

## Problem
- ARC-AGI-3 agents must infer goals and dynamics in new interactive games without natural-language instructions, and each real action can waste budget or end a level.
- Direct trial and error is costly, so the agent needs a way to test hypotheses and plans before spending environment actions.
- The benchmark matters because humans can solve these games, while frontier AI systems reportedly scored below 1% as of March 2026.

## Approach
- The agent maintains a Python world model with functions for state reconstruction, transition prediction, goal checking, and planning.
- After each new observation, verifier programs test whether the model reproduces previous transitions and whether the planner can solve already modeled levels.
- The agent is prompted to refactor the code toward simpler shared rules, used as a practical proxy for an MDL-style simplicity bias.
- A plan executor simulates an action sequence in the model, then executes it in the real game while checking predicted frames against observed frames after each step.
- The controller is scripted and game-general: it supplies prompts, handles RESET after GAME_OVER, and provides templates, but it has no hand-coded game-specific logic.

## Results
- On 25 public ARC-AGI-3 games, the agent fully solved 7 games and reached mean per-game RHAE of 32.58% with median per-game RHAE of 14.65%.
- It achieved mean game RHAE above 75% on 6 of 25 games and below 5% on 9 of 25 games.
- Across 29 recorded runs, including repeated fresh runs for some games, it solved 106 of 209 attempted levels.
- Top runs included ar25 at 8/8 levels and 100.00% RHAE, lp85 at 8/8 and 100.00%, tr87 at 6/6 and 100.00%, sb26 at 8/8 and 92.70%, cd82 at 6/6 and 86.51%, and tu93 at 9/9 and 78.33%.
- Run-to-run variance was large: cn04 scored 62.15% RHAE in one fresh run and 0.01% in another; g50t scored 21.43% and 34.03%.
- The public-game runs used Codex CLI 0.122.0 with GPT-5.4; estimated API costs ranged from $34.08 to $620.33 per recorded run, and several runs ended early due to interruptions.

## Link
- [https://arxiv.org/abs/2605.05138v1](https://arxiv.org/abs/2605.05138v1)
