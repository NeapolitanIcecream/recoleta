---
source: arxiv
url: https://arxiv.org/abs/2606.09774v1
published_at: '2026-06-08T17:35:17'
authors:
- Matthew Ho
- Brian Liu
- Jixuan Chen
- Audrey Wang
- Lianhui Qin
topics:
- coding-agents
- scientific-simulation
- code-intelligence
- agent-adapters
- self-evolving-agents
- validation-guided-generation
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# SIGA: Self-Evolving Coding-Agent Adapters for Scientific Simulation

## Summary
SIGA adds a small simulator-specific adapter to a coding agent so it can write scientific simulation input decks. On GEOS, it reports expert-level deck quality in about five minutes instead of about three hours.

## Problem
- Scientific simulators such as GEOS, OpenFOAM, and LAMMPS require specialized input files with exact vocabulary, schema rules, cross-file references, and valid stop conditions.
- Scientists can spend hours or days reading documentation, adapting examples, and debugging invalid configurations before a simulation can run.
- General coding agents can edit files and run commands, but they often lack the simulator contract needed to choose valid tags, fill required sections, and know when the deck is complete.

## Approach
- SIGA wraps a frozen coding-agent harness rather than replacing its planning loop. The base agent still navigates files, edits code, runs shell commands, and repairs outputs.
- It adds four grounding components: semantic retrieval over documentation, schemas, examples, and technical snippets; a 775-token procedural memory cheatsheet; an agent-callable XML validator; and a validation stop hook.
- The validator uses `xmllint --schema` for GEOS. The stop hook blocks final submission until XML files in `/workspace/inputs/` parse and pass schema checks, with structured repair feedback.
- A self-evolution loop rewrites adapter text, memory, and auxiliary skills from prior trajectories while keeping the model and harness fixed.

## Results
- On a representative GEOS task, SIGA produced a complete deck in about 5 minutes with TreeSim above 0.90, matching an extended-budget human expert who needed about 3 hours. The claimed wall-clock speedup is about 36x.
- On a harder held-out GEOS set, grounding raised TreeSim from 0.720 for the bare agent to 0.789, about a 10% relative gain.
- The grounded setup reduced across-seed standard deviation by about 16x on the held-out GEOS set, which points to fewer unstable or failed runs.
- The self-evolved SIGA variant reached the highest held-out GEOS mean and matched or beat the strongest hand-designed configuration reported in the excerpt.
- Transfer tests on OpenFOAM and LAMMPS found different bottlenecks: validation helped most when structural completeness failed, while memory and retrieval helped most when domain choices were wrong.

## Link
- [https://arxiv.org/abs/2606.09774v1](https://arxiv.org/abs/2606.09774v1)
