---
source: arxiv
url: http://arxiv.org/abs/2604.21771v2
published_at: '2026-04-23T15:29:09'
authors:
- Binhang Qi
- Yun Lin
- Xinyi Weng
- Chenyan Liu
- Hailong Sun
- Gordon Fraser
- Jin Song Dong
topics:
- test-generation
- software-testing
- llm-for-code
- scenario-coverage
- java
- program-analysis
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Generalizing Test Cases for Comprehensive Test Scenario Coverage

## Summary
TestGeneralizer turns one developer-written test into more tests that cover the intended behavioral scenarios of a method. It targets scenario coverage rather than branch coverage and reports better coverage than EvoSuite, gpt-o4-mini, and ChatTester on a Java benchmark.

## Problem
- Existing automated test generation tools mostly optimize code coverage, but developers write tests to check requirement-driven scenarios that may not match control-flow branches.
- Important scenarios are often missing when the first test is written and get added later after bugs or issue reports, which makes testing slower and less complete.
- Requirements are often implicit in code and tests, so the task is to infer the hidden test pattern and generate valid scenario variants from a single initial test.

## Approach
- The system takes a focal method, one existing test, and the project codebase, then runs a 3-stage pipeline called TestGeneralizer.
- Stage 1 uses **Masked Oracle Modeling (MOM)**: it mutates the original test's assertions into executable wrong alternatives and asks the LLM to pick the correct one. If the model is unsure or wrong, it retrieves project facts through program analysis to improve understanding.
- Stage 2 asks the LLM to write a **test scenario template**: a compact plan with variation points such as input style, object type, or API choice. It then instantiates those variation points into concrete scenario instances with primary and alternative oracles.
- To make variation-point detection more accurate, the prompts are automatically tuned. To make instantiated scenarios project-valid, the system retrieves code facts with tools such as CodeQL and JDTLS.
- Stage 3 generates executable tests for each scenario instance and iteratively repairs compile errors, runtime errors, and assertion failures until the test passes or the iteration limit is reached.

## Results
- Evaluation covers **12 open-source Java projects**, **506 multi-test focal methods**, and **1,637 test scenarios**.
- Against **EvoSuite**, TestGeneralizer improves **mutation-based scenario coverage by 57.67%** and **LLM-assessed scenario coverage by 59.62%**.
- Against **gpt-o4-mini**, it improves **mutation-based scenario coverage by 37.44%** and **LLM-assessed scenario coverage by 32.82%**.
- Against **ChatTester**, it improves **mutation-based scenario coverage by 31.66%** and **LLM-assessed scenario coverage by 23.08%**.
- In a field study, the authors submitted **27** generated tests that developers had missed; **16** were accepted and merged into the official repositories.
- The paper also claims the method works consistently across both commercial and open-source LLMs, including **ChatGPT** and **DeepSeek-V3.1**.

## Link
- [http://arxiv.org/abs/2604.21771v2](http://arxiv.org/abs/2604.21771v2)
