---
source: arxiv
url: https://arxiv.org/abs/2605.26563v1
published_at: '2026-05-26T05:24:37'
authors:
- Minxing Wang
- Xiaofei Xie
- Yintong Huo
topics:
- agentic-coding
- failure-diagnosis
- code-intelligence
- software-maintenance
- llm-agents
- benchmark
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems

## Summary
TrajAudit diagnoses failed repository-level coding-agent runs by finding the earliest step that sent the agent down the wrong path. It combines test-error hints, trajectory filtering, and tool-based inspection to handle long, noisy execution traces.

## Problem
- Coding agents fail on multi-file software maintenance tasks, and developers need to know the first decisive error step so they can fix the agent, prompt, tools, or workflow.
- Existing LLM diagnosis methods read whole trajectories or fixed chunks, so accuracy drops on repository-level traces with 20 to more than 100 steps and observations that can exceed 70% of the content.
- Prior benchmarks understate this difficulty; Who&When averages 22.24 steps and 1,384.11 characters per step, while RootSE averages 50.94 steps and 5,830.71 characters per step.

## Approach
- TrajAudit first uses failed test code and error messages to produce a preliminary diagnosis, including likely failure phases and reasons.
- It compresses trajectory observations through semantic saliency folding: content without failure-related patterns or keywords is replaced with a folded marker, while likely useful code, patches, and error signals stay visible.
- An investigator agent reads the task, the preliminary diagnosis, and the folded trajectory, then calls APIs to inspect hidden observation content only when needed.
- The output is the predicted earliest decisive error step plus a natural-language justification.
- The paper also introduces RootSE, a benchmark with real failed coding-agent trajectories from SWE-agent, OpenHands, and AutoCodeRover on SWE-bench and SWE-bench Pro tasks.

## Results
- On RootSE, TrajAudit beats the strongest existing baseline by more than 24.4 percentage points in localization accuracy.
- TrajAudit uses at least 18% fewer tokens than baselines.
- RootSE contains 93 failed execution instances, more than 4,500 execution steps, and about 27 million characters.
- RootSE task descriptions average 8,223.51 characters, compared with 240.47 for Who&When; RootSE tasks modify 2.9 files on average, compared with 1.7.
- RootSE covers 3 programming languages; Who&When covers 1.
- Annotation quality reports Cohen’s kappa of 0.78 for earliest decisive error step identification, followed by 100% final consensus after arbitration.

## Link
- [https://arxiv.org/abs/2605.26563v1](https://arxiv.org/abs/2605.26563v1)
