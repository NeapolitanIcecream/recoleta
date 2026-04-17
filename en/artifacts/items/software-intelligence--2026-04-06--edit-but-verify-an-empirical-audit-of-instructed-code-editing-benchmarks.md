---
source: arxiv
url: http://arxiv.org/abs/2604.05100v1
published_at: '2026-04-06T18:59:42'
authors:
- Amir M. Ebrahimi
- Gopi Krishnan Rajbahadur
topics:
- code-editing-benchmarks
- llm-evaluation
- benchmark-audit
- software-engineering
- test-coverage
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Edit, But Verify: An Empirical Audit of Instructed Code-Editing Benchmarks

## Summary
This paper audits the two main instructed code-editing benchmarks with human-written instructions and test-based evaluation: CanItEdit and EDIT-Bench. It argues that both benchmarks measure a narrower slice of real code editing than deployment decisions need, and that EDIT-Bench in particular has weak or faulty test artifacts.

## Problem
- The paper asks whether current instructed code-editing benchmarks actually reflect real developer editing work and whether their tests can reliably judge correctness.
- This matters because instructed code editing is about 19% of real coding-assistant interactions, and benchmark scores are used to pick models for tools such as IDE assistants.
- If benchmarks overfocus on the wrong languages, domains, or edit types, or if tests miss regressions, then model rankings can mislead product and deployment choices.

## Approach
- The authors surveyed more than 150 code benchmarks and found only two that fit their criteria: human-authored natural-language edit instructions on existing code, single-file local scope, and test-based evaluation: CanItEdit and EDIT-Bench.
- They compared both benchmarks against real-world reference sources: Copilot Arena, AIDev, and GitHub Octoverse, using three representativeness axes: programming language, edit intent, and application domain.
- They executed all benchmark test suites in instrumented Docker environments and measured test counts, whole-file statement coverage, diff-region coverage, and whether tests check only the requested edit or also catch unwanted changes outside the edited region.
- For EDIT-Bench, which does not release reference solutions, they reconstructed passing solutions from models with perfect published pass rates to estimate coverage on 91 executable problems.
- They also inspected 15 EDIT-Bench problems unsolved by all 40 evaluated models and checked codebase duplication within both benchmarks.

## Results
- Language coverage is highly skewed: CanItEdit is 105/105 Python, and EDIT-Bench is 89.8% Python. Combined, the two benchmarks put over 90% of tasks in Python, while Python is only about 20–30% of real-world AI-assisted coding activity. TypeScript, GitHub’s most-used language by contributor count, is absent.
- Edit intent is narrow: 78.7% of EDIT-Bench and 85.7% of CanItEdit are feature or fix tasks. Four categories that make up 31.4% of human PRs in AIDev—docs, chore, build, and ci—have 0% representation in both benchmarks. Test-writing tasks are only 1.9% in each benchmark versus 4.5% of agent PRs.
- Domain coverage is misaligned: backend and frontend work together account for 46% of real-world editing activity, but CanItEdit has 0% backend and 0% frontend coverage, while EDIT-Bench reaches only 13.9% backend and 10.2% frontend. CanItEdit puts 68.6% of tasks in algorithm problems versus 18% in the real-world reference; EDIT-Bench puts 36.1% in AI/ML versus 7% in the reference.
- Test adequacy differs sharply: CanItEdit has median 13 tests per problem and near-complete whole-file coverage (median 100.0%, mean 99.8%). EDIT-Bench has median 4 tests (mean 4.7), 14 problems with a single test, median whole-file coverage of 40.0% (mean 48.7%), and median diff-region coverage of 85.7% but mean 64.9%; 11 problems have 0% diff-region coverage and 39 of 91 executable problems (42.9%) fall below 75% diff-region coverage.
- Scope checks are weak in EDIT-Bench: 59% of low-coverage suites would not detect extra modifications outside the requested edit region, and 56% of all tests check only the edited code. The paper gives an example where adding the requested Dropout layer while silently changing convolution kernel sizes still passes.
- Among 15 EDIT-Bench problems unsolved by all 40 models, 11 are attributed to benchmark artifacts rather than model limits. The paper also reports codebase overlap: 29% of EDIT-Bench problems and 6% of CanItEdit problems share a codebase with another problem in the same benchmark.

## Link
- [http://arxiv.org/abs/2604.05100v1](http://arxiv.org/abs/2604.05100v1)
