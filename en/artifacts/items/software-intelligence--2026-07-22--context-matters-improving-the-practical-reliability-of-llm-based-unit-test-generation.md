---
source: arxiv
url: https://arxiv.org/abs/2607.19682v1
published_at: '2026-07-22T02:31:10'
authors:
- Junjie Chen
- Ziqi Wang
- Lin Yang
- Chen Yang
- Xiao Chu
- Jianyi Zhou
- Guangtai Liang
- Qianxiang Wang
- Dong Wang
topics:
- code-intelligence
- automated-software-production
- unit-test-generation
- llm-agents
- program-analysis
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation

## Summary
CATGen improves the practical reliability of LLM-generated unit tests by making project context explicit and moving scaffolding and common repairs into deterministic analysis. The experience paper reports higher compilation and coverage rates with lower time and token use on proprietary industrial projects and Defects4J.

## Problem
- LLM-generated tests often fail to compile in framework-heavy projects with cross-file dependencies, even when their test logic is plausible.
- Missing project context, fragile test-class scaffolding, and repeated LLM repair loops increase developer effort, latency, and token consumption.
- This matters because coverage improvements have little practical value until generated tests compile and execute.

## Approach
- CATGen retrieves five types of context: focal-class structure, focal-method details, external method calls, testing framework, and mocking framework, using build-file parsing and lightweight AST-based analysis.
- It deterministically constructs a framework-specific test-class skeleton with imports, annotations, lifecycle methods, mocks, and initialization instead of asking the LLM to generate this boilerplate.
- The LLM performs skeleton-conditioned completion, generating test methods, mocks, and assertions while preserving the fixed structure and analyzing the focal method's branches.
- Program-analysis post-processing applies eight deterministic repair strategies, including import completion, annotation correction, signature alignment, invalid-reference resolution, and exception handling, without additional LLM repair rounds.

## Results
- On 183 focal methods from 8 proprietary industrial projects, CATGen improved compilation success by 24.72%–38.05% over 6 representative baselines.
- In the industrial benchmark, line coverage increased by 17.27%–22.17% and branch coverage by 15.31%–18.24%.
- Industrial generation time fell by 51.27%–69.00%, while token usage fell by 66.83%–83.86%.
- On Defects4J, CATGen improved compilation success by 10.42%–14.33%, line coverage by 6.11%–8.39%, and branch coverage by 3.27%–10.56% over existing LLM-based approaches.
- The industrial benchmark contains methods where 57.38% involve complex dependencies and that interact with an average of 3.05 external files, but the excerpt does not provide absolute metric values or per-baseline results.

## Link
- [https://arxiv.org/abs/2607.19682v1](https://arxiv.org/abs/2607.19682v1)
