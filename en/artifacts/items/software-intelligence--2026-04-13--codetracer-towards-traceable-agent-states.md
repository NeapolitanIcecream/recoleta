---
source: arxiv
url: http://arxiv.org/abs/2604.11641v3
published_at: '2026-04-13T15:52:03'
authors:
- Han Li
- Yifan Yao
- Letian Zhu
- Rili Feng
- Hongyi Ye
- Jiaming Wang
- Yancheng He
- Pengyu Zou
- Lehan Zhang
- Xinping Lei
- Haoyang Huang
- Ken Deng
- Ming Sun
- Zhaoxiang Zhang
- He Ye
- Jiaheng Liu
topics:
- code-agents
- agent-tracing
- failure-localization
- software-engineering-benchmark
- code-intelligence
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# CodeTracer: Towards Traceable Agent States

## Summary
CodeTracer is a tracing and diagnosis system for code agents that reconstructs agent runs into state-transition trees and finds the earliest failure-causing stage and steps. The paper also introduces CodeTraceBench, a large benchmark of executed and annotated code-agent trajectories for failure localization.

## Problem
- Code agents now run long, multi-step workflows across tools, files, tests, and environments, so when they fail it is hard to tell where the run first went wrong and which later errors came from that mistake.
- Existing evaluation usually collapses a whole run into a single success or failure label, or depends on small manual inspections, which does not scale to real software engineering trajectories.
- This matters for debugging, agent improvement, and recovery: if the system cannot locate the failure onset, extra iterations often turn into loops, wasted tokens, and wrong edits.

## Approach
- CodeTracer parses heterogeneous run artifacts from different agent frameworks with an evolving extractor that can reuse or synthesize format-specific parsers, then normalizes runs into typed step records.
- It builds a hierarchical trace tree where pure exploration steps stay within the current state and state-changing actions create child states. This makes the run history easier to navigate and ties actions to context changes.
- The diagnosis module predicts the failure-responsible stage, the error-relevant steps inside that stage, and a compact evidence set that supports the diagnosis.
- The paper also builds CodeTraceBench from executed trajectories across 5 benchmarks, 4 agent frameworks, and 5 model backbones, with stage labels and step-level failure annotations. The benchmark includes a 3.32K full split and a 1.06K verified split.
- Annotation uses backward tracing from the observed failure to the earliest causally responsible step. On a 15% double-annotated subset, Cohen's kappa for the error-critical step label is 0.73.

## Results
- Data scale: the authors collected 7,936 raw trajectories, filtered them to 3,326 for analysis, and report 4,354 standardized and step-level annotated trajectories in the broader benchmark source pool.
- Main localization result on CodeTraceBench: CodeTracer beats Bare LLM and Mini-CodeTracer on step-level failure localization for all tested backbones. For GPT-5, F1 rises from 18.78 (Bare LLM) and 19.33 (Mini-CodeTracer) to 48.02 with CodeTracer, while token use drops from 58.5k and 44.8k to 31.1k.
- For Claude-sonnet-4, CodeTracer reaches 46.57 F1, 40.47 precision, and 54.87 recall at 56.8k tokens, compared with 16.22 F1 for Bare LLM at 105.1k tokens.
- For DeepSeek-V3.2, CodeTracer reaches 46.14 F1 at 44.6k tokens, compared with 16.33 F1 for Bare LLM at 83.4k tokens.
- On hard instances, CodeTracer still keeps a large margin: GPT-5 gets 40.14 F1, Claude-sonnet-4 38.67, and DeepSeek-V3.2 38.72.
- The analysis claims extra iterations help only up to a point. For example, GPT-5 resolved rate rises from 38.69% at 10 iterations to 47.06% at 40 iterations, then stays at 47.06% even at 100 and >=150 iterations, while tokens increase from 106.19k to 266.32k.
- Framework complexity raises cost more than success in their corpus: MiniSWE-Agent has 32.8% success at 44.6k tokens, while OpenHands has 38.3% success at 91.4k tokens and SWE-Agent has 37.5% at 86.7k.
- Their behavioral analysis finds an evidence-to-action gap: ineffective steps rise from 22% in solved runs to 40% in unsolved runs, while correct state changes fall from 30% to 21%.

## Link
- [http://arxiv.org/abs/2604.11641v3](http://arxiv.org/abs/2604.11641v3)
