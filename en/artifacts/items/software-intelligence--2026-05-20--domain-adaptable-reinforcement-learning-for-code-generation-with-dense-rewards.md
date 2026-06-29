---
source: arxiv
url: https://arxiv.org/abs/2605.21180v1
published_at: '2026-05-20T13:47:52'
authors:
- Erfan Aghadavoodi Jolfaei
- Daniel Maninger
- Abhinav Anand
- Mert Tiftikci
- Mira Mezini
topics:
- code-generation
- reinforcement-learning
- dense-rewards
- program-synthesis
- robotics-code
- code-intelligence
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Domain-Adaptable Reinforcement Learning for Code Generation with Dense Rewards

## Summary
The paper trains Qwen2.5-Coder-1.5B with PPO using dense execution-aware rewards, so code tokens get feedback tied to syntax, lint checks, tests, data-flow matches, or robot simulator outcomes. It reports higher pass@1 on MBPP/MBPP+ and fewer non-executable robot programs on RoboEval.

## Problem
- Code LLMs can generate programs with syntax errors, failed tests, unsafe patterns, or domain violations.
- Sparse sequence-level RL rewards give the same penalty or reward to the whole output, which makes credit assignment weak when only a few tokens cause failure.
- Robotics code needs extra checks because a program can compile and still fail due to collisions, unreachable goals, invalid object use, or wrong action order.

## Approach
- The method fine-tunes a pre-trained Qwen2.5-Coder-1.5B-Instruct policy with proximal policy optimization.
- Rewards combine syntax checks from a SynCode-style constraint, Ruff linter signals, KL distance from a reference model, and optional task rewards.
- For general Python, the task rewards are unit-test pass@1 and data-flow graph match.
- For robotics, the task reward comes from RoboSim simulator feedback.
- Sequence-level signals are mapped back to code tokens or spans when possible; unit-test outcomes are spread across generated code tokens when exact attribution is unavailable.

## Results
- On MBPP pass@1, Qwen2.5-Coder-1.5B improves from 0.460 to 0.653, an absolute gain of 0.193 or 19.3 percentage points.
- On MBPP+ pass@1, the same model improves from 0.413 to 0.556, an absolute gain of 0.143 or 14.3 percentage points.
- On RoboEval with 80 tasks, Python-level errors drop from 77 to 11 after RL fine-tuning.
- On RoboEval, solved tasks rise from 0 to 14 out of 80 for the fine-tuned 1.5B model.
- The paper reports a shift from 100% non-executable robot code to 51% simulator-executable code after fine-tuning.
- Larger 7B baselines still score higher on RoboEval success: 30/80 for Qwen2.5-Coder-7B base and 31/80 for the 7B Robo-Instruct model, compared with 14/80 for the fine-tuned 1.5B model.

## Link
- [https://arxiv.org/abs/2605.21180v1](https://arxiv.org/abs/2605.21180v1)
