---
source: arxiv
url: https://arxiv.org/abs/2605.27461v1
published_at: '2026-05-25T20:46:22'
authors:
- Brian Zhu
- Philipp Schmitt
- Philine Meister
- Lukas Gensler
- Momen Khalil
- Emmanuele Poggi
- Johannes Hechtl
- Carsten Braunroth
- Kai Wurm
- Gokul Narayanan
- Eugen Solowjow
- Georg von Wichert
- Andre Scholz
- Felix Albrecht
- Maxmillian Metzner
topics:
- vision-language-action
- robot-foundation-model
- industrial-robotics
- robot-data-scaling
- factory-deployment
- manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons

## Summary
This paper is a factory-floor case study of fine-tuning a pretrained Pi0.5 VLA policy for one Siemens packaging task. Its main value is the measured deployment workflow and failure analysis, not a new model architecture.

## Problem
- The robot must pick a transparent accessory bag from a cluttered pile, place it into a cardboard package cavity, and keep the bag contents below the box closing plane.
- The task matters because production use needs reliable handling under occlusion, tight timing, safe motion, and strict downstream quality checks.
- Lab VLA demos often hide practical issues such as teleoperation latency, poor camera views, transparent objects, and recovery after bad grasps.

## Approach
- The team adapted a pretrained Pi0.5 policy with task-specific fine-tuning through repeated data collection, manual review, training, evaluation, and targeted recovery data.
- They collected 2,535 factory episodes, about 10 hours, using UR7e arms with Robotiq 2F-85 grippers, wrist cameras, a base camera, Meta Quest 3 teleoperation, and an RTX 5090 industrial PC.
- They simplified the task at first with three constraints: settled bag contents, no need to reposition bags, and fewer bags in the bin. They removed these constraints across later rounds.
- Training used LoRA fine-tuning for the first two rounds with batch size 32 for 30k steps, then full fine-tuning after the third round with batch size 128 for 60k steps, about 4 epochs.
- The execution plan used gravity to settle bag contents during transport, then used the second arm to push protruding contents into the package cavity.

## Results
- The dataset contains 2,535 episodes: 693 constrained episodes, 199 episodes without the no-reposition constraint, 1,401 unconstrained episodes, 242 recovery episodes, and about 900 earlier mock-cell episodes used to refine the execution plan.
- Manual review removed less than 5% of collected trajectories before fine-tuning.
- The paper required at least 70% evaluation success before moving to the next data-collection round, but it does not report the final overall success rate after the last training round.
- Final evaluation used trials that simulated emptying bins of 30 randomly placed bags, with a 1-minute limit per pick-and-place episode.
- In unconstrained Trials 2 and 3, the most common error was bag contents remaining on top of the product: 65% of failed episodes overall, with 62% in Trial 2 and 69% in Trial 3.
- Other reported failure rates among failed episodes were multiple bags grasped at 23%, bag not fully inserted into the box at 15%, and poor or failed grasps at 15%.

## Link
- [https://arxiv.org/abs/2605.27461v1](https://arxiv.org/abs/2605.27461v1)
