---
source: hn
url: https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/
published_at: '2026-04-17T22:45:36'
authors:
- hhs
topics:
- cross-robot-transfer
- skill-learning
- manipulation
- kinematics
- safe-control
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# How to teach the same skill to different robots

## Summary
EPFL's Kinematic Intelligence aims to transfer a human-demonstrated manipulation skill across robots with different kinematics without rewriting task code for each robot. The main claim is safe, predictable cross-robot execution of the same task sequence on multiple commercial robots.

## Problem
- A task programmed or demonstrated on one robot often does not work on another because robots differ in joint layout, reach, motion limits, and stability constraints.
- Reprogramming each robot from scratch raises deployment cost, slows upgrades, and makes robot fleets harder to maintain.
- Skill transfer matters in manufacturing and other settings where hardware changes faster than task specifications.

## Approach
- The system starts from human demonstrations of manipulation tasks such as placing, pushing, and throwing, captured with motion-tracking.
- It converts each demonstrated task into a robot-agnostic movement strategy rather than keeping a controller tied to one robot body.
- It builds a structured description of each robot's kinematic and safety limits, including joint ranges, forbidden configurations, and stability-related constraints.
- It adapts the shared movement strategy to each robot automatically so the robot can execute the skill within its own feasible motion space.
- The paper frames this as "Kinematic Intelligence" for cross-robot skill transfer and safe execution.

## Results
- In an assembly-line experiment, three different commercial robots reproduced the same demonstrated sequence: pushing a wooden block off a conveyor belt, placing it on a table, and throwing it into a basket.
- The reported outcome is safe and reliable execution across all three robots, even when the allocation of task steps between robots was changed.
- The excerpt gives no benchmark table, error rate, success percentage, or runtime numbers.
- The strongest concrete claim is one-shot transfer in the sense of "Demonstrate once, execute on many," with one human-demonstrated skill used across robots with different mechanical designs.

## Link
- [https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/](https://actu.epfl.ch/news/how-to-teach-the-same-skill-to-different-robots-2/)
