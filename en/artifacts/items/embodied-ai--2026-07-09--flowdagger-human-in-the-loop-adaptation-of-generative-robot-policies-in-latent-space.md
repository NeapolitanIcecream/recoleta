---
source: arxiv
url: https://arxiv.org/abs/2607.08877v1
published_at: '2026-07-09T19:07:33'
authors:
- Michael Murray
- Daphne Chen
- Simran Bagaria
- Dean Fortier
- Tess Hellebrekers
- Galen Mullins
- Harshavardhan Gajarla
- Oier Mees
- Maya Cakmak
- Andrey Kolobov
topics:
- robot-foundation-model
- generative-robot-policy
- human-in-the-loop
- latent-space-adaptation
- vision-language-action
- world-action-model
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space

## Summary
FlowDAgger adapts frozen generative robot policies with sparse human corrections by converting corrective actions into latent noise targets. It improves task success while retaining the base policy's pretrained skills and requires only a small trainable controller.

## Problem
- Generative robot policies fail on objects, dynamics, embodiments, and edge cases outside their training data.
- Collecting demonstrations, fine-tuning large models, and running reinforcement learning on physical robots require substantial data, compute, or risk.
- Action-space corrections can push behavior outside the base policy's reliable support, while weight updates can damage unrelated skills.

## Approach
- For each human correction, action inversion runs the frozen policy's generative process backward to find the noise vector that would reproduce the expert action.
- A small observation-to-noise policy learns these inverted targets; deployment feeds its predicted noise into the frozen base policy.
- The method uses per-step fixed-point inversion, with 5 iterations per step, to handle few-step flow-matching action heads.
- For world-action models such as Cosmos-Policy, it inverts the joint latent process while changing only the action frame and preserving predicted state and value frames.
- Training mixes inverted intervention data with noise from successful autonomous rollouts to preserve existing behavior.

## Results
- On 12 MetaWorld tasks with pi_0.5, FlowDAgger reached a mean success rate of 0.78, improving the frozen base from 0.53 by +0.25 after a matched budget of 50 rollouts; SFT reached 0.71, LoRA-DAgger 0.68, Residual-DAgger 0.64, and DSRL 0.55.
- FlowDAgger won on 8 of 12 MetaWorld tasks and achieved 1.00 success on Coffee Pull and Stick Push, 0.99 on Hand Insert, and 0.89 on Assembly.
- Across a shared seven-task MetaWorld set, mean success improved from 0.53 to 0.79 with pi_0.5 and from 0.53 to 0.74 with Cosmos-Policy, a world-action model; the corresponding gains were +0.26 and +0.21.
- In the Hammer adaptation test, success rose from 0.40 to 0.84, while mean performance on five held-out tasks was 0.88 versus 0.96 for the unadapted base; Residual-DAgger fell to 0.69 on those held-out tasks.
- The method trains only the small noise policy, fits within about 8 GB of VRAM in the reported pi_0.5 setup, and the excerpt claims successful evaluation on simulated tasks plus real-world single-arm and bimanual manipulation.
- The provided excerpt does not include complete quantitative results for the real-world experiments.

## Link
- [https://arxiv.org/abs/2607.08877v1](https://arxiv.org/abs/2607.08877v1)
