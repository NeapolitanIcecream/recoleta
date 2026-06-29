---
source: arxiv
url: https://arxiv.org/abs/2606.23617v1
published_at: '2026-06-22T17:12:50'
authors:
- Ulas Berk Karli
- Tesca Fitzgerald
topics:
- vision-language-action
- active-learning
- continual-learning
- robot-data-scaling
- imitation-learning
- uncertainty-estimation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# RECALL: Recovery Experience Collection for Active Lifelong Learning in Vision-Language-Action Models

## Summary
RECALL studies how to fine-tune Vision-Language-Action robot policies with fewer demonstrations by collecting recovery examples at high-uncertainty states. It finds that uncertainty-guided recovery data improves adaptation, while replay data is needed to prevent forgetting.

## Problem
- VLA policies often need fine-tuning after deployment to new task distributions, robots, or environments.
- Passive imitation learning waits for failures, then collects full demonstrations from task starts, which can spend expert time on states the policy already handles.
- Targeted recovery data can improve weak substeps, but training only on that narrow data can erase earlier skills.

## Approach
- The paper starts with a π0-FAST autoregressive VLA trained on LIBERO-10, then rolls it out to find states where the policy may need help.
- It uses INSIGHT, a token-level uncertainty and help-prediction method, to flag high-uncertainty states during rollouts.
- It collects recovery demonstrations from either the first uncertain state in a rollout, called online collection, or every uncertain state in a rollout, called offline collection.
- It compares these active recovery datasets against matched passive start-state demonstrations.
- It tests fine-tuning with new-only data, full replay, LIBERO-10 replay, targeted replay, lower learning rates, and elastic weight consolidation.

## Results
- Strong INSIGHT online recovery with full replay reaches 72.4% overall LIBERO-10 success, compared with 60.2% for matched passive collection and 59.8% for the original baseline; the active-vs-passive gain has p=0.0001.
- Online recovery reaches 72.4% overall success, while offline recovery reaches 68.4%; collected-task success is 49.2% online and 48.4% offline, with no significant overall difference reported at p=0.1659.
- New-only fine-tuning fails: the best Strong INSIGHT online new-only checkpoint reaches 28.4% overall success, 0.4% collected-task success, and 56.4% retained-task success. The replay version reaches 72.4% overall, 49.2% collected-task, and 95.6% retained-task success.
- Lower learning-rate new-only training reaches 62.8% overall success, 34.4% collected-task success, and 91.2% retained-task success. EWC with λ=10^12 reaches 61.4% overall, 32.0% collected-task, and 90.8% retained-task success.
- LIBERO-10 replay reaches 68.6% overall success, close to full replay at 72.4%, with p=0.1877. Targeted replay reaches 63.2% overall and drops retained-task success from 90.0% to 83.6% compared with LIBERO-10 replay, with p=0.0345.

## Link
- [https://arxiv.org/abs/2606.23617v1](https://arxiv.org/abs/2606.23617v1)
