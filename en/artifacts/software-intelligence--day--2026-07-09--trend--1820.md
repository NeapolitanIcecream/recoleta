---
kind: trend
trend_doc_id: 1820
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
topics:
- agent harnesses
- test-time adaptation
- long-horizon evaluation
- repository verification
- small language models
run_id: materialize-outputs
aliases:
- recoleta-trend-1820
tags:
- recoleta/trend
- topic/agent-harnesses
- topic/test-time-adaptation
- topic/long-horizon-evaluation
- topic/repository-verification
- topic/small-language-models
language_code: en
pass_output_id: 314
pass_kind: trend_synthesis
---

# Executable harnesses now determine agent cost, reliability, and test-time gains

## Overview
Agent performance is increasingly determined by the executable control layer around the model. TTHE improves fixed large language models (LLMs) by editing their harnesses from unlabeled traces, while Long-Horizon-Terminal-Bench shows how quickly current agents break down during sustained terminal work. Repository-wide checks complete the picture: useful agents need adaptive control, dense evaluation, and structural verification.

## Clusters

### Adaptive agent harnesses
The harness is becoming an optimization target. TTHE branches and edits executable control programs using runtime errors, tool outputs, public tests, and other unlabeled traces. With DeepSeek-V4-Flash, it raised BIRD accuracy from 12.0% to 50.0% and SWE-bench Verified from 20.0% to 35.0%. The gains are transductive, and imperfect proxy signals can still cause selection errors.

Automated harness adaptation also changes deployment economics. Across 21 task-model pairs, optimized harnesses improved 16 and closed the small language model (SLM) gap on seven. The best SLM agent reached 89.7% of frontier-LLM performance at 4% of the cost. A separate enterprise study encoded source, routing, output, and trace requirements in code; all 270 model-boundary runs passed those contracts, while a bolt-on guardrail reduced measured utility.

#### Evidence
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): Documents TTHE's trace-driven harness editing, benchmark gains, transductive setup, and proxy-selection limits.
- [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](../Inbox/2026-07-09--better-harnesses-smaller-models-building-90-cheaper-agents-via-automated-harness-adaptation.md): Provides results for automated harness adaptation across business tasks, including cost and performance figures.
- [From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents](../Inbox/2026-07-09--from-prompts-to-contracts-harness-engineering-for-auditable-enterprise-llm-agents.md): Supports code-owned contracts, the 270-run evaluation, and the guardrail utility comparison.

### Long-horizon terminal evaluation
Long-Horizon-Terminal-Bench measures sustained execution with 46 containerized tasks and dense subtask rewards. Runs averaged 9.9 million tokens, 231 episodes, and 85.3 minutes. The strongest tested model solved seven tasks at the 0.95 reward threshold. Across all models, the mean pass rate was 4.3%, and timeouts caused 79% of unresolved runs.

Dense grading exposes useful distinctions within failure. Of 690 runs, 433 earned partial reward, including 180 at or above 0.5. Seventy-three runs were near completion, compared with 30 full passes. This gives developers evidence about progress, stalling, and verification failures that final-state scoring hides.

#### Evidence
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): Contains benchmark scope, resource use, pass rates, partial-reward distribution, and timeout analysis.

### Repository context and structural coherence
Repository-level coding requires context that matches the procedure being implemented. ProjAgent retrieves functions with similar computational steps even when vocabulary and application domains differ, then uses compiler and static-analysis feedback for repair. It reports 41.14% Pass@1 on REPOCOD, though the available evidence does not quantify its margin over retrieval baselines.

Generation also needs repository-wide invariants after code is written. The Patchwork Problem models imports, calls, dependencies, configuration, schemas, resources, control flow, and routing as coordinated graphs. Its study covers 336 generations and validates the failure categories on 43 real-world AI-generated repositories. The paper does not report precision, recall, or a numerical failure rate in the available excerpt, so its strongest supported contribution is the verifier’s scope and taxonomy.

#### Evidence
- [ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation](../Inbox/2026-07-09--projagent-procedural-similarity-retrieval-for-repository-level-code-generation.md): Supports procedural retrieval, static-analysis repair, and the reported REPOCOD result.
- [The Patchwork Problem in LLM-Generated Code](../Inbox/2026-07-09--the-patchwork-problem-in-llm-generated-code.md): Supports the eight repository graph types, evaluation scope, external validation, and reporting limitations.
