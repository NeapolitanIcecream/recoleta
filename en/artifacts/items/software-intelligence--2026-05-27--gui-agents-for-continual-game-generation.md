---
source: arxiv
url: https://arxiv.org/abs/2605.28258v1
published_at: '2026-05-27T10:08:48'
authors:
- Yixu Huang
- Bo Li
- Na Li
- Zhe Wang
- Kaijie Chen
- Haonan Ge
- Qingyi Si
- Yuanzhe Shen
- Ruihan Yang
- Guangjing Wang
- Hongcheng Guo
topics:
- gui-agents
- code-generation
- game-generation
- software-agents
- playtesting
- multi-agent-systems
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# GUI Agents for Continual Game Generation

## Summary
Play2Code uses a GUI agent to play generated browser games and feed concrete playtest failures back to a code-generating agent. On PlaytestArena, it raises average rubric pass-rate to 66.8% across three model backbones.

## Problem
- One-shot game code generation can produce artifacts that compile and run, then fail during play through unresponsive controls, missing state changes, or broken win conditions.
- Code-level checks miss visual and interaction failures, so generated games need evaluation through actual gameplay.
- Human playtesting is too slow for rapid model-generated builds, which makes automated playtesting useful for game generation workflows.

## Approach
- PlaytestArena contains 200 self-contained HTML/CSS/JS browser-game tasks across 8 genres, paired with 1,548 human-written rubric criteria.
- A GUI agent loads each generated game in a browser, plays through clicks and key presses, and judges each rubric item from observed gameplay.
- Play2Code runs a loop between a Game Agent and a GUI Agent: the Game Agent writes or patches the game, the GUI Agent plays it, then returns a play summary and fix list.
- The system stores experience in episode memory for the current task, skill memory for each agent, and world memory for shared game rules and design patterns.

## Results
- On a 20-game, roughly 120-level playtesting check, GUI agents cleared most levels: GPT-5.4 reached pass@20 of 0.82, Claude Sonnet 4.6 reached 0.79, Kimi K2.5 reached 0.72, and the human reference reached 0.92.
- The GUI evaluator matched blind human annotators on 84.2% of per-criterion judgments on a 32-game sample, with Cohen’s κ=0.64 versus human-human κ=0.66.
- At game level, GUI-derived and human-derived scores were closely aligned on the same 32-game sample: Spearman’s ρ=0.87 and Pearson’s r=0.88.
- Play2Code achieved a 66.8% average rubric pass-rate across three backbones, improving over Direct LLM by 37.1 points and over OpenGame by 14.6 points.
- By backbone, Play2Code reached average rubric pass-rates of 72.3% with GPT-5.4, 71.1% with Claude Sonnet 4.6, and 56.9% with Kimi K2.5.

## Link
- [https://arxiv.org/abs/2605.28258v1](https://arxiv.org/abs/2605.28258v1)
