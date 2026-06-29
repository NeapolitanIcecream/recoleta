---
source: arxiv
url: https://arxiv.org/abs/2606.25985v1
published_at: '2026-06-24T15:53:43'
authors:
- Tiecheng Guo
- Meng Guo
topics:
- vision-language-action
- robot-control
- asynchronous-control
- action-adapter
- robot-manipulation
- delay-compensation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models

## Summary
ACNet adapts chunked VLA robot policies for asynchronous execution by feeding the motion already executed during inference delay into the action head. It aims to reduce chunk-handoff jitter without retraining the full backbone.

## Problem
- Large VLA backbones and generative action heads add inference latency, which makes synchronous robot control pause between action chunks.
- Asynchronous execution removes idle waiting, but the next chunk is predicted from a stale observation while the robot keeps moving.
- Directly stitching chunks can cause action jumps, jitter, and contact failures; full delay-conditioned retraining is costly for large pretrained policies.

## Approach
- The paper treats the executed motion during inference delay as the key boundary signal for the next action chunk.
- ACNet takes the executed suffix of the previous chunk, called the delay action, and pads it to the full action horizon with learnable tokens.
- A small transformer encodes this delay action, then projection layers inject it as a residual into the mostly frozen action head.
- The perception-language backbone stays frozen, and the adapter is designed for generative action heads such as diffusion and flow matching.
- Training samples different delays and reuses cached visual-language latents, so delay coverage does not require repeated full-backbone passes.

## Results
- On Kinetix, ACNet reaches 0.79 average success for delayed settings d>0, compared with 0.61 for Naïve Async, 0.72 for RTC, and 0.80 for Training-RTC.
- On Kinetix, ACNet trains about 20% of model parameters, while Training-RTC updates 100%.
- On Meta-World MT50 with H=50 and delays d=0,5,10,15, ACNet gets 0.74 average success, matching Training-RTC at 0.74 and exceeding Naïve Async at 0.70 and RTC at 0.71.
- On Meta-World MT50, ACNet reports 91 ms latency and 11.0 Hz control frequency, compared with RTC at 159 ms and 6.28 Hz, and Training-RTC at 134 ms and 7.46 Hz. The paper states this latency gain mainly comes from the Evo-1 backbone used by ACNet rather than the adapter alone.
- On a real SO-ARM101 setup with 50 training rollouts and 10 trials per task, ACNet succeeds in 20/20 trials across two tasks, compared with 17/20 for Naïve Async.
- Jerk plots on Meta-World nut-assembly-v3 and plate-slide-back-v3 with H=50 and d=10 show smoother chunk transitions for ACNet, but the excerpt does not provide numeric jerk values.

## Link
- [https://arxiv.org/abs/2606.25985v1](https://arxiv.org/abs/2606.25985v1)
