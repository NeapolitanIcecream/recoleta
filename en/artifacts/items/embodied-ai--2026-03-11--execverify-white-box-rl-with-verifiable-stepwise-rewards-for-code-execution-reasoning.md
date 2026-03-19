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
- white-box-rewards
- execution-traces
- code-generation
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# ExecVerify: White-Box RL with Verifiable Stepwise Rewards for Code Execution Reasoning

## Summary
ExecVerify proposes a white-box reinforcement learning framework for code execution reasoning, using verifiable intermediate execution rewards instead of merely imitating teacher explanations. It also combines constraint-based data synthesis with two-stage training to transfer execution reasoning ability to code generation.

## Problem
- Existing code reasoning training mostly relies on SFT to imitate teacher-generated explanation chains, but intermediate execution steps (such as the next statement, variable values, and variable types) **cannot be explicitly verified** during training.
- This can cause the model to learn to “sound like it is explaining” without actually understanding how the program executes, which is especially pronounced for smaller models and affects downstream tasks such as code generation and program repair.
- Existing data usually lacks **difficulty control**: samples may be too easy or too hard, preventing gradual curriculum-style training.

## Approach
- Use **constraint-based program synthesis** to build the training set: enumerate Python built-in types and methods, then progressively add method-composition constraints and control-flow nesting constraints to generate programs from simple to complex.
- Automatically synthesize inputs for each program, execute and filter them, obtaining 239,992 raw and 239,466 mutated instances at first; after execution filtering, retain 201,537 raw and 191,463 mutated instances; then, after difficulty filtering, keep **119,358** samples that are “non-trivial but solvable for 7B.”
- Automatically generate two types of **verifiable white-box questions** from interpreter execution traces: control-flow questions (predict the next executed statement) and data-flow questions (predict the next-step variable value/type).
- In stage one, perform a brief SFT warm-up first, then apply white-box RL; the reward jointly considers final I/O correctness and intermediate-step correctness, using \(R_{white-box}=2((1-\alpha)R^{I\rightarrow O}+\alpha R_{white})\), with \(\alpha=0.5\) in the paper.
- In stage two, use unit-test rewards for code generation RL, transferring the learned execution reasoning ability to generating code that passes tests.

## Results
- **Code reasoning**: the final 7B model (SFT + white-box RL) improves the average score on CRUXEval, LiveCodeBench-Exec, and REval from **60.8** for the base 7B model to **80.8** (+**20.0**), surpassing the **77.9** average score of Qwen2.5-Coder-32B-Instruct.
- On specific reasoning metrics, the 7B white-box RL model reaches: CRUXEval-O **85.6**, CRUXEval-I **81.0**, LCB-Exec **82.3**, REval State **74.5**, Path **73.0**; compared with the base 7B model, examples include CRUXEval-O **61.0→85.6**, State **51.7→74.5**, and Path **49.7→73.0**.
- Compared with I/O RL alone or SFT+I/O RL, white-box RL is stronger overall: the average scores are **71.4**, **76.3**, and **80.8**, respectively, showing that intermediate execution rewards are better than looking only at the final output.
- **Code generation**: the best two-stage 7B model (SFT + white-box RL + UT RL) achieves an average score of **57.1** on HumanEval/MBPP/LiveCodeBench/BigCodeBench, higher than the base 7B’s **51.0** and also higher than pure UT RL’s **53.9**.
- The paper claims that its code generation pass@1 improves by up to **5.9** percentage points over strong post-training baselines; in the table, for example, LiveCodeBench-Hard improves from the base 7B’s **3.0** to **5.9**, MBPP+ from **71.7** to **75.1**, and BigCodeBench-Hard from **18.2** to **25.7**.
- White-box question ablations show that control-flow and data-flow rewards are complementary: Full averages **80.8**, better than CF-only’s **79.9** and DF-only’s **78.1**. In addition, on library I/O prediction, the base 7B model gets **56.0**, SFT+I/O RL gets **62.5**, and SFT+white-box RL gets **64.7**, close to the 32B model’s **70.4**.

## Link
- [http://arxiv.org/abs/2603.11226v1](http://arxiv.org/abs/2603.11226v1)
