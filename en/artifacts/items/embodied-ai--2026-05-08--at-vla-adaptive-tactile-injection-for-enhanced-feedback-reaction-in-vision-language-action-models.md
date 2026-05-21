---
source: arxiv
url: https://arxiv.org/abs/2605.07308v2
published_at: '2026-05-08T06:17:08'
authors:
- Xiaoqi Li
- Muhe Cai
- Jiadong Xu
- Juan Zhu
- Hongwei Fan
- Yan Shen
- Guangrui Ren
- Hao Dong
topics:
- vision-language-action
- tactile-feedback
- contact-rich-manipulation
- robot-foundation-model
- closed-loop-control
- dexterous-manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models

## Summary
AT-VLA adds gated tactile feedback to a pretrained vision-language-action robot policy so it can handle contact-rich manipulation without hurting pre-contact visual grounding. It uses a slow vision-language stream and a fast tactile stream to react to touch within 0.04 s.

## Problem
- Pretrained VLA models often fail in tasks where force and contact shape the next action, such as unzipping a bag, stamping, wiping a curved vase, and unscrewing a lid.
- Tactile data is rare in large robot pretraining datasets, and adding tactile tokens during finetuning can shift attention away from the target object.
- Standard VLA inference is too slow for high-frequency tactile correction during closed-loop contact.

## Approach
- The model builds on GO-1, a pretrained VLA using InternVL-2B and a DiT action expert, and adds a lightweight MLP tactile encoder for 3D normal and 3D tangential force signals.
- A learned tactile gate predicts contact versus non-contact from tactile tokens, trained with binary cross-entropy on manually labeled contact states; a 0.5 threshold activates tactile input.
- Adaptive cross attention keeps the original state-token query when there is no contact, then switches the query to the tactile token during contact while keeping the action expert shape unchanged.
- A dual-stream design runs vision-language reasoning at low frequency and tactile action correction at high frequency; inference uses a 3:1 fast-to-slow ratio.
- Training uses action loss plus 0.01 times the tactile gate loss.

## Results
- Real-robot tests use AgiBot Genie1 with 30-50 demonstrations per task and 15 trials per task across four contact-rich tasks and two non-contact tasks.
- Overall success improves over GO-1 and pi_0.5 on contact-rich tasks: Unzip Bag 0.33 vs 0.20 and 0.00; Stamp 0.46 vs 0.13 and 0.20; Wipe Vase 0.67 vs 0.07 and 0.33; Unscrew Lid 0.53 vs 0.27 and 0.46.
- Against tactile baselines on contact-stage performance, AT-VLA reaches Unzip Full 0.33 vs VTLA 0.00 and RDP 0.06, Wipe Full 0.67 vs 0.60 and 0.33, and Stamp Place 0.46 vs 0.13 and 0.40.
- On Unscrew Rotate, AT-VLA scores 0.53, below VTLA 0.80 and RDP 0.87; the paper says those baselines start from an ideal manually set grasp while AT-VLA must complete the full task.
- In the modality-missing test, the same AT-VLA weights without tactile input score Pick Place 1.0, Open Drawer 0.93, Stamp 0.20, and average 0.70; with tactile input they score Stamp 0.46 and average 0.79.
- The paper reports closed-loop tactile reaction within 0.04 s.

## Link
- [https://arxiv.org/abs/2605.07308v2](https://arxiv.org/abs/2605.07308v2)
