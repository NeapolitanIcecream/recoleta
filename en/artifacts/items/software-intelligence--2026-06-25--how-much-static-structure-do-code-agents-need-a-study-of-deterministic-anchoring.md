---
source: arxiv
url: https://arxiv.org/abs/2606.26979v1
published_at: '2026-06-25T12:50:01'
authors:
- Zhihao Lin
- Mingyi Zhou
- Yizhuo Yang
- Li Li
topics:
- code-agents
- static-analysis
- fault-localization
- repository-navigation
- swe-bench
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# How Much Static Structure Do Code Agents Need? A Study of Deterministic Anchoring

## Summary
CodeAnchor adds static program links to grep-first code agents as plain-text comments. The paper claims these comments make repository navigation more accurate, shorter, and more repeatable without changing the agent loop.

## Problem
- Grep-first code agents miss call graphs, inheritance, imports, configuration use, and data-flow links, so they often stop at nearby text matches instead of the function that needs work.
- This matters because two runs on the same issue can visit different files and produce different outcomes, which makes failures hard to inspect and reproduce.
- The paper studies how much static structure helps when the baseline is already strong: Codex reaches 83.2% Func@5 on SWE-bench Lite, compared with 59.5% for the graph-based LocAgent under the reported matched setup.

## Approach
- CodeAnchor runs lightweight static analysis offline, then inserts the discovered facts next to functions, classes, files, and configuration entries as normal comments.
- The agent still uses ordinary text search and file reads. When it opens code, the nearby comments show links such as CALLS, CALLED_BY, IMPORTS, BASE, DERIVED, CONFIG_USAGE, DATA_DEP, IO_DEP, and TEST_REF.
- The paper compares raw grep with Anchor-Topo, Anchor-Dense, and Anchor-Inv. Anchor-Topo adds call, inheritance, import, and containment links; Anchor-Dense adds config and data-flow hints; Anchor-Inv keeps inverse links such as CALLED_BY while dropping forward links.
- The Python prototype uses PyCG for call graphs and AST passes for imports, containment, inheritance, config use, constants, I/O, and test links.

## Results
- On SWE-bench Lite, lightweight topology improves function localization by +2.2 percentage points on Func@5 and shortens navigation by 1.6 interaction rounds.
- Tags increase structural link-following from 0.15-0.18 to 0.21-0.24 and roughly halve run-to-run variance in the reported stability study.
- On medium-scale repositories, the paper reports a +3.4 percentage point Pass@1 gain for single-run reliability.
- The added comments cost about 9.9% more input tokens on SWE-bench Lite, described as roughly 10% in the abstract.
- Static graph construction times are 6.8s for pytest-7432 at 73k LOC, 21.1s for sklearn-15512 at 247k LOC, 58.4s for astropy-12907 at 341k LOC, and 133.4s for django-13658 at 367k LOC.
- The paper reports that inverse-only links help hub-heavy repositories, while dense tags have diminishing returns unless the task depends on implicit configuration or data-flow links.

## Link
- [https://arxiv.org/abs/2606.26979v1](https://arxiv.org/abs/2606.26979v1)
