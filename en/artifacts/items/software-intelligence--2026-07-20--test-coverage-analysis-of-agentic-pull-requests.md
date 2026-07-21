---
source: arxiv
url: https://arxiv.org/abs/2607.18057v1
published_at: '2026-07-20T15:26:30'
authors:
- Atish Kumar Dipongkor
- Talank Baral
- Wing Lam
- Kevin Moran
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Test Coverage Analysis of Agentic Pull Requests

## Summary
This study finds that agent-generated pull requests often leave newly added code inadequately tested. Across 4,882 Java and Python PRs from five coding agents, existing tests cover only 61.5% of changed executable Java lines and 27.0% of changed Python lines, while agent-written tests improve coverage in a minority of cases.

## Problem
- Autonomous coding agents increasingly submit complete pull requests, but their testing behavior and the coverage of their own changes are poorly understood.
- Passing existing tests does not show that newly added code is exercised, which can leave regression-prone paths—especially error handling—untested.

## Approach
- Analyze 4,882 PRs from the AIDev dataset: 532 Java and 4,350 Python PRs produced by five coding agents.
- Classify PRs by whether they change production code, test files, or both, and measure how often agents add or modify tests.
- Reconstruct PR patches and run repository test suites with JaCoCo for Java and pytest-cov for Python.
- Compute diff coverage for added executable lines using existing tests, then remove agent-written test changes to estimate their incremental coverage gain.
- Label added lines by syntactic construct to identify consistently under-tested code categories.

## Results
- Of 4,387 PRs that modify code under test, 50.4% include no test-file changes; 49.6% include test changes.
- Existing tests cover 61.5% of changed executable lines in Java and 27.0% in Python. In Python, 64.8% of analyzed PRs have no changed line executed by an existing test.
- Agent-written tests raise mean diff coverage from 70.5% to 86.1% in Java (+15.6 percentage points, 64 Code + Tests PRs, p<0.001) and from 24.8% to 34.5% in Python (+9.6 points, 605 PRs, p<0.001).
- Coverage gains occur in only 35.9% of Java and 22.5% of Python Code + Tests PRs. In non-improving Java PRs, agents delete 82 tests and add 31, a 2.6x deletion-to-addition ratio; in Python, 74.8% add tests that still do not cover their changed lines.
- Error-handling constructs are especially under-tested: Try-Catch lines have miss rates of 86.0% in Java and 81.0% in Python, while Throw lines are missed 67.5% and 82.3%, respectively.
- The coverage analysis is limited to merged PRs from repositories that could be built and instrumented—213 Java and 1,664 Python PRs—so the results may not generalize to all agent-generated PRs.

## Link
- [https://arxiv.org/abs/2607.18057v1](https://arxiv.org/abs/2607.18057v1)
