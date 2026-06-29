---
source: arxiv
url: https://arxiv.org/abs/2605.04320v2
published_at: '2026-05-05T21:49:52'
authors:
- Toufique Ahmed
- Jatin Ganhotra
- Avraham Shinnar
- Martin Hirzel
topics:
- code-intelligence
- software-testing
- java
- llm-agents
- benchmarking
- automated-software-engineering
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Reproduction Test Generation for Java SWE Issues

## Summary
The paper introduces TDD-Bench-Java, a 250-instance benchmark for generating Java reproduction tests from issue reports, and e-Otter++ for Java, an LLM workflow that writes and refines tests. The main claim is that execution feedback plus issue rewriting improves fail-to-pass rates on Java SWE issues.

## Problem
- A reproduction test should fail on the buggy code and pass after the developer fix, which gives execution-based evidence that an issue is real and later fixed.
- Most recent reproduction-test work targets Python, while Java adds static typing, package/import rules, Maven or Gradle builds, and object-oriented code patterns.
- Existing Java coverage is limited: prior datasets are small, unavailable, or do not evaluate whether generated tests reproduce the issue on pre-fix code.

## Approach
- The authors build TDD-Bench-Java from Java samples in Multi-SWE-bench and SWE-PolyBench, then filter for developer tests with fail-to-pass behavior and remove duplicates.
- e-Otter++ first localizes likely relevant Java files and functions from the issue text, then chooses a package, imports, and test directory for a new test file.
- The generator writes one new Java test class and method, rather than editing an existing test, to reduce package and placement errors.
- A refiner runs the test on the old code, reads build or test logs, asks an LLM critic whether the failure matches the issue, and rewrites the test for up to 10 iterations.
- The system creates six candidates using the original issue plus five rewritten issue variants, then asks an LLM selector to choose one final test.

## Results
- TDD-Bench-Java contains 250 instances from 13 open-source Java repositories; examples include trinodb/trino with 44 instances, jackson-databind with 42, rocketmq with 41, and dubbo with 36.
- The benchmark average issue description length is 199.4 words; average changed code size is 86.3 lines and average changed test size is 87.2 lines.
- e-Otter++ reaches a 43.6% fail-to-pass rate with Claude-Sonnet-4.5 and 46.4% with GPT-5.2 on TDD-Bench-Java.
- Refinement improves fail-to-pass rate over the initial Otter generator by 9.4 percentage points for Claude-Sonnet-4.5 and 13.6 points for GPT-5.2.
- The Otter to e-Otter improvement is statistically significant for both models with McNemar's test at p < 0.01.
- The paper also reports evaluation on a 150-instance proprietary Java dataset, but the excerpt does not include its numerical results.

## Link
- [https://arxiv.org/abs/2605.04320v2](https://arxiv.org/abs/2605.04320v2)
