---
source: arxiv
url: http://arxiv.org/abs/2604.01437v1
published_at: '2026-04-01T22:24:08'
authors:
- Jingyue Li
- "Andr\xE9 Storhaug"
topics:
- agentic-ai-evaluation
- software-engineering
- llm-agents
- reproducibility
- trajectory-analysis
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering

## Summary
This paper studies how agentic AI systems for software engineering are being evaluated and argues that current practice is hard to reproduce and hard to explain. It proposes concrete reporting rules and a trajectory-based evaluation method built around publishing and analyzing Thought-Action-Result (TAR) logs.

## Problem
- Evaluations of software engineering agents often rely on black-box LLM behavior, random outputs, and incomplete reporting, which makes results hard to reproduce and compare.
- In the authors' review of 18 recent SE papers, only 1 paper compared against a relevant state-of-the-art agentic baseline, so many claimed gains are measured against weaker baselines such as classical methods, naive prompting, or non-agent models.
- Re-running agent evaluations is expensive because API calls, repeated trials, and prompt sensitivity can change outcomes and raise replication cost.

## Approach
- The paper analyzes 18 papers from ICSE 2025/2026, FSE 2025, ASE 2025, and ISSTA 2025, and extracts common evaluation patterns: baselines used, ablations, failure analysis, cost analysis, and reproducibility details.
- It recommends a minimum reporting standard: publish prompts, temperature settings, and exact LLM versions to make evaluations reproducible.
- It proposes that papers also publish agent Thought-Action-Result trajectories, or summarized versions of them, so later work can inspect why an agent succeeded or failed instead of only seeing final aggregate scores.
- For long trajectories, the paper suggests automatic analysis with LLM summarization in 3 steps: summarize each run, compare agents on the same run, then aggregate repeated strengths and weaknesses across runs.
- A proof-of-concept case study uses open TAR traces from a vulnerability-fix detection agent and compares agents built on Qwen3-235B, Llama-3.3-70B-Instruct, and Gemma-3-27B with Kimi K2.5 Instant as the analyzer.

## Results
- Literature review result: 18 agentic SE papers were analyzed; 11/18 used multi-agent setups.
- Baseline result: only 1/18 papers compared against an existing agentic AI baseline; 13/18 included ablation studies.
- Reproducibility result: all reviewed papers named the LLM family, but only a few papers gave exact version identifiers, with examples such as GPT-3.5-0125.
- Cost/reporting result: some papers reported API or token costs, and some ran temperature sensitivity or repeated trials, but the paper does not provide a full quantitative benchmark table across all 18 studies.
- Case study result: the proof of concept compares 10 randomly sampled failed Qwen3-235B runs against corresponding Gemma-3-27B and Llama-3.3-70B-Instruct runs on the same cases; the stronger agents solved some cases that Qwen failed.
- The paper does not claim a new state-of-the-art task score. Its main concrete claim is methodological: automated TAR analysis can recover interpretable agent differences such as verification behavior, dominant failure modes, and per-model strengths from shared traces.

## Link
- [http://arxiv.org/abs/2604.01437v1](http://arxiv.org/abs/2604.01437v1)
