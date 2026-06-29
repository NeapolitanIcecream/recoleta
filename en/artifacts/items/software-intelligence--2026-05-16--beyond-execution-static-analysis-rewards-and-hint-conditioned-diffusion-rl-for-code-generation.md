---
source: arxiv
url: https://arxiv.org/abs/2605.17174v1
published_at: '2026-05-16T22:18:04'
authors:
- Shuyin Ouyang
- Zhaozhi Qian
- Faroq AL-Tam
- Muhammad AL-Qurishi
- Jie M. Zhang
topics:
- diffusion-code-models
- rl-for-code
- static-analysis-rewards
- hint-conditioned-sampling
- code-generation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Beyond Execution: Static-Analysis Rewards and Hint-Conditioned Diffusion RL for Code Generation

## Summary
This paper studies RL post-training for diffusion code models when unit-test rewards are too sparse to guide learning. It finds that Pylint-based static checking and moderate training-time hints can improve DiffuCoder on HumanEval and LiveCodeBench while reducing rollout cost.

## Problem
- Diffusion language models for code can enter a low-reward regime during RL: most sampled programs fail unit tests, so semantic rewards stay near zero and policy updates get little useful signal.
- Unit-test execution also adds rollout cost, which matters because RL samples multiple programs per prompt.
- The paper asks which reward signals and training hints work best across task difficulty levels on HumanEval, MBPP, and LiveCodeBench.

## Approach
- The study compares five standalone rewards: format extraction, syntax parsing, Pylint static checking, reference-solution similarity, and semantic unit-test pass rate.
- Static checking gives graded feedback without running code, using Pylint scores over errors, warnings, undefined names, unreachable code, unused variables, and related issues.
- Hint-conditioned diffusion sampling reveals some reference-solution tokens only during RL training; evaluation uses no hints.
- It tests left-to-right hints, random token hints, and AST-based hints at ratios such as 0.25, 0.5, and 0.75.
- Experiments use DiffuCoder and Dream-Coder 7B SFT checkpoints, AceCode-87K for RL training, and an all-of-3 evaluation protocol where all three sampled solutions must pass.

## Results
- On DiffuCoder, static checking improves over semantic reward from 53.9 to 67.1 on HumanEval, 60.8 to 61.7 on MBPP, and 14.9 to 15.5 on LiveCodeBench.
- Static checking reduces DiffuCoder rollout time from 29.3 seconds to 26.5 seconds, a 9.4% reduction, because it avoids repeated test execution.
- On Dream-Coder, static checking reaches 70.9 on HumanEval versus 69.1 for semantic reward; similarity reaches 62.5 on MBPP versus 61.9 for semantic reward; LiveCodeBench remains weak, with semantic at 3.6 and format at 8.1.
- Under semantic reward on DiffuCoder, hints improve HumanEval from 53.9 with no hint to 68.9 with left-to-right hints at 0.5; random hints at 0.25 reach 16.3 on LiveCodeBench versus 14.9 with no hint.
- Under static checking, AST hints give the best LiveCodeBench score in Table 4: 16.5 at a 0.5 hint ratio, compared with 15.5 with no hint.
- Higher hint ratios do not always help: under static checking with random hints, HumanEval falls from 67.7 at 0.25 to 40.4 at 0.5 and 32.1 at 0.75.

## Link
- [https://arxiv.org/abs/2605.17174v1](https://arxiv.org/abs/2605.17174v1)
