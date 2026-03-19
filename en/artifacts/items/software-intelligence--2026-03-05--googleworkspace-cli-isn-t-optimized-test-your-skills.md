---
source: hn
url: https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7
published_at: '2026-03-05T23:34:24'
authors:
- sjmaplesec
topics:
- cli-evaluation
- agent-tool-use
- schema-guided-execution
- google-workspace
- benchmarking
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Googleworkspace/CLI isn't optimized – Test your skills

## Summary
This is not a traditional paper, but an evaluation results page for Google Workspace CLI usage skills. It shows how providing an agent with a specific “skill/context tile” changes the success rate, cost, and latency of related CLI tasks. The core conclusion is: injecting structured operational knowledge into the agent can significantly improve task completion rates, and for some tasks reduce tokens, time, and cost.

## Problem
- The problem being addressed is that agents using Google Workspace/CLI often fail because they do not understand the correct command syntax, parameter construction, safety practices, and output formatting.
- This matters because automated software production and agent execution depend on stable, reproducible tool calls; mistakes in CLI details can directly cause task failure, leakage risk, or costly repeated trial and error.
- The page focuses in particular on common mistakes in real operations, such as resource syntax, flag usage, dry-run safety workflows, pagination and formatting, authentication, and PII/secret handling.

## Approach
- The core method is to provide the agent with a Google Workspace CLI “skill tile/context package” that explicitly encodes the correct practices, and then compare performance against a baseline without that context.
- This tile appears to center on **schema-first API inspection**: first inspect the schema/help documentation, then construct commands, resource paths, and flags according to the schema.
- It also turns operational norms into executable guidance, including: correct CLI resource syntax, parameter flag usage, the JSON usage of `batchUpdate`, output controls such as `--format`/`--page-all`, safe dry-runs, confirmation steps, and avoiding outputting secrets.
- The evaluation method measures success rates for each skill point in “with context vs without context,” while also recording cost, duration, number of turns, and token usage, thereby quantifying the benefit of the context package for agent execution.

## Results
- Overall, after using the tile, the **agent success rate was 81%**, improving from the baseline **45%** to **1.8x**.
- In **Schema-first API inspection**, multiple capabilities jumped from low baselines to perfect scores: schema inspection **15% → 100%**, correct CLI resource syntax **0% → 100%**, params flag used **0% → 100%**, schema-driven flag construction **13% → 100%**; the task’s cost/latency dropped from **$1.1610, 3m41s, 50 turns, 10,517 output tokens** to **$0.2663, 53s, 15 turns, 2,860 output tokens**.
- In **Plain text vs rich text appending**, multiple items stayed at or reached **100%**: `+write for plain text`, `batchUpdate for table`, correct `+write` flags, `batchUpdate uses --json`, reason for split documented, and no hardcoded credentials; however, **confirmation before write remained 0% → 0%**. Cost/latency dropped from **$0.6478, 3m33s, 22 turns** to **$0.4307, 1m12s, 24 turns**, and output tokens fell from **9,860 → 4,099**.
- In **Batch update safety with dry-run**, dry-run preview pass improved **22% → 100%**, correct `batchUpdate` syntax **0% → 100%**, runbook dry-run explanation **27% → 100%**, and loops over all IDs plus no secrets exposed stayed at **100%**; however, **user confirmation before live run was 0% → 0%**. This category instead became more expensive with context: **$0.2168 → $0.3692**, duration **1m04s → 1m42s**, output tokens **3,510 → 6,201**.
- In **Output formatting and pagination**, the `--format` flag improved **0% → 100%**, `--page-all` **0% → 100%**, FORMAT argument controls `--format` **0% → 100%**, pagination flags documented **0% → 100%**, and output filename matches format remained **100%**; however, the `--output` flag for file saving stayed **0% → 0%**. This category saw higher cost/input tokens: **$0.2705 → $0.4985**, duration **1m10s → 1m34s**, input tokens **12 → 6,290**.
- In **Service account auth and PII screening**, safety-related capabilities improved with context but not consistently: no credential values output **90% → 100%**, sanitize explained in setup guide **16% → 100%**; however, the `GOOGLE_APPLICATION_CREDENTIALS` env var degraded **72% → 22%**, and the `--sanitize` flag on get **0% → 0%** remained unresolved. Cost rose from **$0.2651 → $0.4179**, while duration changed from **1m32s → 1m14s**.

## Link
- [https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7](https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7)
