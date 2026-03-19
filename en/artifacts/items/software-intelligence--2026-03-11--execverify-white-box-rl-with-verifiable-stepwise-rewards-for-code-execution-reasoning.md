---
source: arxiv
url: http://arxiv.org/abs/2603.11226v1
published_at: '2026-03-11T18:49:45'
authors:
- Lingxiao Tang
- He Ye
- Zhaoyang Chu
- Muyang Ye
- Zhongxin Liu
- Xiaoxue Ren
- Lingfeng Bao
topics:
- code-reasoning
- reinforcement-learning
- white-box-verification
- code-generation
- execution-traces
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning

## Summary
ExecVerify trains code models with verifiable rewards on intermediate program-execution steps instead of only imitating teacher explanation text. It turns “read code and infer execution” into a reinforcement learning problem where answers can be checked step by step, and shows that this capability can also transfer to code generation.

## Problem
- Existing training for code execution reasoning mostly relies on SFT to learn teacher-written explanation chains, but during training it is **not possible to explicitly verify whether intermediate execution steps are actually correct**, making it easy to learn “text imitation” rather than semantic understanding.
- Training data typically **lacks controllable difficulty and structural coverage**, mixing in samples that are too easy or nearly unsolvable, which hurts small models’ ability to learn the true execution process.
- Weak code execution reasoning further degrades downstream tasks such as **code generation, program repair, and semantic understanding**, making it a key bottleneck in code intelligence.

## Approach
- First, perform **constraint-based data synthesis**: automatically generate programs around Python built-in types, methods, and control-flow patterns, and construct curriculum-style data with multiple difficulty levels under structural constraints from simple to complex.
- Execute each program to obtain interpreter traces, then automatically generate two types of **white-box verifiable questions**: next executed statement prediction (control-flow) and variable value/type prediction (data-flow).
- Train the model with **white-box reinforcement learning**: rewards consider not only whether the final I/O is correct, but also whether intermediate-step questions are answered correctly; the reward function combines final-state correctness with step-level correctness.
- Also add **reverse O→I prediction**, requiring the model to find executable inputs from outputs, reducing reliance on forward pattern matching alone.
- Use **two-stage training**: the first stage improves execution reasoning; the second stage applies code-generation RL with unit-test rewards, transferring reasoning ability to generating functionally correct programs.

## Results
- On code execution reasoning, the 7B base model improves from an average of **60.8** to **80.8** (`+ SFT + white-box RL`), higher than **76.3** for `+ SFT + I/O RL`, and also above the average score of **77.9** from **Qwen2.5-Coder-32B-Instruct**.
- In detailed metrics, `+ SFT + white-box RL` reaches **CRUXEval-O 85.6**, **LiveCodeBench-Exec 82.3**, **REval State 74.5**, and **REval Path 73.0**; compared with the 7B base’s **61.0 / 58.0 / 51.7 / 49.7**, this shows clear gains and suggests especially effective learning of white-box intermediate states.
- On code generation, the best two-stage model `+ SFT + white-box RL + UT RL` averages **57.1**, higher than pure `+ UT RL` at **53.9**, `+ I/O RL + UT RL` at **54.6**, and `+ SFT + I/O RL + UT RL` at **54.9**; the paper claims **up to a 5.9-point pass@1 improvement** over strong post-training baselines.
- Specific generation metrics include **HumanEval+ 84.8**, **MBPP+ 75.1**, **LiveCodeBench Hard 5.9**, and **BigCodeBench Hard 25.7**; all improve over the 7B base’s **84.1 / 71.7 / 3.0 / 18.2**.
- For data construction, the authors start from **239,992** original samples and **239,466** mutated samples; after execution-based filtering, **201,537** and **191,463** are retained, then difficulty filtering yields **119,358** training samples; Stage I actually uses **30K SFT + 30K RL**.
- Ablations show the two white-box question types are complementary: the full version averages **80.8**, control-flow only gets **79.9**, and data-flow only gets **78.1**. On library-related I/O prediction, the 7B base scores **56.0**, `SFT+I/O RL` scores **62.5**, and `SFT+White-Box RL` scores **64.7**, close to the 32B model’s **70.4**.

## Link
- [http://arxiv.org/abs/2603.11226v1](http://arxiv.org/abs/2603.11226v1)
