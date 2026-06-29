---
source: arxiv
url: https://arxiv.org/abs/2605.09573v1
published_at: '2026-05-10T14:37:20'
authors:
- Yuandao Cai
- Shuhao Fu
- Wensheng Tang
- Cheng Wen
- Shengchao Qin
- Charles Zhang
topics:
- concurrency-testing
- llm-agents
- test-generation
- code-intelligence
- static-analysis
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing

## Summary
ConCovUp generates multi-threaded C/C++ test drivers that reach shared-memory access pairs for concurrency testing. It combines static shared-access analysis, LLM-based backward path reasoning, and execution feedback.

## Problem
- Dynamic race and concurrency analyzers such as ThreadSanitizer need tests that create real shared-memory interactions across threads.
- Existing unit tests and LLM coding agents mostly target sequential behavior, so they miss write-read, read-write, and write-write interactions inside libraries.
- The gap matters because open-source libraries may be treated as thread-safe while their internal synchronization paths receive little concurrent execution.

## Approach
- The Analysis Agent uses whole-program static analysis to find public entry functions, shared variables, shared memory access locations, and conflicting access pairs.
- The Path Agent starts from each target access and traces backward through the control-flow graph to infer what inputs and object states can reach that access.
- Instead of sending constraints to an SMT solver, the system asks the LLM to read path summaries and choose concrete inputs, such as a new key versus an existing key in the hash-map example.
- The Test Generation Agent writes multi-threaded test drivers, compiles and runs them, then sends uncovered access pairs and failures back for another path search.
- The paper sets the refinement budget to 3 iterations per test in the reported experiments.

## Results
- On 9 real-world C/C++ libraries totaling about 1,000 kLoC, ConCovUp raises average Shared Memory Access Pair Coverage from 36.6% with a Claude Code agent baseline to 68.1%.
- In the ablation study, static target identification alone reaches 39.2% average SMAP Coverage, while the full system reaches 68.1%.
- Model choice changes coverage: Claude Sonnet 4.6 reaches 68.1%, GPT 5.4 reaches 55.9%, and Kimi K2.5 reaches 28.1% average SMAP Coverage.
- The paper’s main measured gain is coverage of conflicting shared-memory access pairs; the excerpt does not report a count of new bugs or races found.

## Link
- [https://arxiv.org/abs/2605.09573v1](https://arxiv.org/abs/2605.09573v1)
