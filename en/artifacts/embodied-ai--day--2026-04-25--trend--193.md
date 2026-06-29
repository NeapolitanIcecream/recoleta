---
kind: trend
trend_doc_id: 193
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
topics:
- robotics
- vision-language-action
- tactile sensing
- low-data post-training
- steerability
run_id: materialize-outputs
aliases:
- recoleta-trend-193
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/tactile-sensing
- topic/low-data-post-training
- topic/steerability
language_code: en
pass_output_id: 108
pass_kind: trend_synthesis
---

# Robot adaptation work is getting more grounded in contact and instruction control

## Overview
This day is tightly focused on robot adaptation that survives real deployment constraints. One paper adds tactile and torque signals to VLA policies and nearly doubles average success on contact-heavy tasks. Another shows that small post-training sets can preserve instruction following if the model protects pretrained visual grounding and uses prompt guidance at inference.

## Clusters

### Physical feedback becomes a practical VLA input
MoSS makes the day's strongest empirical case for adding physical feedback directly into vision-language-action models. It keeps tactile and torque inputs in separate streams, then lets them interact with the action model through shared attention. On four real robot tasks, the full model lifts GR00T N1.5 from 20.8% average success to 49.0%, and pi_0 from 26.1% to 45.9%. The reported overhead is small at 1.11x for the dual-signal setup. The task mix matters here: cup unstacking, egg pick-and-place, board erase, and plug insertion all depend on contact cues that vision alone can miss.

#### Evidence
- [Modular Sensory Stream for Integrating Physical Feedback in Vision-Language-Action Models](../Inbox/2026-04-25--modular-sensory-stream-for-integrating-physical-feedback-in-vision-language-action-models.md): Summary and headline results for tactile+torque integration into VLAs.

### Low-data adaptation is being judged by steerability, not just task fit
DeLock focuses on a narrower but important failure mode: low-data post-training can make a robot stop obeying new instructions after it learns a task. The paper keeps the visual encoder close to its pretrained state during fine-tuning, then uses Contrastive Prompt Guidance (CPG) at test time to bias action generation toward a new prompt. In 8 tasks with 20 trials each, it posts 19/20 on two concept-lock tests and 11/20 to 14/20 on several spatial-lock tests. The gains over the low-data RETAIN baseline are large, including 19/20 versus 0/20 on T2 and 13/20 versus 1/20 on T8. Ablations also show that CPG is carrying much of the spatial generalization load.

#### Evidence
- [Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training](../Inbox/2026-04-25--breaking-lock-in-preserving-steerability-under-low-data-vla-post-training.md): Summary, method, and benchmark results for preserving steerability under low-data post-training.
