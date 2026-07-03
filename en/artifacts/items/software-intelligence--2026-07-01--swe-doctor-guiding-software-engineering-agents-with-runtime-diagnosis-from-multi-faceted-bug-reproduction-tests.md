---
source: arxiv
url: https://arxiv.org/abs/2607.00990v1
published_at: '2026-07-01T14:27:12'
authors:
- Yaoqi Guo
- Yang Liu
- Jie M. Zhang
- Yun Ma
- Yiling Lou
- Zhenpeng Chen
topics:
- software-agents
- code-intelligence
- bug-fixing
- swe-bench
- runtime-debugging
- test-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Multi-Faceted Bug Reproduction Tests

## Summary
SWE-Doctor is a bug-fixing agent that uses generated reproduction tests as debugging probes before patch generation. It reports higher SWE-bench resolution rates by generating tests for multiple issue requirements and turning their executions into runtime diagnosis records.

## Problem
- LLM software agents often use bug reproduction tests only after generating a patch, so tests do not help identify what code to change.
- Directly making generated BRTs pass can hurt patch generation: in a 100-issue SWE-bench Verified study, mini-SWE-agent resolved 74 issues, while variants with e-Otter++, Issue2Test, and AssertFlip resolved 71, 71, and 73.
- Single fail-to-pass tests may cover one behavior and lead to partial fixes; fail-to-fail tests can point the agent at invalid targets.

## Approach
- Extract expected behaviors from the issue report, treat each behavior as a separate facet, and generate a targeted bug reproduction test for each facet.
- Localize likely files and functions for each requirement using identifier matches plus LLM-based localization, then run a generate-execute-refine loop until the test fails for the intended behavior.
- Run the generated tests under a debugger and create diagnosis records with suspected fault locations, failure symptoms, propagation paths, runtime values, patch impact notes, and suggested fixes.
- Feed requirements, localization data, and diagnosis records into mini-SWE-agent before patch generation, then run a completeness check before submission.

## Results
- The main evaluation covers Python bug-fixing tasks on SWE-bench Verified and SWE-bench Pro across 5 LLM backends, giving 10 LLM-benchmark combinations.
- SWE-Doctor reports average resolution rates of 75.7% on SWE-bench Verified and 59.4% on SWE-bench Pro.
- On SWE-bench Pro, it improves average resolution by 8.0 to 8.9 percentage points over mini-SWE-agent and live-SWE-agent.
- It beats both baseline agents across all 10 LLM-benchmark combinations.
- In the preliminary 100-issue study, e-Otter++ resolved 71/100 issues with 50 fail-to-pass and 50 fail-to-fail tests; Issue2Test resolved 71/100 with 42 fail-to-pass and 58 fail-to-fail tests; AssertFlip resolved 73/100 with 70 fail-to-pass and 30 fail-to-fail tests; original mini-SWE-agent resolved 74/100.
- The paper says removing either multi-faceted test generation or runtime-grounded diagnosis lowers resolution, but the excerpt does not provide the ablation rates.

## Link
- [https://arxiv.org/abs/2607.00990v1](https://arxiv.org/abs/2607.00990v1)
