---
source: hn
url: https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7
published_at: '2026-03-05T23:34:24'
authors:
- sjmaplesec
topics:
- cli-evaluation
- tool-use
- prompt-context
- safety
- google-workspace
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Googleworkspace/CLI isn't optimized – Test your skills

## Summary
This is not a traditional academic paper, but rather a summary of evaluation results for Google Workspace CLI usage skills, showing how an agent’s success rate and efficiency change on a set of CLI skill tasks after being given a specific “tile/context.” The core conclusion is: structured context can significantly improve task success rates, and on several key operations can raise accuracy from near 0% to 100%.

## Problem
- The problem this work aims to solve is: when using Google Workspace/CLI, agents often make mistakes in details such as **resource syntax, parameter construction, safety procedures, and output formatting**, leading to low task success rates.
- This matters because in enterprise automation scenarios, misuse of the CLI not only reduces efficiency, but can also introduce security and compliance risks such as **incorrect writes, credential leakage, and PII exposure**.
- The text also implicitly examines a practical question: whether providing agents with appropriate structured operational context can significantly improve their real-world tool-use capability and cost efficiency.

## Approach
- The core method is simple: on a set of Google Workspace CLI skill evaluation tasks, compare agent performance under two settings: **without context** and **with a specific tile/context**.
- These context/tile assets appear to provide task-relevant operating guidance, such as **schema-first API inspection, flag construction rules, dry-run safety procedures, formatting and pagination parameters, and authentication and sanitization requirements**.
- The evaluation is broken down by skill dimension, checking whether the agent does things such as: using correct CLI resource syntax, using correct flags, doing a dry-run before a live run, using `--format`/`--page-all`, and not outputting secrets.
- In addition to success rate, it also reports execution cost, elapsed time, number of dialogue turns, and token usage to measure whether context also improves efficiency.

## Results
- Overall, after using the tile, the agent success rate reached **81%**, a **1.8x** improvement over the **45%** baseline.
- In **Schema-first API inspection**, several capabilities jumped from low levels to full marks: `Correct CLI resource syntax` **0% → 100%**, `Params flag used` **0% → 100%**, `Schema-driven flag construction` **13% → 100%**; meanwhile, this group’s cost/latency dropped from **$1.1610 / 3m41s / 50 turns / 10,517 output tokens** to **$0.2663 / 53s / 15 turns / 2,860 output tokens**.
- In **Plain text vs rich text appending**, multiple sub-items remained at **100%**, but `Confirmation before write` was still **0% → 0%**; this group’s cost fell from **$0.6478** to **$0.4307**, time from **3m33s** to **1m12s**, and output tokens from **9,860** to **4,099**.
- In **Batch update safety with dry-run**, `Dry-run preview pass` improved **22% → 100%**, `Correct batchUpdate syntax` **0% → 100%**, and `Runbook dry-run explanation` **27% → 100%**, but `User confirmation before live run` remained **0% → 0%**.
- In **Output formatting and pagination**, `--format flag used` improved **0% → 100%**, `--page-all flag present` **0% → 100%**, `FORMAT argument controls --format` **0% → 100%**, and `Pagination flags documented` **0% → 100%**, but `--output flag for file saving` remained **0% → 0%**.
- In **Service account auth and PII screening**, the results were mixed: `Sanitize explained in setup guide` **16% → 100%**, `No credential values output` **90% → 100%**, but `GOOGLE_APPLICATION_CREDENTIALS env var` declined **72% → 22%**, while `--sanitize flag on get` stayed **0% → 0%**.

## Link
- [https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7](https://tessl.io/eval-runs/019cc02f-bb26-76e0-a7c9-598a7337edb7)
