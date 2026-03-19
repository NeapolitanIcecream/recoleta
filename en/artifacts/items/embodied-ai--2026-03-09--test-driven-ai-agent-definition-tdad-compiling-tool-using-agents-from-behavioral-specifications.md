---
source: arxiv
url: http://arxiv.org/abs/2603.08806v1
published_at: '2026-03-09T14:04:54'
authors:
- Tzafrir Rehan
topics:
- llm-agents
- prompt-compilation
- behavioral-testing
- mutation-testing
- specification-gaming
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Test-Driven AI Agent Definition (TDAD): Compiling Tool-Using Agents from Behavioral Specifications

## Summary
TDAD turns tool-using LLM agent development into a process of “writing tests first and then compiling prompts, like software development,” automatically generating tests from behavioral specifications and iteratively modifying prompts until they pass. It focuses on solving the problems of production-grade agents being hard to verify, prone to regressions, and susceptible to gaming the tests, and provides a complete methodology with hidden tests, semantic mutation testing, and specification evolution evaluation.

## Problem
- Existing LLM agent development mainly relies on manual trial and error and spot checks, and **cannot systematically verify** whether behavioral requirements such as tool invocation order, policy compliance, PII protection, and deterministic outputs are satisfied.
- Small prompt changes can cause **silent regressions**, and many issues are only exposed after deployment, which is critical for compliance, security, and operations.
- If optimization targets only visible tests, the system may **game the specification (specification gaming)**: appearing to pass tests while the actual behavior is incorrect.

## Approach
- Agent development is treated as a “compilation” problem: the input is a YAML behavioral specification (tools, policies, decision trees, response contracts), and the output is a compiled prompt and tool descriptions.
- Two coding agents split the work: **TestSmith** first converts the specification into executable tests; **PromptSmith** then iteratively modifies the prompt based on visible test failures until all tests pass.
- To reduce “teaching to the test,” TDAD adds three layers of anti-gaming mechanisms: **visible/hidden test splits**, **semantic mutation testing** (deliberately generating defective prompt variants to see whether the tests can catch them), and **regression safety evaluation when the specification evolves from v1 to v2**.
- It also treats **tool descriptions** as first-class optimization targets, and requires the agent to output via a structured `respond` tool, so tests directly inspect tool invocation traces and structured fields rather than only natural-language text.
- Evaluation is based on **SpecSuite-Core**, which includes 4 deeply specified agent tasks: SupportOps, DataInsights, IncidentRunbook, ExpenseGuard.

## Results
- Across **24 independent trials** on **SpecSuite-Core** (4 specifications × 2 versions × 3 runs), TDAD reports a **v1 compilation success rate of 92%**.
- For successful **v1** runs, the average **hidden pass rate (HPR) was 97%**, indicating that it not only passes visible tests but also generalizes well to held-out tests.
- For evolved **v2** specifications, compilation success dropped to **58%**, but the paper says that most failed runs were only **1–2 visible tests short**, suggesting the method remains close to success under changing requirements.
- The average hidden pass rate for **v2** was **78%**, lower than v1, reflecting that specification evolution is harder, but still preserving substantial generalization ability.
- Semantic mutation testing achieved **mutation scores (MS) of 86%–100%**; additionally, **87%** of mutation intents were successfully activated, indicating that the test suite can usually detect common erroneous behaviors.
- The specification-evolution regression safety score **SURS averaged 97%**; the paper also provides some concrete cases: for example, DataInsights had a missed `HALLUCINATE_NUMBERS` mutation in v1, and v2 filled that testing gap; ExpenseGuard’s v2 added a new approval-threshold rule, increasing compilation iterations from **2 to 5**.

## Link
- [http://arxiv.org/abs/2603.08806v1](http://arxiv.org/abs/2603.08806v1)
