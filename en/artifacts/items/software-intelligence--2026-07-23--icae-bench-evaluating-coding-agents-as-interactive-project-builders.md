---
source: arxiv
url: https://arxiv.org/abs/2607.21217v1
published_at: '2026-07-23T11:31:38'
authors:
- Zhongyuan Peng
- Dan Huang
- Chuyu Zhang
- Caijun Xu
- Changyi Xiao
- Shibo Hong
- David Lo
- Lin Qiu
- Xuezhi Cao
- Jiyuan He
- Yixin Cao
topics:
- code-intelligence
- automated-software-production
- coding-agents
- interactive-benchmark
- repository-generation
- multi-agent-software-engineering
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders

## Summary
ICAE-Bench evaluates whether coding agents can turn incomplete product intent into working repositories through clarification, planning, tool use, debugging, and implementation. It reports a 480-task benchmark spanning 12 languages, with experiments showing that agents often reproduce visible behavior but struggle with hidden constraints, boundary cases, and long-horizon integration.

## Problem
- Existing coding benchmarks mainly use complete specifications or existing repositories, so they do not measure whether an agent can clarify ambiguous intent and build a project from scratch.
- This matters because interactive project building requires agents to recover requirements, preserve them during implementation, and deliver runnable software across repository-level constraints.

## Approach
- Derive each task from a verified open-source repository, create a complete GroundPRD and black-box behavioral cases, then hide selected API, edge-case, and architectural constraints to produce Fuzzy L1, L2, and L3 requirements.
- Simulate clarification with a grounded User Agent backed by authored User Agent Data, preventing hallucinated requirements, implementation leakage, and unreproducible interaction.
- Remove the original code and tests from a provisioned execution image, allowing agents to construct the repository from the fuzzy requirement and recovered information.
- Score open-ended implementations with black-box Native and Enhanced tests plus diagnostics for functional correctness, semantic and API similarity, structural fidelity, design quality, and interaction quality.

## Results
- ICAE-Bench contains 480 tasks, with 40 tasks in each of 12 languages; ICAE-Bench-Lite contains 50 tasks across 10 languages.
- The benchmark evaluates 6 coding models in 2 agent frameworks, Claude Code and OpenHands, and finds that ambiguous project generation remains challenging.
- GroundPRD is reported as a strong upper bound; clarification recovers only part of the performance gap, and greater constraint coverage does not automatically produce a higher pass rate.
- Agents generally reproduce visible behavior but struggle with hidden constraints, boundary cases, and long-horizon integration; the excerpt does not provide aggregate pass-rate or model-by-model metric values.
- On ICAE-Bench-Lite, Fuzzy L1 and L3 were judged equivalent to GroundPRD for all 50 repositories, with mean semantic-similarity scores of 0.952 and 0.942, respectively, and no case judged likely to fail the same tests.

## Link
- [https://arxiv.org/abs/2607.21217v1](https://arxiv.org/abs/2607.21217v1)
