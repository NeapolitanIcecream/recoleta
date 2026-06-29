---
source: arxiv
url: https://arxiv.org/abs/2605.06125v1
published_at: '2026-05-07T12:31:09'
authors:
- Ye Shang
- Quanjun Zhang
- Haichuan Hu
- Chunrong Fang
- Liang Xiao
- Zhenyu Chen
topics:
- test-evolution
- coding-agents
- software-testing
- code-intelligence
- benchmarking
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution

## Summary
TEBench is a project-level benchmark for coding agents that must update tests after a production-code commit. It matters because current agents find only about half of affected tests, and stale or missing tests can leave changed behavior unchecked.

## Problem
- Existing test-evolution benchmarks give the affected test method as input, so they skip the search across a repository.
- Real commits can break tests, leave passing tests semantically stale, or add behavior with no test at all.
- Poor test evolution lets suites pass while no longer checking the behavior changed by the commit.

## Approach
- The task input is a repository and a production-code-changing commit; the output is a test patch.
- TEBench labels each instance as Test-Breaking, Test-Stale, Test-Missing, or a combination of these types.
- The dataset comes from Defects4J Java projects after static filtering, execution checks, and quality filters.
- Evaluation separates test identification from patch quality, using precision, recall, and F1 for affected tests and executability, coverage overlap, and token-level modification similarity for updates.
- The paper evaluates seven agent configurations across Claude Code, Codex CLI, and OpenCode, plus a heuristic baseline.

## Results
- TEBench contains 314 task instances from 10 Java projects, drawn from 67,670 starting commits and 14 Maven Defects4J projects.
- The final dataset covers 172 Test-Breaking tasks, 207 Test-Stale tasks, and 199 Test-Missing tasks; labels can overlap.
- Seven agent configurations reach identification F1 scores from 45.7% to 49.4%, with less than 4 percentage points between them.
- Test-Stale is hardest, with average F1 around 36%, because agents mainly follow execution failures and miss passing tests that need semantic updates.
- Exhaustive structural dependency analysis reaches only 66% recall, leaving about one-third of affected tests outside direct dependency tracing.
- The paper reports that agent patches often compile and run, but their edits differ a lot from developer-written ground truth.

## Link
- [https://arxiv.org/abs/2605.06125v1](https://arxiv.org/abs/2605.06125v1)
