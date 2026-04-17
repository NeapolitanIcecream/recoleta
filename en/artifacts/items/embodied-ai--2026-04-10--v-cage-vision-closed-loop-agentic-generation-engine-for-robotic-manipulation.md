---
source: arxiv
url: http://arxiv.org/abs/2604.09036v1
published_at: '2026-04-10T06:56:17'
authors:
- Yaru Liu
- Ao-bo Wang
- Nanyang Ye
topics:
- vision-language-action
- robot-data-scaling
- sim2real
- synthetic-data-generation
- long-horizon-manipulation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation

## Summary
V-CAGE is a data generation pipeline for robotic manipulation that builds simulation scenes, executes tasks, checks them with a vision-language model, and compresses the resulting videos. The paper targets long-horizon Vision-Language-Action training, where bad scene layouts and undetected execution errors can poison large synthetic datasets.

## Problem
- VLA models need large manipulation datasets, but real data collection is expensive and misses many long-tail cases.
- Existing synthetic pipelines often place objects without enough task context, which causes collisions, occlusion, or unreachable targets.
- Many systems run in open loop: code finishes without runtime errors, but the task can still fail visually, and those silent failures contaminate long-horizon training data.

## Approach
- V-CAGE uses an agentic pipeline built on OpenClaw to turn a language task into a usable simulation scene and verified manipulation trajectory.
- Its Inpainting-Guided Scene Construction first selects relevant assets, places them without collisions, writes a semantic layout plan, then uses image inpainting to rearrange objects into a task-aware scene.
- It recovers object positions from the edited image with Grounding DINO and DINOv2 matching, then refines coordinates with constrained optimization to remove collisions while keeping the intended layout.
- It searches for executable subtasks from predefined manipulation templates using object metadata such as grasp points and functional points, instead of generating all robot code from scratch.
- After execution, Gemini 3 checks each subtask from visual observations; any failed step causes the whole trajectory to be rejected. The pipeline also compresses videos with action-aware keyframe selection and HEVC CRF tuning under a 0.1 JOD perceptual loss threshold.

## Results
- For long-horizon policy learning, the paper fine-tunes a **π0.5** VLA model on **4 tasks** with **100 synthetic expert trajectories per task** and evaluates over **100 trials per task**.
- Zero-shot pre-train success is **0% on all 4 tasks**. After training on raw synthetic data, success rates are **54%** on **AutoCheckout**, **54%** on **PackBreads**, **100%** on **PackStationery**, and **25%** on **SortToCabinet**.
- Training on compressed data gives similar results: **52%**, **50%**, **100%**, and **28%** on the same tasks, which supports the claim that compression preserves training utility.
- In Sim2Real on **ALOHA-AgileX**, using **10 real demos** alone gives **20%** success over **20 trials**. Co-training with **10 real + 250 simulated trajectories** raises success to **55%**, an absolute gain of **35 points**.
- The compression method claims **over 90%** reduction in file size; Figure 1 and the method section report about **93%** while keeping perceptual loss below **0.1 JOD**.
- The excerpt does not provide standalone ablation numbers for IGSC or VLM verification beyond these end-task results, though the paper claims they improve scene feasibility and remove silent-failure trajectories.

## Link
- [http://arxiv.org/abs/2604.09036v1](http://arxiv.org/abs/2604.09036v1)
