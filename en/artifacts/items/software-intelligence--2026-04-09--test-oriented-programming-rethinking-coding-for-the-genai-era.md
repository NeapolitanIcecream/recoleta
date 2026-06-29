---
source: arxiv
url: http://arxiv.org/abs/2604.08102v1
published_at: '2026-04-09T11:21:28'
authors:
- Jorge Melegati
topics:
- test-oriented-programming
- llm-code-generation
- software-engineering
- test-generation
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Test-Oriented Programming: rethinking coding for the GenAI era

## Summary
The paper proposes Test-Oriented Programming (TOP), a software development style where developers review generated tests and let the LLM generate production code from those tests. The authors built a proof-of-concept tool, Onion, and show that this workflow can complete a small command-line program, with clear limits and failure modes.

## Problem
- Current LLM coding tools still leave developers inspecting production code, so the abstraction level stays close to ordinary programming.
- Natural-language specifications are ambiguous, and LLM outputs are non-deterministic, so direct delegation of implementation is hard to trust.
- The paper asks whether developers can shift their review effort to test code instead of production code, which matters if GenAI is going to reduce manual coding work in a reliable way.

## Approach
- TOP uses natural-language specifications to generate test code first, then uses those tests to generate production code.
- Developers review and edit the generated YAML configuration, system structure, and test files, but do not directly edit production code in the intended workflow.
- The authors implemented this idea in Onion, a command-line Python tool that iteratively generates project structure, acceptance tests, class tests, and then implementation code until tests pass or the run aborts.
- The evaluation used one small BibTeX command-line application with features to add entries, list entries, and search text, and compared two models: GPT-4o-mini and Gemini 2.5-Flash.

## Results
- Onion was run **5 times per model** on the same task, for **10 total runs**.
- **All 10 runs succeeded** in producing the target application.
- In **0 runs** did the developers need to directly modify production code.
- In **2 runs total** (**1 with GPT-4o-mini, 1 with Gemini 2.5-Flash**), developers had to add comments to the test code to guide generation after repeated failures on the same tests.
- For **GPT-4o-mini**, the authors report **1 run** where they had to modify the test code before checking the implementation.
- The paper does **not report standard software metrics** such as pass rate by benchmark, time saved, token cost, accuracy, or comparison against Copilot, TDD, or multi-agent baselines. The strongest concrete claims are that production code could be generated from reviewed tests on a small task, outputs varied across runs, and Gemini 2.5-Flash tended to generate longer, more commented code than GPT-4o-mini.

## Link
- [http://arxiv.org/abs/2604.08102v1](http://arxiv.org/abs/2604.08102v1)
