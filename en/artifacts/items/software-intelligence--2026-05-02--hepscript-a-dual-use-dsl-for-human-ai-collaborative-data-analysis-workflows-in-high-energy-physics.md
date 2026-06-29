---
source: arxiv
url: https://arxiv.org/abs/2605.01423v1
published_at: '2026-05-02T12:42:34'
authors:
- Junkun Jiao
- Tong Liu
- Ke Li
- Weimin Song
- Yipu Liao
- Bolun Zhang
- Beijiang Liu
- Chang-Zheng Yuan
- Yue Sun
topics:
- domain-specific-language
- code-generation
- llm-agents
- scientific-workflows
- human-ai-collaboration
- high-energy-physics
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# HepScript: A Dual-Use DSL for Human-AI Collaborative Data Analysis Workflows in High-Energy Physics

## Summary
HepScript is a Ruby-embedded DSL that lets physicists and LLM agents specify BESIII high-energy physics analysis workflows, then generates BOSS and ROOT code. Its main claim is that a constrained DSL makes agent code generation more reliable and cuts human coding work.

## Problem
- HEP analyses use large datasets and experiment-specific software, so direct LLM code generation can fail on domain rules, long workflows, and low-level APIs.
- BESIII workflows need a bridge between physics intent, including particle reconstruction and selection cuts, and production BOSS/ROOT code.
- The problem matters because analysis code is repetitive, error-prone, and hard for agents to generate safely without a narrow action space.

## Approach
- HepScript expresses dataset preparation, base selection, advanced selection, visualization, and statistical analysis in a constrained Ruby syntax.
- A processor translates HepScript into target code for BOSS, ROOT, shell scripts, Python, or C++ snippets.
- The processor uses templates for stable code, Ruby translators for complex syntax, and LLM calls for analysis-dependent tasks, including cascade decay logic and ROOT scripts.
- LLMs generate HepScript from papers using a long prompt with one complete workflow example and YARD API documentation; retry loops feed processor errors back to the model.

## Results
- Human-written HepScript for 45 BESIII papers generated 63 BOSS algorithm packages; with the LLM-assisted component disabled, all 63 compiled without errors.
- Across two full case studies, HepScript reduced human-written analysis code by 93% by removing BOSS boilerplate and repeated ROOT plotting code.
- For LLM-generated HepScript over 72 BOSS packages, DeepSeek-R1 reached 47.3% initial success, 87.8% after one retry, and 94.6% after three retries.
- GLM-4.7 reached 43.2% initial success, 90.5% after one retry, and 95.9% after three retries on the same 72-package task.
- In the variable-storage subtask for human-written specs, DeepSeek-V3, GPT-4o, GLM-4.7, and Qwen3-Max started at 93.8-96.9% success; all tested models reached 98.5% after one retry.
- Two ROOT case studies executed end-to-end and reproduced figures from the original BESIII papers; the authors state these are pipeline checks, not official physics results.

## Link
- [https://arxiv.org/abs/2605.01423v1](https://arxiv.org/abs/2605.01423v1)
