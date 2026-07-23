---
source: arxiv
url: https://arxiv.org/abs/2607.19843v1
published_at: '2026-07-22T07:30:07'
authors:
- Yuhao Tan
- Zhibang Yang
- Fangkai Yang
- Yuan Yao
- Yu Kang
- Lu Wang
- Pu Zhao
- Xin Zhang
- Xiaoxing Ma
- Qingwei Lin
- Saravan Rajmohan
- Dongmei Zhang
topics:
- automated-program-repair
- code-intelligence
- bug-reproduction-tests
- mutation-testing
- multi-agent-software-engineering
- automated-software-production
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes

## Summary
CoHarden improves automated program repair by iteratively strengthening bug reproduction tests against plausible incorrect patches, rather than judging tests only by fail-to-pass behavior. On a 433-instance SWE-bench Verified ∩ SWT-bench Verified setting, it reports 69.4% Resolved and 78.9% test F→P, exceeding the same-backbone cogeneration baseline by 8.0 and 6.2 percentage points, respectively.

## Problem
- Bug reproduction tests are commonly evaluated only by fail-to-pass (F→P): failing on buggy code and passing on the golden fix. This can label a lax test as successful even when it also accepts plausible but incorrect fixes.
- Lax tests provide no downstream repair benefit, while misaligned tests can mislead repair agents. In joint test-and-fix generation, the two errors can also reinforce each other.
- The problem matters because passing a reproduction test does not necessarily establish that an automated patch fixes the reported behavior or its underlying cause.

## Approach
- Mutation Patch Evaluation (MPE) runs a generated test against semantic mutations of the golden fix and classifies it as Rigorous, Lax, or Misaligned using a 2×2 test-outcome matrix. A Laxity rate of β/total measures mutants accepted by the generated test but rejected by the reference test; the main cutoff is τ=0.202.
- The study separates BRT quality from downstream utility. On 1,104 F→P BRT/fix pairs and 474 non-F→P pairs, it measures the paired change in Resolved performance when tests are injected into an OpenHands + GPT-5-mini repair agent.
- CoHarden first generates a reproduction test without modifying source code. It then runs up to five hardening rounds that mutate the current fix, evaluate mutants against the current and previous tests, and update the test-fix pair until the temporal Laxity rate is at most 0.2.
- The method uses four targeted mutation operators and 12 candidate mutants per full round, replacing unavailable golden artifacts during deployment with a reference-free Temporal Matrix based on the previous-round test.

## Results
- Among injected F→P tests, Rigorous tests raised Resolved from 67.3% to 75.8% (+8.5 points), while Lax tests produced no change (69.5% to 69.5%, +0.0). Misaligned tests reduced Resolved by 3.6 points, from 44.5% to 40.9%.
- In cogeneration, the joint-failure rate was 19.9%, or 1.87× the 10.6% rate predicted under independent test and fix errors. Of 166 unresolved instances, 80 had an F→P-passing test paired with an incorrect fix.
- On the 433-instance SWE-bench Verified ∩ SWT-bench Verified evaluation, CoHarden achieved 69.4% Resolved and 78.9% F→P. OpenHands + Cogen reached 61.4% Resolved and 72.7% F→P, while InfCode reached 61.5% and 69.6%; CoHarden's reported gains over OpenHands + Cogen were +8.0 and +6.2 points.
- CoHarden cost $0.84 per instance, compared with $0.77 for InfCode and $0.88 for Agent-CoEvo; mutation generation accounted for 9.5% of the final run cost. The mutation pool is an approximation of plausible incorrect repairs, so the Rigorous/Lax assessment depends on its operators and sampling.

## Link
- [https://arxiv.org/abs/2607.19843v1](https://arxiv.org/abs/2607.19843v1)
