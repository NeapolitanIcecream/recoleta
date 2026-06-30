---
source: arxiv
url: https://arxiv.org/abs/2606.30549v1
published_at: '2026-06-29T16:47:46'
authors:
- Jessica Hutchison
- Ian Tyler Applebaum
- Kenneth Angelikas
- Kush Rakesh Patel
- Phuoc Nguyen
- Antonio Lazaro
- Nicholas Rucinski
- Rahad Arman Nabid
- Stephen MacNeil
topics:
- code-completion
- programming-education
- behavioral-signals
- attention-checks
- human-ai-interaction
- code-intelligence
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# To Tab or Not to Tab: Measuring Critical Engagement in AI Code Completion Tools Using Behavioral Signals and Attention Checks

## Summary
The paper introduces Clover, a VS Code code-completion extension that logs how students accept, reject, edit, and inspect AI suggestions. It uses deliberate attention checks to measure whether novice programmers notice bad AI-generated lines.

## Problem
- Students may accept AI code suggestions without checking whether the code fits the task, which can hurt learning and debugging.
- Prior studies used think-alouds, screen recordings, screenshots, eye tracking, and journals, which give detail but do not scale well to many programming sessions.
- The paper targets a measurement gap: instructors and researchers need behavioral signals that show how students use AI code completion during real coding work.

## Approach
- Clover mimics GitHub Copilot in VS Code, including single-line suggestions at the cursor and Tab-to-accept behavior.
- The system logs events such as suggestion shown, tab accept, slow accept, accept-then-modify, accept-then-delete, ignore, run code, dwell time, and failed attention check.
- Attention checks are deliberately misleading suggestions, such as `count--` when `count++` fits the immediate goal. Accepting one counts as a failed attention check; rejecting it counts as passing.
- The authors ran an in-person study with 55 analyzed CS1 students working on a Java rainfall problem with up to 26 test cases.
- They analyzed session-level metrics with Spearman correlations against task performance and failed attention check rate.

## Results
- Students accepted an average of 18.4 suggestions (SD 30.9), tab-accepted 17.1 suggestions (SD 31.0), slow-accepted 1.3 suggestions (SD 1.5), modified accepted suggestions 17.7 times (SD 29.8), deleted accepted suggestions 0.6 times (SD 1.0), and ignored 36.3 suggestions (SD 13.3).
- Average dwell time was 12.2 seconds (SD 8.1), with a range of 1.7 to 39.1 seconds.
- Students ran code 15.5 times on average (SD 12.6), with a range of 0 to 52 runs.
- Average task performance was 10.4 passed tests out of 26 (SD 12.9); 22 of 55 students passed all 26 tests.
- Number of runs had the strongest positive correlation with task performance among measured behaviors, but the effect was modest (Spearman ρ = 0.26).
- Tab acceptance rate strongly correlated with failed attention check rate (ρ = 0.73, p < 0.001), and dwell time negatively correlated with failed attention check rate (ρ = -0.26). Failed attention check rate weakly correlated with lower task performance (ρ = -0.17).

## Link
- [https://arxiv.org/abs/2606.30549v1](https://arxiv.org/abs/2606.30549v1)
