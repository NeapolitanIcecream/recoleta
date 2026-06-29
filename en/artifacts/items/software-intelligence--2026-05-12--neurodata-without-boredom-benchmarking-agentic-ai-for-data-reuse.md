---
source: arxiv
url: https://arxiv.org/abs/2605.12808v2
published_at: '2026-05-12T23:00:18'
authors:
- Ling-Qi Zhang
- Kristin Branson
topics:
- agentic-ai
- code-intelligence
- scientific-data-reuse
- neuroscience-data
- human-ai-interaction
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Neurodata Without Boredom: Benchmarking Agentic AI for Data Reuse

## Summary
The paper tests whether Claude Code and Codex can turn messy neuroscience datasets into a shared format for neural decoding. The main finding is that agents often solve single conversion steps, but full error-free dataset reuse still needs human review.

## Problem
- Neuroscience datasets are split across labs, file formats, APIs, and experiment designs, so reusing them can take substantial manual work.
- Standards such as NWB make files easier to load, but field meanings and analysis choices often remain unclear.
- This matters for cross-dataset analyses and brain-behavior foundation models, where data preparation can become the bottleneck.

## Approach
- The benchmark uses 8 recent mouse neural population recording papers with shared data and code, including NWB files, consortium APIs such as IBL and Allen Brain Observatory, Python files, and MATLAB files.
- Each agent received the paper, methods text, released code, and raw data, then wrote `convert_data.py` to produce `converted_data.pkl` in a prescribed subject/session/trial format.
- The target task was fixed across datasets: train a linear decoder from neural activity to task or behavioral variables.
- The evaluation used outcome metrics, such as dataset statistics and decoder balanced accuracy, plus manual process ratings for data loading, trial construction, neural preprocessing, variable construction, missing-data handling, and code efficiency.
- The study ran Claude Code Opus 4.6 and Codex GPT 5.4 three times per dataset, for 48 agent runs.

## Results
- All 48 runs produced converted data in the required format and yielded decoder-performance values.
- On supervised datasets with human references, agents passed many outcome checks, such as Allen2P format checks at 11/12 for Claude Code and 9/12 for Codex, and Lee2025 checks at 15/15 for both agents.
- Full end-to-end success was rare: Allen2P had 0/3 successful Claude Code runs and 0/3 successful Codex runs by the table's end-to-end criterion, while Lee2025 reached 3/3 for both agents.
- Manual process scores, measured as the proportion of subtasks rated at least ok, ranged from 0.813 to 0.938 for Claude Code across datasets and from 0.885 to 1.000 for Codex.
- The paper reports 169 incorrect or concerning trial-subtask cases per agent for error analysis, with many errors tied to filtering choices, time resolution, processing decisions, assumptions from variable names, and ambiguous semantics.
- Agents-as-judges were unreliable, especially without ground-truth references, so the authors argue for interactive human review in scientific data reuse.

## Link
- [https://arxiv.org/abs/2605.12808v2](https://arxiv.org/abs/2605.12808v2)
