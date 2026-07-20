---
source: hn
url: https://codex-resets.com/
published_at: '2026-07-18T23:24:26'
authors:
- denysvitali
topics:
- code-intelligence
- software-production
- usage-monitoring
- developer-tools
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Codex Resets

## Summary
Codex Resets is a monitoring page that records public announcements about Codex usage-limit resets attributed to @thsottiaux. It measures reset frequency and preserves the announcement context, rather than proposing a software or machine-learning method.

## Problem
- Codex users lack a centralized history of when usage limits are reset and why.
- This matters because resets can compensate for outages, billing or metering errors, capacity constraints, promotions, and unusually fast usage growth.

## Approach
- Monitor the relevant public feed and identify announcements that grant or restore Codex limits.
- Preserve the announcements and link each entry to its original post on X.
- Aggregate the records into simple measures: reset count, average interval, and longest interval between resets.

## Results
- The page reports 35 resets, an average interval of 8.9 days, and a longest recorded gap of 67.7 days.
- Its timeline covers the last 26 weeks, according to the displayed dashboard.
- The collected announcements document several concrete causes or contexts, including a cache-hit-rate problem during session compaction, an estimated 9% of Plus and Pro users missing a 2X promotional increase, incidents causing rejected requests or outages, and capacity provisioning for slowdowns.
- The announcements also report Codex growth from 2 million to 3 million weekly users in under a month, followed later by milestones of 7 million, 8 million, and 9 million active users across Codex and ChatGPT Work.

## Link
- [https://codex-resets.com/](https://codex-resets.com/)
