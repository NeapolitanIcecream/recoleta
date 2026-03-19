---
source: arxiv
url: http://arxiv.org/abs/2603.08616v1
published_at: '2026-03-09T16:59:30'
authors:
- Nils Loose
- Nico Winkel
- Kristoffer Hempel
- "Felix M\xE4chtle"
- Julian Hans
- Thomas Eisenbarth
topics:
- software-fuzzing
- java-testing
- llm-agents
- coverage-guided-testing
- program-analysis
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing

## Summary
This paper presents a **multi-agent LLM system for automatic Java library fuzzing harness generation**. It generates, repairs, and iteratively improves harnesses by querying documentation, source code, and call graphs on demand. Its core contribution is making coverage feedback “target-method-directed” and letting agents decide when to continue optimization and when to stop, thereby achieving higher coverage and real bug discovery than existing baselines.

## Problem
- The paper addresses the problem that **Java library fuzzing requires high-quality harnesses, but writing them manually is slow and heavily depends on understanding API semantics, initialization order, and exception contracts**.
- This matters because without suitable harnesses, coverage-guided fuzzing has difficulty truly reaching deep into library code, leaving many widely deployed Java libraries insufficiently tested.
- Existing automated methods either rely on large amounts of client code, only examine type structure, or use only fixed thresholds for feedback, making them poorly suited to handling implicit preconditions, complex initialization, and semantic judgment of coverage gaps.

## Approach
- The core method is a **five-agent ReAct pipeline**: Research handles understanding the target API, Generation creates the initial harness, Patching fixes compilation errors, Coverage Analysis analyzes coverage gaps, and Refinement iteratively modifies the harness.
- Instead of stuffing the entire codebase into context at once, the system uses **MCP for on-demand queries** to Javadoc, source indexes, and static call graphs, retrieving only information relevant to the current task and avoiding context explosion.
- One key mechanism is **method-targeted coverage**: JaCoCo recording is enabled only during execution of the target method, preventing the harness from “inflating” coverage by running unrelated initialization code.
- Another key mechanism is **agent-guided termination**: the coverage-analysis agent inspects uncovered source code and judges whether those gaps can be addressed through better inputs or call sequences, or are inherently difficult to reach, thereby deciding whether to continue refinement or stop.
- At the simplest level, the system works like this: **first study the API, then write the harness, fix it if it does not compile, run fuzzing to see what remains uncovered, then revise the harness in a targeted way, until further changes are no longer worthwhile**.

## Results
- The method is evaluated on **7 target methods across 6 widely deployed Java libraries**, which together have **115,000+ Maven dependents**.
- Relative to existing **OSS-Fuzz** harnesses, the generated harnesses achieve a **median 26% improvement** in **method-targeted coverage**.
- Under **full package-scope coverage**, the method outperforms **OSS-Fuzz by 6%** and **Jazzer AutoFuzz by 5%** (median).
- Generation cost is low: on average each harness takes **about 10 minutes** and **about $3.20**, suggesting it is practical for continuous fuzzing workflows.
- In a **12-hour fuzzing campaign**, the generated harnesses found **3 previously unreported bugs** in projects already integrated into OSS-Fuzz.
- The paper also notes one example that did not surpass the baseline: **jackson-databind**, because the OSS-Fuzz baseline harness included additional fuzzing logic after the target method, resulting in higher overall coverage.

## Link
- [http://arxiv.org/abs/2603.08616v1](http://arxiv.org/abs/2603.08616v1)
