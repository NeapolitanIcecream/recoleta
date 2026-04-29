---
source: arxiv
url: http://arxiv.org/abs/2604.19315v1
published_at: '2026-04-21T10:24:26'
authors:
- Jamie Lee
- Flynn Teh
- Hengcheng Zhu
- Mengzhen Li
- Mattia Fazzini
- Valerio Terragni
topics:
- llm-test-generation
- unit-testing
- mocking
- java
- mutation-testing
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Improving LLM-Driven Test Generation by Learning from Mocking Information

## Summary
MockMill improves LLM-based unit test generation by feeding the model mocking information already present in developer-written tests. On 10 Java classes from six open-source projects, it generated executable tests that often reached code and killed mutants missed by existing tests, a plain LLM baseline, and Randoop.

## Problem
- LLMs can generate unit tests, but they usually rely on the class under test and nearby text, while ignoring behavior already encoded in test doubles such as Mockito stubbings and verify calls.
- That misses concrete usage knowledge: which dependency methods get called, with which arguments, and what values or exceptions should come back.
- This matters because tests that follow real dependency behavior can cover harder paths and catch faults that generic generated tests miss.

## Approach
- MockMill scans an existing Java test suite and finds project classes that appear as mocked dependencies in other tests.
- It extracts mocking facts from JUnit 5 and Mockito tests with AST analysis, mainly stubbings and verify operations, and stores the relevant method calls, arguments, returns, and exceptions in structured JSON.
- It prompts an LLM with three inputs: the full source code of the target class, explicit test-generation instructions aimed at mutation-sensitive assertions, and the extracted mock information.
- It asks the LLM to build tests against real instances of the target class while reusing exact values and interaction patterns found in mocks.
- After generation, it runs an iterative compile/execute/repair loop that feeds compiler or runtime errors back to the LLM until the tests pass or a retry limit is hit.

## Results
- Dataset: 10 classes from 6 open-source Java projects; evaluation used 4 LLMs: GPT-4o Mini, GPT-5 Mini, GPT-5, and Claude Sonnet 4.5.
- Executability was high after repair: eventual compilation reached 92% with GPT-4o Mini and 100% with GPT-5, GPT-5 Mini, and Claude Sonnet 4.5; test pass rate reached 81.6%, 98.6%, 99.7%, and 99.7% respectively.
- Median mutation score under MockMill was 43% for GPT-4o Mini, 62% for GPT-5, 84% for GPT-5 Mini, and 89% for Claude Sonnet 4.5; maximum mutation score reached 85%, 100%, 100%, and 100%.
- Median line coverage under MockMill was 58% for GPT-4o Mini, 91% for GPT-5, 93% for GPT-5 Mini, and 94% for Claude Sonnet 4.5; maximum line coverage reached 93%, 100%, 100%, and 100%.
- Test volume varied by model: MockMill generated 8.5 tests per class on average with GPT-4o Mini, 11.4 with GPT-5 Mini, 13.2 with GPT-5, and 45.7 with Claude Sonnet 4.5.
- The paper claims MockMill covers lines and kills mutants missed by existing project tests, a no-mock LLM baseline, and Randoop, but the excerpt does not include the detailed head-to-head numbers for those comparisons.

## Link
- [http://arxiv.org/abs/2604.19315v1](http://arxiv.org/abs/2604.19315v1)
