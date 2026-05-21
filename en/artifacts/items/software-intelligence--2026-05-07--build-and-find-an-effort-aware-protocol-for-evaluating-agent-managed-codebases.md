---
source: arxiv
url: https://arxiv.org/abs/2605.06136v1
published_at: '2026-05-07T12:35:27'
authors:
- Jhen-Ke Lin
topics:
- code-intelligence
- coding-agents
- agent-evaluation
- multi-agent-software-engineering
- repository-understanding
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# BUILD-AND-FIND: An Effort-Aware Protocol for Evaluating Agent-Managed Codebases

## Summary
Build-and-Find evaluates whether a codebase written by one agent makes its intended behavior and design choices recoverable by later agents, and how much repository inspection that recovery costs.

## Problem
- Standard coding-agent benchmarks mainly test whether code passes behavioral checks, while agent-managed repositories also need to communicate design intent to later agents.
- A repository can behave correctly yet force a downstream agent to spend extra effort finding why features, configuration, or structure were chosen.
- This matters for multi-agent software work because later agents may audit, extend, or modify code using the generated repository as their main context.

## Approach
- A builder agent sees a hidden repository specification and creates a self-contained codebase.
- A finder agent sees only the generated codebase and a specification-traced multiple-choice question bank, then answers questions about intended behavior and design choices.
- The protocol reports audited recovery accuracy, all-correct rates, repeatability, builder implementation coverage, and novel agent inspection bytes.
- Effort is interpreted only after recovery and stability checks, so low inspection cost does not count as good evidence when answers are unreliable.
- Controls include question-only, spec-only, compile-failed, low-prior, evidence-audit, and builder-finder affinity analyses.

## Results
- The released study uses 2 repository task families, 15 questions per task, 48 builds, 1,728 artifact-conditioned find records, and 25,920 raw question rows; the compile-pass primary panel has 41 builds, 1,476 find records, and 21,312 scored finder-answer rows.
- Question-only accuracy is 94.5%, spec-only accuracy is 99.9%, and compile-pass artifact-conditioned recovery is 98.9%, a +4.4 percentage-point lift over question-only.
- Repeatability is higher with artifacts than with question-only controls: formal artifact-conditioned 3-trial agreement is 97.5% and reliable questions are 96.7%, compared with 86.7% and 66.7% for question-only.
- Builder-side implementation coverage ranges from 85.0% to 100.0%, with four builders at 100.0%; downstream recovery on implemented-gold claims is 97.3% to 99.5%.
- On the low-prior subset, question-only accuracy is 88.9% and artifact-conditioned recovery is 97.9%, a +9.0 percentage-point lift; scratch_minidb rises from 90.0% to 96.8%, and scratch_nanoweb rises from 87.8% to 98.9%.
- Conditional effort ranks GPT-5.5 artifacts as low-cost full-coverage examples, with R_b = 1.033 in the high-effort panel and R_b = 1.151 for GPT-5.5-low; GPT-5.4-mini-high is second in the high-effort panel with R_b = 1.320.

## Link
- [https://arxiv.org/abs/2605.06136v1](https://arxiv.org/abs/2605.06136v1)
