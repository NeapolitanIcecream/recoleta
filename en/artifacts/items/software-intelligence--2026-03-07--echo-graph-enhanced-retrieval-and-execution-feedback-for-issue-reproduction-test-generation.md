---
source: arxiv
url: http://arxiv.org/abs/2603.07326v1
published_at: '2026-03-07T20:11:30'
authors:
- Zhiwei Fei
- Yue Pan
- Federica Sarro
- Jidong Ge
- Marc Liu
- Vincent Ng
- He Ye
topics:
- issue-reproduction
- test-generation
- code-retrieval
- execution-feedback
- code-graph
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Echo: Graph-Enhanced Retrieval and Execution Feedback for Issue Reproduction Test Generation

## Summary
Echo is an agent for automatically generating issue-reproducing tests for software issues, focused on solving the problems of “how to find the right code context, actually run the tests, and reliably determine whether reproduction succeeded.” It combines code-graph retrieval, automatic execution, and patch-version-based fail-to-pass validation, and reports a new open-source SOTA on SWT-Bench Verified.

## Problem
- Many bug reports lack executable reproduction tests, so developers must manually understand the codebase and fill in environment and test-framework details, which is costly and time-consuming.
- Existing methods often rely on weak file-level retrieval or preset execution commands, making it difficult to accurately find relevant code/tests in real repositories and to execute generated tests reliably.
- Relying only on LLM semantic judgment to decide whether a test “really reproduces the problem” is unreliable; the more important criterion is that the test fails on the buggy version and passes on the patched version (fail-to-pass).

## Approach
- Construct the repository as a heterogeneous code graph (files, AST nodes, text fragments, and their relationships), and perform multi-strategy retrieval based on Neo4j to obtain focal code and related regression tests.
- Introduce automatic query refinement: the LLM first evaluates whether the current retrieval results are sufficient, then iteratively rewrites the query for missing information, improving the precision and compactness of the context.
- During test generation, feed the issue description, retrieved focal code, related test examples, and candidate patches into the LLM, requiring it to produce a single standalone, minimal issue-reproducing test file that matches the project style.
- Automatically infer and execute the repository-specific command for that test, but strictly limit it to read-only behavior, running only the generated test file, not modifying the repository, and not running the full test suite, in order to obtain usable execution feedback.
- Use candidate patches to construct a patched version and perform a rule-based dual-version check: if the test fails on the original version and passes on the patched version, it is considered successful; otherwise, the logs are fed back to the generator for further iteration, with at most two retries.

## Results
- On **SWT-Bench Verified**, Echo reports a **66.28% success rate**, which the paper describes as a **new SOTA among open-source methods**.
- Compared with many methods that first generate and rank multiple candidate tests, Echo chooses to **focus on generating only 1 test per issue and iteratively improving it**, arguing that this offers a better **cost-performance trade-off**.
- The paper explicitly claims that its automatic execution of generated tests is a **first-of-its-kind feature**, emphasizing that this capability is closer to real development workflows.
- The core quantitative result given in the text is mainly **66.28%**; the current excerpt does not provide more detailed baseline comparison numbers, ablation gains, or cost figures.

## Link
- [http://arxiv.org/abs/2603.07326v1](http://arxiv.org/abs/2603.07326v1)
