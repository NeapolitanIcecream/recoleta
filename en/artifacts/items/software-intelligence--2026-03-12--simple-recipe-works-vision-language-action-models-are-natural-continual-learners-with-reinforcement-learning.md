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
- continual-learning
- reinforcement-learning
- vision-language-action
- lora
- embodied-ai
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Simple Recipe Works: Vision-Language-Action Models are Natural Continual Learners with Reinforcement Learning

## Summary
This paper shows that applying **Sequential Fine-Tuning (Seq. FT) + LoRA + on-policy RL** to large pretrained vision-language-action models is surprisingly naturally stable in continual reinforcement learning: it not only exhibits almost no forgetting, but also often outperforms more complex continual learning methods.

## Problem
- The paper aims to solve the following problem: **when vision-language-action (VLA) models perform continual reinforcement learning on newly arriving tasks, how can they learn new tasks without forgetting old ones**.
- This matters because real robots/embodied agents operate in **open, changing environments** and need to continuously improve themselves, rather than relying only on fixed capabilities trained once offline.
- Traditional continual learning wisdom holds that directly applying sequential fine-tuning causes **catastrophic forgetting**, so complex mechanisms such as replay, regularization, and parameter isolation are usually required; however, these methods often sacrifice adaptation to new tasks and increase training cost.

## Approach
- The authors systematically compare **8 classes of continual reinforcement learning methods**, covering regularization, replay, parameter isolation, and methods tailored to large-model adaptation, and compare them against **sequential fine-tuning** and a **multitask joint-training oracle**.
- The experiments use a unified training recipe of **large pretrained VLA + LoRA parameter-efficient fine-tuning + GRPO on-policy reinforcement learning** in order to fairly study “why a simple method is strong enough.”
- At the core-mechanism level, the method is actually very simple: **as tasks arrive one after another, they continue training the same pretrained VLA only on the current task, while updating only a small number of LoRA parameters**; the authors find that this does not significantly damage prior knowledge.
- The authors further analyze and argue that the source of stability is the synergy of three components: **large-scale pretrained models** provide robust representations, **LoRA** constrains the magnitude/subspace of updates, and **on-policy RL** brings more controlled policy updates; removing any one of these significantly increases forgetting.

## Results
- On **libero-spatial**, Seq. FT achieves **AVG 81.2±0.4**, outperforming EWC **66.1±0.9**, DER **73.4±1.3**, SLCA **69.9±0.7**, and RETAIN **66.0±0.7**, while approaching the multitask oracle at **85.8±0.2**; its forgetting is **NBT 0.3±0.5**, and its zero-shot success rate **ZS 57.1±1.1** is even higher than the oracle’s **51.2±0.7**.
- On **libero-object**, Seq. FT reaches **AVG 93.2±0.7**, higher than EWC **82.6±1.2**, Expert Replay **88.8±0.2**, DER **89.1±0.2**, SLCA **84.1±0.7**, and RETAIN **76.6±0.3**, and close to the oracle at **95.7±0.7**; forgetting is only **NBT 1.0±0.7**, with **FWT 7.1±0.8** and **ZS 25.4±0.2**.
- On **libero-long-horizon**, Seq. FT achieves **AVG 89.8±0.9**, close to the oracle at **90.5±0.8**, and better than EWC **86.6±0.3**, DER **87.6±0.4**, and RETAIN **86.2±0.9**; its **NBT -2.4±1.0** implies almost no forgetting and even improvement on old tasks, while **ZS 86.6±0.2** is also strong.
- Across the three major benchmarks, the authors claim that Seq. FT typically has forgetting **below 2%**, and sometimes even negative forgetting; by contrast, many complex CRL methods reduce plasticity by constraining updates, and replay methods additionally require extra storage and access to old data, yet **do not deliver better results**.
- The paper also claims that this phenomenon persists under **multiple controlled perturbations** (changes in environment parameters, different model/physics domains, and task-order changes), but the full numerical results for these extended experiments are not provided in the current excerpt.

## Link
- [http://arxiv.org/abs/2603.11653v1](http://arxiv.org/abs/2603.11653v1)
