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
- llm-alignment
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Social-R1: Towards Human-like Social Reasoning in LLMs

## Summary
This paper proposes Social-R1, which uses harder social reasoning data and "process-level" reinforcement learning to teach large language models to reason about social situations more like humans, rather than guessing answers from superficial patterns. The core conclusion is that by aligning reasoning trajectories rather than only final answers, smaller models can outperform larger models on social intelligence tasks.

## Problem
- The paper addresses the problem that, on social reasoning/Theory-of-Mind tasks, LLMs often "appear capable but actually rely on shortcuts": models frequently guess the answer first and then justify it afterward, instead of genuinely inferring characters' mental states from story cues.
- This matters because social intelligence directly affects human-AI collaboration, understanding of human intentions and emotions, and the reliability of AI in open-ended settings; if models only do pattern matching, they fail under perturbations or out-of-distribution cases.
- The paper also argues that existing benchmarks are too easy, masking this brittleness: models perform near human level on simple ToM benchmarks, but their scores drop significantly on harder adversarial tests.

## Approach
- The authors first construct **ToMBench-Hard**: a benchmark of **800** expert-annotated, multiple-choice, adversarial Theory-of-Mind questions covering six social intelligence abilities: belief, desire, emotion, intention, knowledge, and non-literal communication, with quality ensured by three annotators.
- They then propose **Social-R1**: instead of rewarding only correct answers, it uses reinforcement learning to supervise the "entire reasoning process." It requires the model to proceed through the four stages of human Social Information Processing (SIP): first identify social cues, then interpret mental states, then clarify goals, and finally produce a response.
- The reward function is multi-dimensional: **structure reward** ensures reasoning unfolds by stage, **content reward** checks whether each step is supported by story evidence, **length/repetition reward** suppresses verbosity and repetitive thinking, and an additional format reward makes it easier to extract reasoning and answer.
- The content reward is provided by a separately trained reward model: trained on the **SocialPairs-20K** preference dataset and initialized from Qwen3-4B; during training, RL is applied to **Qwen3-4B/8B**, using **700** training samples, **100** test samples, **600** optimization steps, and running on **8×A100 80GB**.

## Results
- **ToMBench-Hard reveals a "shortcut illusion" in current models**: humans achieve about **0.89** accuracy on this benchmark; but **DeepSeek-R1 0.61, O3 0.59, GPT-5 0.56, Qwen3-32B 0.52, Qwen3-8B 0.34**. By contrast, these models score **0.71–0.88** on the easier **ToM-RL**, showing that high scores on older benchmarks do not equal genuine social reasoning.
- **SocialR1-4B Full** reaches **Overall=0.6880** across 8 benchmarks, clearly above the original **Qwen3-4B 0.5822**, an improvement of **+0.1058**; it also exceeds **LLaMa3.1-70B 0.6111** and **LLaMa3.1-70B_COT 0.6496**, and is slightly below/close to **Distill-Llama-70B 0.6886**.
- **SocialR1-8B Full** reaches **Overall=0.7270**, above **Qwen3-8B 0.5877** (an improvement of **+0.1393**), and also surpasses **DeepSeek-R1 0.7073, GPT-5 0.6956, O3_COT 0.7163, Qwen3-32B 0.6624, Distill-Llama-70B 0.6886**, showing that an 8B model can outperform larger or stronger baselines through training methodology.
- By task, **SocialR1-8B Full** delivers the best or near-best results on metrics including **ToMBench-Hard Val 0.6279**, **SimpleToM 0.9675**, **EmoBench 0.7010**, **Hi-ToM 0.7083**, and **TactfulToM 0.5079**; for example, on **SimpleToM** it outperforms **DeepSeek-R1 0.7187** and **Qwen3-32B 0.7634**.
- The reward model itself also has measurable quality: the content reward model achieves **89.2%** accuracy on an automatic test set of **2k pairs**, and **87.5%** agreement with human labels on a human-calibrated subset of **200 pairs**.
- Ablations show that "process-level rewards" are effective overall: for 4B, **only R_out=0.6332**, while **Full=0.6880**; for 8B, **only R_out=0.7004**, **Full=0.7270**. This indicates that rewarding only the final answer is less effective than jointly constraining structure, content, and efficiency.

## Link
- [http://arxiv.org/abs/2603.09249v1](http://arxiv.org/abs/2603.09249v1)
