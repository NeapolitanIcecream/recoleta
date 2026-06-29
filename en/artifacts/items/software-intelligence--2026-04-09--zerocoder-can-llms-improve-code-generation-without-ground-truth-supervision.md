---
source: arxiv
url: http://arxiv.org/abs/2604.07864v1
published_at: '2026-04-09T06:24:54'
authors:
- Lishui Fan
- Mouxiang Chen
- Tingwei Zhu
- Kui Liu
- Xin Xia
- Shanping Li
- Zhongxin Liu
topics:
- code-generation
- test-generation
- reinforcement-learning
- self-supervision
- program-synthesis
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ZeroCoder: Can LLMs Improve Code Generation Without Ground-Truth Supervision?

## Summary
ZeroCoder trains a model to write code and generate tests at the same time, without human-written tests or reference solutions. It uses execution outcomes between self-generated code and self-generated tests to create rewards, then improves both roles through co-evolution.

## Problem
- Standard RL for code generation usually needs human-written unit tests or tests derived from reference solutions, which are costly and hard to scale.
- Self-generated tests alone are often weak, so bad code can still pass them and the reward signal becomes noisy.
- The paper asks whether an LLM can improve code generation with no ground-truth supervision at all, using only code-test execution feedback.

## Approach
- ZeroCoder uses one model in two prompted roles: a **coder** that samples candidate programs and a **tester** that samples candidate tests for the same problem.
- It executes every sampled program against every sampled test to build a pass/fail matrix, then applies a selector such as MaxPass, CodeT, or **B^4** to pick a consensus set of likely good solutions and tests.
- The coder gets reward for being selected into the consensus solution set. The tester gets reward for producing executable tests that both pass on a proxy-good solution and kill mutated versions of that solution, which pushes tests to be discriminative rather than trivial.
- Before RL, ZeroCoder filters out low-information training problems by keeping only instances whose pass/fail matrix has high enough rank, since low-rank matrices give weak learning signals.
- The paper also adds **DyB^4**, a dynamic version of the Bayesian selector that recalibrates its priors during training using as few as 10 labeled calibration instances to reduce selector drift.

## Results
- In the fully label-free setting, on **Qwen2.5-Coder-7B-Instruct**, ZeroCoder with **B^4** improves code generation by **14.5%** and test generation by **15.6%** relative to the base model.
- On the same model, adding **DyB^4** raises the gains to **21.6%** for code generation and **24.3%** for test generation, and the paper says this is competitive with oracle-supervised training.
- Averaged across **3 model families** and **6 benchmarks**, ZeroCoder with **DyB^4** improves code generation by **18.8%** and test generation by **62.7%** over base models.
- The method is evaluated on **4 code-generation benchmarks** and **2 test-generation benchmarks**. Code generation uses **Pass@1** under greedy decoding; test generation uses **test accuracy** and **mutation score**.
- DyB^4 uses a calibration set of only **10 labeled instances**, and the paper reports that this calibration step adds about **2%** per-step wall-clock time.

## Link
- [http://arxiv.org/abs/2604.07864v1](http://arxiv.org/abs/2604.07864v1)
