---
source: arxiv
url: http://arxiv.org/abs/2603.05863v1
published_at: '2026-03-06T03:38:17'
authors:
- Juyong Jiang
- Jiasi Shen
- Sunghun Kim
- Kang Min Yoo
- Jeonghoon Kim
- Sungju Kim
topics:
- code-generation
- reinforcement-learning
- self-reflection
- self-correction
- llm-reasoning
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# ReflexiCoder: Teaching Large Language Models to Self-Reflect on Generated Code and Self-Correct It via Reinforcement Learning

## Summary
This paper proposes ReflexiCoder, which uses reinforcement learning to directly bake the debugging process of “write code first, then self-reflect, then self-correct” into the model parameters, thereby avoiding reliance on external testers or execution feedback at inference time. It targets complex code generation tasks, with the main goals of higher single-pass success rates and lower iterative token overhead.

## Problem
- Existing code LLMs often use single-pass generation (“System 1”), and on complex algorithmic problems they can easily produce code that looks reasonable on the first try but is actually wrong.
- Existing iterative improvement methods usually depend on external oracles, execution environments, unit tests, or multi-round prompt interaction, leading to high deployment cost, high latency, and large token consumption.
- This matters because real development scenarios often do not have comprehensive test sets; if a model cannot **internalize debugging ability**, it is hard for it to reliably solve complex programming tasks.

## Approach
- The core method models code generation as a **structured trajectory**: `reasoning -> answer -> reflection -> corrected answer`, letting the model first solve the problem, then inspect bugs/optimization opportunities, and then correct itself.
- The authors use the **RL-zero** paradigm rather than first doing traditional SFT, directly applying reinforcement learning to optimize the full “reflection-correction” trajectory. The goal is not just to reward whether the final code is correct, but whether the model can discover problems on its own and fix them effectively.
- The reward function consists of several parts: format-compliance reward, reflection-step penalty, stepwise quality-improvement reward, and efficiency reward. In short, it encourages **few but effective reflections** and penalizes unproductive loops and verbose reasoning.
- During training, reflection-aware GRPO is used so the model learns to debug within its own “inner monologue”; at inference time, no external executor or additional critic is needed to drive repair.

## Results
- The authors claim effectiveness across **7 code benchmarks**, and that **ReflexiCoder-8B** reaches **SOTA among open-source models in the 1.5B-14B range**.
- **Single-attempt (Single)** results: HumanEval **94.51%**, HumanEval+ **87.20%**, MBPP **81.80%**, MBPP+ **78.57%**, BigCodeBench **35.00%**, LiveCodeBench **52.21%**, CodeForces **37.34%**.
- **Multiple-round reflection (Multiple)** results improve further to: HumanEval **95.73%**, BigCodeBench **36.84%**, LiveCodeBench **54.12%**, CodeForces **37.68%**; the paper says it can **match or exceed GPT-5.1** on some metrics.
- In the specific comparison numbers with proprietary models, GPT-5.1 is listed in the table as: HumanEval **95.12%**, HumanEval+ **87.20%**, MBPP **84.00%**, MBPP+ **79.10%**, BigCodeBench **39.56%**, LiveCodeBench **48.03%**, CodeForces **34.70%**. Based on this, ReflexiCoder in the single-attempt setting already surpasses GPT-5.1 on **LCB (52.21 vs 48.03)** and **CF (37.34 vs 34.70)**, but is not comprehensively ahead on **BCB/MBPP** and others.
- In terms of efficiency, the authors say it reduces **inference token overhead by about 40%** versus the base model in iterative mode, including **nearly 50% fewer reasoning tokens**, and that it “almost always executes only one reflection loop.”
- The paper also emphasizes that even in the single-attempt setting with **the same token budget as the baseline**, performance still exceeds the baseline, indicating that the gain does not simply come from “trying more times,” but from learning debugging ability inside the model.

## Link
- [http://arxiv.org/abs/2603.05863v1](http://arxiv.org/abs/2603.05863v1)
