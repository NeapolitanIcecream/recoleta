---
source: arxiv
url: https://arxiv.org/abs/2605.30208v1
published_at: '2026-05-28T16:44:07'
authors:
- Chris Adams
- Arjun Singh Banga
- Parveen Bansal
- Souvik Bhattacharya
- Rujin Cao
- Pedro Canahuati
- Nate Cook
- Brian Ellis
- Prabhakar Goyal
- Gurinder Grewal
- Tianyu He
- Matt Labunka
- Alex Manners
- David Molnar
- Ging Cee Ng
- Vishal Parekh
- Jiefu Pei
- Frederic Sagnes
- James Saindon
- Will Shackleton
- Sid Sidhu
- Gursharan Singh
- Karthik Chengayan Sridhar
- Matt Steiner
- Pratibha Udmalpet
- Sean Xia
- Stacey Yan
- Audris Mockus
- Peter Rigby
- Nachiappan Nagappan
topics:
- code-review-automation
- software-foundation-models
- code-intelligence
- ai-generated-code
- developer-productivity
- risk-calibration
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency

## Summary
RADAR automates low-risk code review at Meta by combining source eligibility rules, a Diff Risk Score model, LLM-based code review, and deterministic checks before landing changes.

## Problem
- Meta’s code volume is rising faster than human review capacity: significant lines of code per human-landed diff grew 105.9% year over year, and diffs per developer per month grew 51%.
- Agentic AI accounts for more than 80% of that growth, while the share of diffs reviewed within 24 hours has declined.
- The paper targets routine low-risk diffs so human reviewers can spend time on changes with higher production or design risk.

## Approach
- RADAR classifies each diff by authorship and source: human-authored diffs, deterministic codemods, AI-generated codemods, and RACER runbook diffs.
- Bot diffs pass through ACE, which applies static safety gates, configurable Diff Risk Score thresholds, LLM-based Automated Code Review, and final validation before landing.
- Human-authored diffs pass through RADAR Verification and RADAR Approval, using author eligibility, scope exclusions, content blocklists, Diff Risk Score, and LLM review.
- Diff Risk Score thresholds control risk appetite: examples include P5 for default human-authored diffs, P20 for stricter bot sources, and P50 for allowlisted RACER runbooks.
- RACER runbooks also use 60-day risk history checks, daily landing caps, and denylists for sources with incidents or sensitive targets.

## Results
- RADAR reviewed more than 535K diffs and landed more than 331K diffs in production at Meta.
- The system reached more than 25K diffs per day.
- Relaxing the Diff Risk Score threshold from the 25th percentile to the 50th percentile raised the approve rate to 60.31%.
- RADAR-reviewed diffs had a revert rate one-third that of non-RADAR diffs.
- RADAR-reviewed diffs had a Production Incident rate one-fiftieth that of non-RADAR diffs.
- Compared with human-reviewed diffs, the paper states that RADAR reduces median time to close by over 330% and median diff review wall time by 35%.

## Link
- [https://arxiv.org/abs/2605.30208v1](https://arxiv.org/abs/2605.30208v1)
