---
source: arxiv
url: http://arxiv.org/abs/2603.09249v1
published_at: '2026-03-10T06:26:24'
authors:
- Jincenzi Wu
- Yuxuan Lei
- Jianxun Lian
- Yitian Huang
- Lexin Zhou
- Haotian Li
- Xing Xie
- Helen Meng
topics:
- social-reasoning
- theory-of-mind
- reinforcement-learning
- process-supervision
- adversarial-benchmark
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Social-R1: Towards Human-like Social Reasoning in LLMs

## Summary
This paper proposes Social-R1, a reinforcement learning framework for social reasoning in large language models, and constructs the adversarial benchmark ToMBench-Hard to expose the problem of models that “appear to reason but actually rely on shortcuts.” The core claim is that using harder data and aligning the entire reasoning trajectory can improve robust social intelligence more effectively than simply scaling model size.

## Problem
- The paper addresses the tendency of LLMs in social reasoning / theory-of-mind tasks to rely on surface patterns and answer backtracking, rather than genuinely inferring others’ beliefs, intentions, emotions, and goals from narrative cues.
- This matters because social intelligence is a key capability for human-AI collaboration, trustworthy assistants, and AI that truly serves human needs; if models only know how to “apply templates,” they will fail significantly under adversarial perturbations or out-of-distribution scenarios.
- The authors also point out that existing evaluations often overestimate capability: models are close to human performance on simple benchmarks, but under harder narrative settings with adversarial perturbations they exhibit “shortcut illusions” and distorted reasoning logic.

## Approach
- Construct **ToMBench-Hard**: 800 expert-annotated adversarial multiple-choice questions based on 6 dimensions of social intelligence (Belief, Desire, Emotion, Intention, Knowledge, Non-literal Communication), with perturbations such as perceptual access, information asymmetry, and second-order beliefs specifically designed so models cannot game the task through lexical matching.
- Propose **Social-R1**: instead of rewarding only whether the final answer is correct, it uses reinforcement learning to align the **entire reasoning process**, encouraging the model to think in stages more like humans.
- Specifically, the reward is divided into four categories: format reward $R_{fmt}$, outcome reward $R_{out}$, structure reward $R_{struct}$, and content reward $R_{content}$, then multiplied by a length/repetition control reward $R_{len}$.
- The structure reward uses the four-stage Social Information Processing (SIP) framework to constrain reasoning order: first encode social cues, then interpret mental states, then clarify goals, and finally generate a response; the content reward checks whether each step is truly supported by story evidence; the length reward suppresses repetition and overly long reasoning.
- Training uses curriculum-style weight scheduling and GRPO; additionally, a content reward model is trained on SocialPairs-20K preference data to learn to assess the quality of intermediate reasoning segments.

## Results
- **ToMBench-Hard reveals the fragility of existing models**: human experts achieve **0.89** accuracy on ToMBench-Hard; DeepSeek-R1 **0.61**, O3 **0.59**, GPT-5 **0.56**, Qwen3-32B **0.52**, and Qwen3-8B **0.34**. But on the easier ToM-RL benchmark, DeepSeek-R1/O3/GPT-5 score **0.87/0.88/0.87**, showing that simple benchmarks clearly overestimate social reasoning ability.
- **Small models surpass large models**: SocialR1-4B Full achieves an overall score of **0.6880** across 8 benchmarks, higher than Qwen3-4B’s **0.5822** (+**0.1058**), as well as LLaMa3.1-70B’s **0.6111** (+**0.0769**) and LLaMa3.1-70B_COT’s **0.6496** (+**0.0384**).
- **The 8B model matches or exceeds larger or closed-source baselines**: SocialR1-8B Full reaches **0.7270** overall, exceeding Qwen3-8B **0.5877** (+**0.1393**), Qwen3-32B **0.6624** (+**0.0646**), Distill-Llama-70B **0.6886** (+**0.0384**), DeepSeek-R1 **0.7073** (+**0.0197**), and GPT-5 **0.6956** (+**0.0314**), though it still trails O3’s **0.7447**.
- **Best per-task results**: SocialR1-8B Full achieves **0.6279** on ToMBench-Hard Val, **0.9675** on SimpleToM, **0.7010** on EmoBench, **0.7083** on Hi-ToM, and **0.5079** on TactfulToM; SocialR1-4B Full reaches **0.4846** on ToMBench-Hard Val, significantly above Qwen3-4B’s **0.3403**.
- **The reward model is effective**: the content reward model reaches **89.2%** accuracy on an automatic test set of 2k pairs, and **87.5%** agreement with human labels on a manually calibrated subset of 200 pairs.
- **The training setup is specific and relatively parameter-efficient**: using only **700** training samples and **100** test samples, the authors conduct **600** RL training steps on Qwen3-4B/8B; the conclusion emphasizes that the “quality of the reasoning trajectory” is more important than parameter scaling alone.

## Link
- [http://arxiv.org/abs/2603.09249v1](http://arxiv.org/abs/2603.09249v1)
