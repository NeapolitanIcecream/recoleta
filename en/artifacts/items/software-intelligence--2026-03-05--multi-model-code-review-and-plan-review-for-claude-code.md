---
source: hn
url: https://github.com/AltimateAI/claude-consensus
published_at: '2026-03-05T23:38:46'
authors:
- aaur0
topics:
- code-review
- multi-model-consensus
- claude-code
- plan-review
- developer-tools
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Multi-model code review and plan review for Claude Code

## Summary
This is a multi-model code review and plan review plugin for Claude Code. It lets multiple AI models first review independently, then form consensus through structured synthesis and up to two rounds of convergence. It aims to improve the instability and bias issues of single-model review, while supporting practical development workflows with a relatively low configuration barrier.

## Problem
- It addresses the problem of over-reliance on a single model in code review and implementation plan review; a single model may miss defects, make one-sided judgments, or produce unstable output, which affects software engineering quality.
- This problem matters because code review and design review directly affect defect discovery, implementation quality, and team trust in AI-assisted development.
- It also addresses the engineering implementation challenge of multi-model collaboration: how to organize multiple models in Claude Code to complete reviews together in a configurable, degradable, and operable way.

## Approach
- The core mechanism is simple: have Claude and multiple external models review the same code or plan **independently in parallel**, avoiding cross-contamination of opinions between models.
- Then it enters the **structured synthesis** stage, summarizing consensus points, conflict points, and comparison tables to form a unified view.
- Finally, it proceeds to the **convergence/approval** stage, outputting `APPROVE` or `CHANGES NEEDED`, with at most 2 rounds.
- The system supports configurable arbitration conditions, including which models are enabled, the minimum quorum, command-line integration methods, and graceful degradation for models unavailable at runtime.
- In the minimum configuration, only Claude + 1 external model is needed; in the full configuration, the README mentions that users can choose from 7 external models to enable.

## Results
- The text **does not provide standard benchmark tests or quantitative experimental results**; it does not report numeric improvements on specific datasets, defect detection rate, accuracy, recall, or human review time.
- The most specific mechanistic result given is that the review process is divided into **3 stages** (independent review, synthesis, convergence), and the convergence stage allows **up to 2 rounds**.
- The default quorum is **5**, requiring a **strict majority response** among participants for a valid review; it also supports skipping unavailable models at runtime as long as quorum is still satisfied.
- The minimum usable setup is **Claude + 1 external model**; the configuration interface states that users can choose from **7 external models** to enable.
- The paper/README’s strongest claim is that multi-model independent review plus consensus synthesis can provide more robust code review and plan review than a single-model approach, but it does not provide quantified comparative evidence.

## Link
- [https://github.com/AltimateAI/claude-consensus](https://github.com/AltimateAI/claude-consensus)
