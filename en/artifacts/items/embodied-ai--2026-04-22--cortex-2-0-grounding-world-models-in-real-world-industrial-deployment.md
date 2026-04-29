---
source: arxiv
url: http://arxiv.org/abs/2604.20246v1
published_at: '2026-04-22T06:49:12'
authors:
- Adriana Aida
- Walid Amer
- Katarina Bankovic
- Dhruv Behl
- Fabian Busch
- Annie Bhalla
- Minh Duong
- Florian Gienger
- Rohan Godse
- Denis Grachev
- Ralf Gulde
- Elisa Hagensieker
- Junpeng Hu
- Shivam Joshi
- Tobias Knobloch
- Likith Kumar
- Damien LaRocque
- Keerthana Lokesh
- Omar Moured
- Khiem Nguyen
- Christian Preyss
- Ranjith Sriganesan
- Vikram Singh
- Carsten Sponner
- Anh Tong
- Dominik Tuscher
- Marc Tuscher
- Pavan Upputuri
topics:
- world-model
- vision-language-action
- industrial-robotics
- long-horizon-manipulation
- cross-embodiment
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Cortex 2.0: Grounding World Models in Real-World Industrial Deployment

## Summary
Cortex 2.0 adds world-model planning to an industrial vision-language-action robot policy. It predicts several possible future trajectories, scores them for progress, risk, and task completion, then executes the best one to improve long-horizon manipulation in cluttered warehouse settings.

## Problem
- Standard vision-language-action policies choose the next action from the current observation and do not evaluate future outcomes, which makes them brittle on long-horizon tasks where errors compound.
- Industrial manipulation has heavy clutter, occlusion, reflective materials, contact-rich interactions, and shifting object distributions, so a single bad action can disrupt the whole workflow.
- The paper targets reliable execution across tasks and embodiments such as single-arm and dual-arm systems in real deployment conditions.

## Approach
- The system keeps a hierarchical VLA stack, then adds a visual-latent world model that rolls out `k` candidate future trajectories over a planning horizon before acting.
- A frozen Process-Reward Operator (PRO), trained on real deployment trajectories, scores each imagined rollout with three signals: task progress, failure risk, and completion likelihood. The score is `S = progress - λ*risk + β*success`.
- The policy selects the highest-scoring rollout and conditions a 2B-VLM flow-matching action head on that chosen future to generate an action chunk.
- Planning happens in visual latent space rather than robot-specific action space, so the same planning loop can transfer across embodiments; robot-specific action mapping is handled by lightweight adapters.
- Training uses internet-video pretraining for the world model, then fine-tuning on deployment recordings at 30 Hz, plus open-source robot datasets, teleoperation data, synthetic data, and a curated subset of 10 million deployment interactions.

## Results
- The paper claims Cortex 2.0 achieves the best success rates across all four evaluated real-world tasks: pick-and-place, item and trash sorting, screw sorting, and shoebox unpacking.
- It reports consistent gains over state-of-the-art reactive VLA baselines on both single-arm and dual-arm platforms.
- It states the system works with zero human interventions during benchmark evaluation.
- The excerpt does not provide task-by-task quantitative metrics, exact success-rate numbers, or named baseline scores, so the magnitude of improvement cannot be verified from the provided text.
- Concrete scale claims in the training setup include `>10M` deployment episodes, `>25k` deployment hours in the curated training corpus, about `40k` teleoperation episodes, about `970k` open-source episodes, and a fleet history of over `500M` manipulation interactions collected at `30 Hz`.

## Link
- [http://arxiv.org/abs/2604.20246v1](http://arxiv.org/abs/2604.20246v1)
