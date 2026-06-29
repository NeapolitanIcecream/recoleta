---
source: arxiv
url: https://arxiv.org/abs/2606.18632v1
published_at: '2026-06-17T03:03:16'
authors:
- Zhuowen Yin
- Chongyang Liu
- Wenzhang Yang
- Renjue Li
- Yinxing Xue
topics:
- embodied-foundation-models
- robot-safety
- vision-language-action
- synthetic-data
- hazard-benchmark
- refusal-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# ROBOSHACKLES: A Safety Dataset for Human-Injury Prevention in Embodied Foundation Models

## Summary
RoboShackles is a synthetic safety dataset for testing whether embodied foundation models refuse robot actions that could injure people. It builds 10,000 hazardous robot video clips from real DROID observations and finds that six tested EFMs produce unsafe actions in every tested category.

## Problem
- EFMs can turn model outputs into physical robot actions, so a bad answer can cause direct injury or create a household hazard.
- Real videos of robots harming people or causing dangerous situations cannot be collected safely or ethically, which leaves little data for injury-prevention training and evaluation.
- Existing EFM safety work often tests attacks or control constraints, but gives limited coverage of direct harm and delayed hazards such as fire, water overflow, electric shock, and falling objects.

## Approach
- The pipeline starts with real DROID robot observations, using about 90,000 filtered third-person robot clips as source material.
- Qwen3-VL analyzes each scene and writes category-specific image-editing instructions; Qwen-Image edits the initial frame to add a safety-critical state.
- Qwen3-VL then writes a temporal video prompt, and Wan2.7 generates the future robot rollout in one pass from the edited frame and prompt.
- Human reviewers filter out samples with severe artifacts, wrong labels, implausible robot motion, object identity drift, or prompt-video mismatch.
- The evaluation uses a strict refusal rule: a model is safe only if it refuses the instruction or produces no executable action.

## Results
- RoboShackles contains 10,000 robot video clips across 6 categories: 2 direct-harm categories, hand and human, and 4 indirect-harm categories, fire, electrical, water, and falling risk.
- The test set has 1,200 samples, with 200 samples per category.
- Automatic video checks report PSP = 1.000 and TAC = 1.000 for all 6 categories; RSS = 1.000 for all 6 categories; MSS ranges from 0.946 for electrical hazards to 1.000 for hand and human direct harm.
- Motion amplitude varies by category: robot MA-R ranges from 0.184 for hand harm to 0.491 for human harm; object MA-O ranges from 0.122 for water safety to 0.403 for human harm.
- Six evaluated EFMs, Cosmos-Policy, DreamZero, LingBot-VA, FastWAM, VLA-JEPA, and World Guidance, each have a 100% unsafe action generation rate in all 6 categories.
- The excerpt gives no quantitative post-training safety improvement, so the strongest measured claim is the benchmark result that all tested models fail the refusal-based safety criterion on this dataset.

## Link
- [https://arxiv.org/abs/2606.18632v1](https://arxiv.org/abs/2606.18632v1)
