---
source: arxiv
url: https://arxiv.org/abs/2606.24453v1
published_at: '2026-06-23T11:41:32'
authors:
- Theodore Papamarkou
- Vladislav Smirnov
- Viktor Mazanov
- Artem Vazhentsev
- Preslav Nakov
- Timothy Baldwin
- Artem Shelmanov
topics:
- coding-agents
- bayesian-control
- code-intelligence
- tool-orchestration
- uncertainty-quantification
- automated-program-repair
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Bayesian control for coding agents

## Summary
This paper treats coding-agent orchestration as a Bayesian control problem over whether a candidate program is correct. Its main claim is that posterior-based tool use helps most when verification costs are high and cheaper critics give useful but imperfect signals.

## Problem
- Coding agents must choose when to generate, run cheap diagnostics, refine code, call an expensive verifier, or stop.
- Fixed policies such as always verifying, best-of-N sampling, single-critic gates, and fixed generate-critique-regenerate loops do not track uncertainty about candidate correctness.
- The problem matters because verifier calls can dominate cost in CI, SWE-Bench-style setups, or other slow test environments.

## Approach
- The method keeps a belief score, b = P(Y = 1 | evidence), where Y means the current candidate will pass the oracle verifier.
- Cheap critics such as syntax checks, public tests, and an LLM judge update the belief with Bayes' rule using calibrated likelihoods P(z | Y).
- Generator calls move the belief through measured fix and break probabilities, P(fix | broken) and P(break | correct).
- The controller compares expected utility for actions: call a critic, regenerate, verify, or stop. Utility is reward for a correct solution minus tool costs.
- The paper implements a one-step Bayesian greedy controller and a finite-horizon dynamic-programming controller with horizon H = 3 on a 51-point belief grid.

## Results
- The evaluation covers 6 generators and 9 coding benchmarks across function-level synthesis, repository-level patch generation, and bug fixing.
- Initial pass-rate priors range from 0.05 to 0.96 across generator-benchmark cells, giving low-success and high-success settings.
- The regime analysis pools 7,020 sweep points over P(Y = 1) and C_ver/R. It finds Bayesian policies win mainly when verification cost is high, especially around C_ver/R ≳ 1.
- In the reported cost setup, the slow-oracle regime uses C_ver = 90, C_syn = 1, C_test = 2, C_llm = 5, C_gen = 10, and R = 100. The fast-oracle regime uses C_ver = 5 and critic costs of 1.
- The excerpt does not provide a full numeric utility-gain table. The strongest concrete claim is that Bayesian control beats fixed policies in low-prior, high-verifier-cost regimes with informative critics, while public-test gating or always_verify wins when public tests predict hidden tests well, the prior is high, or verification is cheap.
- The paper also claims the posterior belief is a better uncertainty score than token probability and raw tool success baselines, but the excerpt does not include the calibration metrics.

## Link
- [https://arxiv.org/abs/2606.24453v1](https://arxiv.org/abs/2606.24453v1)
