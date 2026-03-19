---
source: arxiv
url: http://arxiv.org/abs/2603.01409v1
published_at: '2026-03-02T03:22:44'
authors:
- Sicheng Zhu
- Jiajun Wang
- Jiawei Ai
- Xin Li
topics:
- reinforcement-learning
- unit-test-generation
- mutation-testing
- code-verification
- llm-for-code
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# MIST-RL: Mutation-based Incremental Suite Testing via Reinforcement Learning

## Summary
This paper proposes MIST-RL, which uses reinforcement learning to generate unit tests incrementally based on “added utility” rather than “number of tests,” thereby reducing redundancy and improving code verification quality. Its core value is achieving stronger fault detection with shorter test suites and improving downstream code reranking.

## Problem
- Existing LLM unit test generation methods mostly rely on “generating more tests,” but additional tests quickly face diminishing returns, with many later samples becoming semantically repetitive.
- Redundant tests cause **test bloat**: they increase inference and execution costs without effectively discovering new bugs, and they also weaken the discriminative power of tests as code verifiers.
- This matters because LLM-generated code is often incorrect on the first try; if the verifier is not aggressive enough, it becomes difficult to filter out candidate programs that seem plausible but actually contain subtle logic errors.

## Approach
- Test suite generation is formulated as a **sequential decision process**: at each step, the model generates a new test and uses the mutants killed by previous tests as the historical state.
- Learning is driven by an **incremental mutation reward**: a new test receives reward only if it kills mutants that were not previously killed; tests that merely re-cover old mutants receive little to no benefit.
- A **dynamic redundancy penalty** is added: if a test runs successfully but brings no new fault detection, a penalty that grows over time according to its position in the sequence is applied, forcing the model to generate high-value tests as early as possible.
- The reward function also distinguishes three cases: tests that fail to compile/execute receive a heavy penalty; tests with no new contribution receive a penalty; tests with new contribution receive a positive reward based on “assertion quality + weighted number of newly killed mutants.”
- **GRPO** is used for policy optimization, and a lightweight Python AST-based mutation engine is built to efficiently generate/evaluate mutants.

## Results
- On **HumanEval+**, MIST-RL achieves a **Mutant Kill Rate = 74.03%**, an improvement of **+28.5 percentage points** over **CodeRM-8B’s 45.53%**, and also higher than **Qwen3-14B’s 58.69%**; the average test suite length is **6.14 vs. 7.61**, **19.3%** shorter than CodeRM-8B.
- On **MBPP+**, MIST-RL achieves a **Mutant Kill Rate = 70.27%**, higher than **CodeRM-8B’s 61.08%** and **Qwen3-14B’s 66.50%**; the average length is **5.17 vs. 6.55**, **21.1%** shorter than CodeRM-8B.
- On **DS-1000**, MIST-RL reaches **57.90%** mutant kill, outperforming **CodeRM-8B’s 49.08%** and **Qwen3-14B’s 53.20%**; the average length is **5.78**, also shorter than CodeRM-8B’s **7.37**.
- As a downstream verifier, in **HumanEval+ code reranking**, when the number of candidates is **N=10**, **Pass@1 = 48.78%**, outperforming **CodeRM-8B’s 45.73%** and **Qwen3-14B’s 44.51%**, and improving over the SOTA baseline by **3.05 percentage points**.
- Under the **N=20** reranking setting, MIST-RL still leads: **62.80%**, compared with **CodeRM-8B’s 61.59%** and **Qwen3-14B’s 55.49%**.
- Ablation experiments show that removing the incremental reward reduces HumanEval+ mutation score from **74.03%** to **65.1%**; removing the dynamic penalty causes the average suite length to surge from **6.14** to **14.20**, indicating that both are critical for effectiveness and deduplication, respectively.

## Link
- [http://arxiv.org/abs/2603.01409v1](http://arxiv.org/abs/2603.01409v1)
