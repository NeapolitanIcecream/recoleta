---
source: arxiv
url: https://arxiv.org/abs/2606.17819v1
published_at: '2026-06-16T11:46:56'
authors:
- Maksim Shaposhnikov
- Nicolas Fortuin
- Simon Stipcich
- Maria I. Gorinova
- Amy Heineike
- Rob Willoughby
topics:
- agent-evaluation
- agent-skills
- code-intelligence
- software-agents
- llm-benchmarks
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# A Framework for Evaluating Agentic Skills at Scale

## Summary
The paper presents a scalable method for testing whether agent skills improve LLM agent behavior on realistic coding tasks. It generates tasks and hidden rubrics from each skill, then compares agent runs with and without the skill.

## Problem
- Agent skills are used to encode workflows, API patterns, coding conventions, and domain rules, but authors lack a reusable way to test whether one skill improves agent output.
- Existing agent benchmarks mostly test general task solving, tool use, or coding ability; they do not measure how a specific skill changes behavior across models.
- This matters because a skill can alter instruction following, goal completion, cost, and model choice in production agent systems.

## Approach
- The method reads a skill, infers realistic use cases, builds executable tasks, and creates hidden scoring rubrics for goal completion and instruction following.
- An environment-engineering agent checks required tools, runtimes, credentials, network access, repositories, databases, UI access, and other dependencies.
- A task-generation agent creates task descriptions, input files, execution setup, and rubrics; a validation agent removes tasks with missing inputs, broken environments, or rubric leakage.
- Each task is solved twice: once without the skill and once with the relevant skill installed and announced to the agent.
- A judge model, Sonnet 4.6 in Claude Code, scores solver outputs against 100-point instruction-following and 100-point goal-completion rubrics.

## Results
- The study uses about 500 real-world skills, about 1,000 generated tasks, 19 agent-model configurations, and about 38,000 valid trajectories.
- Access to a relevant skill improves overall scores by 5.5 to 22 points depending on the model, with most of the gain coming from instruction following.
- On instruction following with skills, the best reported scores are Opus 4.8 at 88.0, Opus 4.7 at 87.7, Sonnet 4.6 at 85.9, GLM 5.1 at 85.0, Gemini 3.5 Flash at 81.6, and Gemini 3.1 Pro Preview at 81.5.
- Open-weights GLM 5.1 reaches 85.0 on instruction following, close to the top proprietary models; Kimi K2.6, MiniMax 2.7, Qwen3-Coder-Next, and Gemini 3.1 Flash Lite cluster around 57–60.
- Nemotron Nano 30B scores 25.2 and Nemotron Super 120B scores 46.8 on instruction following with skills, the weakest reported results.
- For Opus 4.8, instruction following rises from 59.8 to 88.0, goal completion rises from 93.3 to 97.5, and overall score rises from 76.6 to 92.7, a +16.2 skill delta; cost increases from $2.66 to $3.26 per scenario.

## Link
- [https://arxiv.org/abs/2606.17819v1](https://arxiv.org/abs/2606.17819v1)
