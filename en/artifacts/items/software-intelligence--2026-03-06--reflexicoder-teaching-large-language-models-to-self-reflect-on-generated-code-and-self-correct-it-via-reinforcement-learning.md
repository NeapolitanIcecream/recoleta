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
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ReflexiCoder: Teaching Large Language Models to Self-Reflect on Generated Code and Self-Correct It via Reinforcement Learning

## Summary
This paper proposes ReflexiCoder: a code LLM training framework that uses reinforcement learning to internalize the process of “write code first, then self-reflect, then self-correct” into the model parameters, thereby reducing reliance on test harnesses, execution environments, or external critics. It targets the single-pass generation bottleneck on complex algorithmic problems, with a focus on autonomous debugging at inference time while using fewer tokens.

## Problem
- Existing code LLMs often rely on single forward-pass generation ("System 1"), which tends to produce code that looks plausible but is actually wrong on complex, multi-step algorithmic tasks.
- Existing iterative repair methods usually depend on external oracles, unit tests, execution feedback, or costly multi-round prompting, which are often unavailable in real development settings and incur high latency.
- The key question is: how can a model, **during inference without external feedback**, identify bugs, reflect, and correct code by itself? This matters because it directly affects the autonomy, deployment cost, and practical usability of coding agents.

## Approach
- The core method models code generation as a **structured trajectory**: `reasoning -> answer -> reflection -> corrected answer`, and uses RL to directly optimize the entire “self-debugging trajectory,” not just the first answer, into the model weights.
- The authors adopt an **RL-zero** paradigm: instead of first relying on traditional SFT to teach a fixed reflection template, they let the model autonomously learn reflection-correction patterns suited to its own parameter space through rewards.
- The reward function is compositional: it first requires **strict format compliance**; it then rewards **quality improvement at each round** and **final test passing**, while penalizing **too many reflection rounds** and additionally encouraging **larger improvements in fewer rounds**.
- Unlike prior approaches such as CodeRL/PPOCoder that “optimize single-pass generation + execution rewards,” ReflexiCoder optimizes the trajectory of “finding problems and fixing them,” aiming to turn debugging into an intrinsic model capability.
- Training is based on fine-tuning Qwen3-8B into ReflexiCoder-8B, with policy optimization using reflection-aware GRPO; at inference time, it can answer directly in single-pass mode or run in a multi-step reflection mode with a system prompt.

## Results
- The authors claim ReflexiCoder-8B establishes a new SOTA in the **1.5B-14B open-source model range**; in the single-attempt setting it achieves: **HumanEval 94.51%**, **HumanEval+ 87.20%**, **MBPP 81.80%**, **MBPP+ 78.57%**, **BigCodeBench 35.00%**, **LiveCodeBench 52.21%**, **CodeForces 37.34%**.
- Under the multi-round reflection setting, results improve further to: **HumanEval 95.73%**, **BigCodeBench 36.84%**, **LiveCodeBench 54.12%**, **CodeForces 37.68%**; the abstract does not provide multi-round MBPP values.
- In comparison with proprietary models, the paper explicitly reports: on **HumanEval+**, ReflexiCoder reaches **87.20%**, tying **GPT-5.1 at 87.20%**; on **LiveCodeBench**, ReflexiCoder at **52.21%** exceeds **GPT-5.1 at 48.03%**; on **CodeForces**, ReflexiCoder at **37.34%** exceeds **GPT-5.1 at 34.70%**.
- The paper also claims more efficient inference: in multi-round mode, compared with the base model, **inference token overhead is reduced by about 40%**, with **reasoning tokens reduced by nearly 50%**.
- At the behavioral level, the authors say the model exhibits a highly disciplined reflection pattern: it **almost always performs exactly 1 reflection cycle**, implying that its gains do not mainly come from unbounded multi-round sampling, but from learned efficient self-correction.

## Link
- [http://arxiv.org/abs/2603.05863v1](http://arxiv.org/abs/2603.05863v1)
