---
source: arxiv
url: https://arxiv.org/abs/2605.08879v2
published_at: '2026-05-09T10:59:03'
authors:
- Tianyi Zhang
- Shaopeng Zhai
- Haoran Zhang
- Fuxian Huang
- Qi Zhang
topics:
- vision-language-action
- robot-foundation-model
- flow-matching
- catastrophic-forgetting
- supervised-fine-tuning
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Preserving Foundational Capabilities in Flow-Matching VLAs through Conservative SFT

## Summary
ConSFT is a supervised fine-tuning loss for flow-matching VLA robot policies that reduces catastrophic forgetting during task adaptation. It keeps target-task success close to vanilla SFT while retaining more prior robot skills, with no prior data, reference model, or architecture change.

## Problem
- Vanilla SFT on narrow robot demonstrations can overwrite many parameters and erase pre-trained skills in spatial reasoning, object handling, and bimanual control.
- Existing fixes are costly or restrictive: Experience Replay needs prior data, regularization needs a parallel reference model, and LoRA can limit adaptation capacity.
- This matters because robot foundation models need to adapt to new tasks without losing skills learned during large-scale pre-training.

## Approach
- ConSFT uses the per-sample flow-matching SFT loss as a confidence signal: high loss means the model is less confident on that transition.
- It multiplies the SFT loss by a stop-gradient weight, exp(-L_SFT/tau), so low-confidence samples produce smaller gradients.
- The temperature tau is annealed during training, so updates start conservative and later allow more target-task fitting.
- The mechanism copies the effect of PPO-style bounded updates inside supervised training, while avoiding action-likelihood ODE solves and parallel reference networks.
- The paper claims the forgetting risk under a Fisher quadratic scales as exp(-2L_SFT/tau) times the vanilla SFT risk.

## Results
- In a pi0 LIBERO ablation, PPO with clipping retained 0.39 average prior-task performance, versus 0.09 for SFT and 0.03 for PPO-NoClip; target LIBERO-Spatial success was 0.95 for PPO, 0.90 for SFT, and 0.87 for PPO-NoClip.
- The same ablation reports lower update volume with trust-region clipping: 15% of parameters changed versus 30% under unconstrained SFT, with >99% sparsity in core Attention and MLP weights.
- On LIBERO with pi0, ConSFT matched SFT on the target task at 0.90 success and improved average prior-task retention to 0.34 versus 0.09; Object retention was 0.32 versus 0.02, and Goal retention was 0.35 versus 0.16.
- On LIBERO with pi0.5, ConSFT matched SFT target success at 1.00 and raised average prior-task retention to 0.43 versus 0.23.
- On LIBERO with GR00T, ConSFT improved average prior-task retention to 0.59 versus 0.49 for SFT, while target success was lower at 0.63 versus 0.70.
- On RoboTwin with pi0, ConSFT reached 0.60 target success on RoboTwin-Indep. versus 0.55 for SFT, and retained 0.28 average prior-task success versus 0.14; RoboTwin-Coord. retention was 0.13 versus 0.00. The abstract also claims an average absolute retention gain of over 20% against vanilla SFT and about a 20% real-world success margin.

## Link
- [https://arxiv.org/abs/2605.08879v2](https://arxiv.org/abs/2605.08879v2)
