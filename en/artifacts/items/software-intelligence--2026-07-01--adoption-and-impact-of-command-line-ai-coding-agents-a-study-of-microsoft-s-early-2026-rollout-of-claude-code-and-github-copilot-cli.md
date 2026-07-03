---
source: arxiv
url: https://arxiv.org/abs/2607.01418v1
published_at: '2026-07-01T19:24:27'
authors:
- Emerson Murphy-Hill
- Jenna Butler
- Alexandra Savelieva
topics:
- command-line-agents
- code-intelligence
- developer-productivity
- ai-tool-adoption
- software-engineering-telemetry
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Adoption and Impact of Command-Line AI Coding Agents: A Study of Microsoft's Early 2026 Rollout of Claude Code and GitHub Copilot CLI

## Summary
This paper studies Microsoft’s early-2026 rollout of Claude Code and GitHub Copilot CLI using developer telemetry. It finds that peer exposure predicts trial, coding activity predicts retention, and adopters merged about 24% more pull requests than their estimated counterfactual.

## Problem
- Organizations need to know which engineers will try command-line AI coding agents, which engineers will keep using them, and whether the tools change shipped output.
- This matters because token costs can reach millions of dollars per year at large companies, while a merged pull request is only a proxy for delivered value.
- Prior work often used surveys, lab tasks, public-repository signals, or IDE-tool data; this study uses Microsoft telemetry for engineers who could adopt sanctioned CLI agents.

## Approach
- The adoption study tracks Copilot CLI first use and retention among eligible Microsoft software engineers from January 5 to April 29, 2026, with predictors from HR data, prior pull-request activity, prior IDE Copilot use, and social exposure.
- Initial use is modeled with discrete-time logistic regression on engineer-week rows; retention is modeled as use on at least 5 of the first 14 days after first use.
- Social exposure is measured through reviewer peers, skip-level peers, and direct managers who used Copilot CLI in the prior 14 days.
- The outcomes study covers both Claude Code and Copilot CLI and uses merged pull requests within 28 days of creation as the output measure.
- Impact is estimated with a CausalImpact synthetic-control counterfactual and a within-person dose-response design that compares weeks with different tool-use intensity for the same engineer.

## Results
- Adopters merged roughly 24% more pull requests than they would have otherwise, and the lift persisted across the four-month observation window.
- Social exposure had the largest adoption association: engineers with more than 25% of skip-level peers using Copilot CLI had +216% higher odds of trying it and +66% higher odds of retention; direct-manager use was linked to +82% higher trial odds and +22% higher retention odds.
- Reviewer-peer exposure also mattered: when at least 25% of reviewer peers used Copilot CLI, trial odds were +54% higher than for engineers with no exposed reviewer peers.
- Prior IDE Copilot use predicted trial but weaker retention: prior use was linked to +49% to +83% higher odds of trying Copilot CLI, while retention odds were lower by about 12% to 15%.
- Baseline coding activity predicted retention: engineers who previously created 2 or more PRs per week had +34% higher odds of trying Copilot CLI and +31% higher odds of retention than engineers with no pre-period PRs.
- Career and tenure effects were smaller: IC2 and IC3 engineers had about 13% to 14% lower trial odds than IC4 engineers, IC5 engineers had about +22% higher trial odds, and first-year Microsoft engineers had +11% higher trial odds than the 5-to-15-year tenure group.

## Link
- [https://arxiv.org/abs/2607.01418v1](https://arxiv.org/abs/2607.01418v1)
