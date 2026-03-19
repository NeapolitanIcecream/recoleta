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
- multi-agent-systems
- llm-code-generation
- fuzzing
- java-testing
- coverage-guided-testing
- program-analysis
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Coverage-Guided Multi-Agent Harness Generation for Java Library Fuzzing

## Summary
This paper presents a multi-agent LLM system for fuzz testing Java libraries that can automatically generate and iteratively improve fuzz harnesses. Its key ideas are querying program information on demand, using method-targeted coverage as feedback, and achieving performance that matches or exceeds existing baselines at low cost.

## Problem
- It addresses the problem of **automatic Java library fuzz harness generation**: for library code to be effectively tested by coverage-guided fuzzing, random bytes must first be translated into valid API calls, but writing harnesses manually is time-consuming and requires understanding API semantics, initialization order, and exception contracts.
- This matters because the lack of high-quality harnesses directly limits code coverage and bug-finding ability for libraries; meanwhile, Java libraries remain relatively under-covered in continuous fuzzing infrastructure despite being widely deployed in practice.
- Existing methods either rely on large amounts of client code, or look only at type structure and fail to capture implicit preconditions, or lack semantic explanations for coverage gaps, leading to weak generalization and limited iterative improvement capability.

## Approach
- The core method is a **five-agent ReAct pipeline**: Research, Generation, Patching, Coverage Analysis, and Refinement, each responsible for investigating APIs, generating harnesses, fixing compilation errors, analyzing coverage gaps, and iteratively optimizing the harness.
- Put simply: the system first “consults documentation and source code to understand the API,” then “writes a compilable harness,” then “runs fuzzing to see which target code was not reached,” and finally “continues improving the harness based on the uncovered source code.”
- Rather than stuffing the entire codebase into the prompt in advance, it uses **MCP** to query Javadoc, source code, and call graphs on demand, avoiding context explosion and allowing different agents to access only the tools relevant to their roles.
- The paper proposes **method-targeted coverage**: coverage is recorded only during execution of the target method, preventing the harness from “inflating” coverage metrics by calling unrelated initialization or utility code, so the feedback better reflects the target API itself.
- It also proposes **agent-guided termination**: the coverage analysis agent reads uncovered source code and determines whether the gaps can be addressed through more input or path exploration, or whether the process has entered diminishing returns, thereby deciding whether to stop refinement.

## Results
- The approach was evaluated on **7 target methods from 6 widely used Java libraries**, which together have **115,000+ Maven dependents**.
- Compared with existing **OSS-Fuzz** harnesses, the generated harnesses achieved a **median 26% improvement** in **method-targeted coverage**.
- Under **package-level / full target-scope coverage**, the method outperformed **OSS-Fuzz by 6%** and **Jazzer AutoFuzz by 5%** respectively (median).
- Generation cost is low: on average about **10 minutes** and about **$3.20** per harness, suggesting it is practical for continuous fuzzing workflows.
- In a **12-hour** fuzzing campaign, the generated harnesses found **3 previously unreported bugs** in projects already integrated into OSS-Fuzz.
- The paper also notes that the only target that did not consistently outperform the baseline was **jackson-databind**, because its OSS-Fuzz baseline included additional fuzzing logic after target method execution, which increased overall coverage.

## Link
- [http://arxiv.org/abs/2603.08616v1](http://arxiv.org/abs/2603.08616v1)
