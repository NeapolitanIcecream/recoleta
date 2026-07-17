---
source: arxiv
url: https://arxiv.org/abs/2607.15275v1
published_at: '2026-07-16T17:59:06'
authors:
- Yunfan Jiang
- Yevgen Chebotar
- Ruijie Zheng
- Fengyuan Hu
- Yunhao Ge
- Jimmy Wu
- Tianyuan Dai
- Scott Reed
- Li Fei-Fei
- Yuke Zhu
- Linxi "Jim" Fan
topics:
- robot-foundation-model
- long-context-policy
- test-time-training
- vision-language-action
- dexterous-manipulation
- in-context-imitation
relevance_score: 0.99
run_id: materialize-outputs
language_code: en
---

# RoboTTT: Context Scaling for Robot Policies

## Summary
RoboTTT extends robot policy context to 8K timesteps by updating fast neural-network weights during training and inference. On real-robot bimanual assembly tasks, it improves long-horizon completion, supports one-shot imitation from human video, and adapts to failures without increasing inference latency with context length.

## Problem
- Most robot foundation models use single-step or short-history visuomotor inputs, limiting their ability to track progress, handle partial observability, imitate demonstrations, and recover during multi-stage tasks.
- The problem matters because long-horizon manipulation requires retaining task-relevant history while keeping inference computation practical.

## Approach
- RoboTTT adds Test-Time Training layers to the GR00T N1.7 Vision-Language-Action policy. Small fast-weight MLPs receive gradient updates at each timestep, compressing history into parameters that later observations can use.
- The model uses attention within each timestep and TTT layers across timesteps, allowing the fast-weight state to propagate while keeping inference latency constant with respect to total context length.
- Sequence action forcing samples an independent diffusion noise level for each action chunk, while truncated backpropagation through time carries fast weights across segments without storing activations for the full sequence.
- For adaptation, masked training makes demonstrations or robot failures serve as context and human actions serve as targets; this supports one-shot video imitation and the DAgger Distillation failure-to-correction procedure.

## Results
- On three real-robot YAM bimanual assembly tasks—Pup Go Car, Circuit, and Gear Bot—RoboTTT reached a 79% average task-completion score, versus 42% for single-step GR00T N1.7 and 56% for GDN; this is reported as an 87% improvement over the single-step baseline and a 41% improvement over GDN.
- RoboTTT produced 9/20, 13/20, and 2/10 fully successful trials on Pup Go Car, Circuit, and Gear Bot, respectively. It was the only evaluated method to fully complete Gear Bot, a five-minute, ten-stage assembly task, although it succeeded in only 2 of 10 trials.
- With 8K-timestep pretraining context, RoboTTT reached 71.5% average completion, compared with 43.9% for the same model pretrained at 1K timesteps and 45.6% for the best short-context baseline. The paper describes this as a 63% gain over 1K and a 57% gain over the short-context baseline; the abstract reports the first comparison as 62%, indicating a minor reporting discrepancy.
- In one-shot Circuit imitation from a single human video of an unseen configuration, RoboTTT achieved a 65% completion score and 6/10 successful rollouts, while GDN achieved 33% and 0/10.
- Under external perturbations, RoboTTT succeeded in 83% of trials versus 53% for the best short-context baseline, and DAgger Distillation produced 36% better performance than the same model without that on-the-fly improvement training.
- The evidence comes from three task families and fixed trial counts—20 trials per task, or 10 for Gear Bot—so the reported gains establish performance on these real-robot evaluations rather than universal superiority across robot platforms or tasks.

## Link
- [https://arxiv.org/abs/2607.15275v1](https://arxiv.org/abs/2607.15275v1)
