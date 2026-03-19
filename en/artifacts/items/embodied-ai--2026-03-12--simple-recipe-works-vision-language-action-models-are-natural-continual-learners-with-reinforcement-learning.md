---
source: arxiv
url: http://arxiv.org/abs/2603.11653v1
published_at: '2026-03-12T08:22:39'
authors:
- Jiaheng Hu
- Jay Shim
- Chen Tang
- Yoonchang Sung
- Bo Liu
- Peter Stone
- Roberto Martin-Martin
topics:
- vision-language-action
- continual-reinforcement-learning
- lora
- robot-foundation-model
- on-policy-rl
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning

## Summary
This paper systematically studies the performance of large pretrained Vision-Language-Action (VLA) models in continual reinforcement learning. Its core conclusion is that seemingly simple Sequential Fine-Tuning (Seq. FT), combined with LoRA and on-policy RL, is often already stable enough, scalable, and stronger than more complex continual learning methods. This challenges the conventional wisdom that “sequential training inevitably causes catastrophic forgetting,” and is important for building robot foundation models capable of sustained self-improvement.

## Problem
- The paper addresses the question: **when tasks arrive continuously, can VLA models learn new tasks while retaining old capabilities and zero-shot generalization, without suffering catastrophic forgetting**.
- This matters because real robotic environments are open-ended and constantly changing. If robot foundation models cannot adapt continually, they are unlikely to become truly long-term usable embodied agents.
- Traditional continual learning generally assumes that directly applying sequential fine-tuning leads to severe forgetting, thus requiring complex mechanisms such as replay, regularization, and parameter isolation. The authors question whether this still holds in the setting of “large pretrained VLA + RL post-training.”

## Approach
- The authors conduct a systematic comparison across **3 different VLA models and 5 continual RL benchmarks**, evaluating 8 methods: Seq. FT, multitask oracle, EWC, Expert Replay, Dark Experience Replay, Dynamic Weight Expansion, SLCA, RETAIN.
- The base training recipe is simple: **freeze most of the pretrained backbone, use only LoRA for parameter-efficient adaptation, and perform RL post-training with on-policy GRPO**.
- Evaluation metrics include average success rate on training tasks **AVG**, forgetting **NBT**, forward transfer **FWT**, and **ZS (zero-shot success)**, which specifically measures retention of pretrained generalization ability.
- The authors further analyze the mechanism and argue that performance comes from the synergy of three components: **large-scale pretraining provides strong initial representations, LoRA restricts update magnitude to reduce interference, and on-policy RL makes updates more stable**; removing any one of these significantly increases forgetting.

## Results
- On **libero-spatial**, Seq. FT achieves **AVG 81.2±0.4%**, **NBT 0.3±0.5**, **FWT 3.9±1.5**, and **ZS 57.1±1.1%**; this is clearly better than EWC’s **66.1% AVG** and RETAIN’s **66.0% AVG**, close to the multitask oracle’s **85.8% AVG**, and **its ZS is even higher than the oracle’s (57.1% vs 51.2%)**.
- On **libero-object**, Seq. FT achieves **AVG 93.2±0.7%**, **NBT 1.0±0.7**, **FWT 7.1±0.8**, and **ZS 25.4±0.2%**; it outperforms EWC **82.6%**, SLCA **84.1%**, and RETAIN **76.6%**, and is close to the oracle **95.7%**. Expert Replay has slightly higher ZS (**26.7%**), but its AVG is still lower than Seq. FT (**88.8% vs 93.2%**).
- On **libero-long-horizon**, Seq. FT achieves **AVG 89.8±0.9%**, **NBT -2.4±1.0**, **FWT 0.5±0.1**, and **ZS 86.6±0.2%**; it is nearly on par with the oracle’s **90.5% AVG**, and shows **negative forgetting** (older tasks actually improve).
- Overall, the authors claim that forgetting under Seq. FT is very small, with **NBT below about 2% on multiple benchmarks and sometimes negative**, contrary to the classic conclusion that “sequential fine-tuning causes severe catastrophic forgetting.”
- Compared with complex CRL methods, the authors argue that these methods often introduce stability constraints that hurt plasticity: for example, EWC, SLCA, and RETAIN have substantially lower AVG on multiple benchmarks; although DWE almost never forgets (e.g. **NBT 0.0**), its forward transfer is **0.0**, indicating difficulty in leveraging positive transfer across tasks; replay methods also depend on extra storage and old data.
- The text also notes that the authors observed similar trends under environment perturbations, across different models/physics engines, and under changes in task order, but the **full numerical results are not all provided** in the given excerpt; the strongest concrete claim is that **the combination of large pretrained VLA + LoRA + on-policy RL makes simple sequential fine-tuning a natural continual learner**.

## Link
- [http://arxiv.org/abs/2603.11653v1](http://arxiv.org/abs/2603.11653v1)
