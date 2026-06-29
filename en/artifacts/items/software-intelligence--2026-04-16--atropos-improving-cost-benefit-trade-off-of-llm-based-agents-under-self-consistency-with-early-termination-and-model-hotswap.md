---
source: arxiv
url: http://arxiv.org/abs/2604.15075v1
published_at: '2026-04-16T14:39:36'
authors:
- Naryeong Kim
- Shin Yoo
topics:
- llm-agents
- software-engineering
- early-termination
- model-hotswap
- self-consistency
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Atropos: Improving Cost-Benefit Trade-off of LLM-based Agents under Self-Consistency with Early Termination and Model Hotswap

## Summary
Atropos cuts the cost of self-consistent LLM agents by predicting mid-run failures and switching those runs from a cheap small model to a stronger large model. It targets software engineering agents where multiple sampled trajectories improve quality but make inference expensive.

## Problem
- Self-consistency runs the same agent multiple times and votes over the outputs, which raises token, tool, and model cost.
- Open-weight small language models are cheaper and faster, but they fail more often than stronger proprietary models on software engineering agents.
- Without an early signal, users only learn that an SLM run failed after paying for the whole trajectory, so the cost-quality trade-off stays poor.

## Approach
- Atropos merges the agent's multiple sampled trajectories into a **Semantic Flow Graph** where nodes are reasoning or tool-use steps and edges track how often steps follow each other.
- It trains a **3-layer Graph Convolutional Network** to classify a partial graph as likely success or likely failure before the full inference finishes.
- For AutoFL and AutoCodeRover, nodes encode tool calls plus structured arguments; for RepairAgent, semantically similar unstructured steps are clustered with FastText embeddings and cosine-similarity thresholds.
- When the partial run is predicted to fail on the source SLM, Atropos either stops early to save cost or **hotswaps** to a stronger target LLM by replaying the current context, using the fact that LLM query contexts are stateless.
- The paper studies both **parallel** truncation/hotswap across all sampled trajectories and **sequential** truncation/hotswap across completed runs.

## Results
- At the midpoint of inference, Atropos predicts eventual failure with accuracy up to **0.85** and **AUROC 0.85**.
- The paper also reports a technical contribution figure of **85.4% accuracy** and **85.45% AUROC** for midpoint prediction of incorrect outcomes.
- Hotswapping salvages up to **27.57%** of runs that would have failed if they had stayed on the small model.
- Relative to closed proprietary LLM runs, Atropos reaches **74.35%** of their performance at only **23.90%** of the monetary cost.
- Framed the other way in the paper, Atropos cuts monetary cost by up to **76.1%** versus proprietary LLMs while keeping **74.35%** of their performance.
- Evaluation covers three software engineering agents: **AutoFL**, **AutoCodeRover**, and **RepairAgent**, under self-consistency with **10 samples**.

## Link
- [http://arxiv.org/abs/2604.15075v1](http://arxiv.org/abs/2604.15075v1)
