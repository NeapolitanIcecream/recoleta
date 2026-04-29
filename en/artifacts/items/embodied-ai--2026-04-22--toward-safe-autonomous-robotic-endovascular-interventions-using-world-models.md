---
source: arxiv
url: http://arxiv.org/abs/2604.20151v1
published_at: '2026-04-22T03:32:18'
authors:
- Harry Robertshaw
- Nikola Fischer
- Han-Ru Wu
- Andrea Walker Perez
- Weiyuan Deng
- Benjamin Jackson
- Christos Bergeles
- Alejandro Granados
- Thomas C Booth
topics:
- world-models
- endovascular-robotics
- safe-robot-learning
- sim2real
- model-based-rl
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Toward Safe Autonomous Robotic Endovascular Interventions using World Models

## Summary
This paper studies autonomous robot navigation for mechanical thrombectomy and tests whether a world-model RL agent can handle longer, harder vascular navigation tasks across unseen anatomies. The main claim is that TD-MPC2 improves generalization and navigation quality over SAC in simulation, while keeping guidewire forces far below a stated rupture threshold and showing comparable in vitro success.

## Problem
- The task is autonomous endovascular navigation for mechanical thrombectomy, where a robot must steer catheter-wire devices through patient-specific blood vessels in real time.
- Existing RL methods have trouble with long-horizon control, anatomy variation, and transfer beyond the vessels seen in training.
- Safety matters because excess tip force can damage vessels; the paper cites a proposed vessel rupture threshold of 1.5 N.

## Approach
- The authors train a multi-task world-model agent based on **TD-MPC2** and compare it with a state-of-the-art **SAC** baseline for five thrombectomy-relevant navigation tasks.
- The agent observes only tracked 2D device-tip state, previous state, target location, and previous action, which matches fluoroscopy-style guidance rather than full vessel geometry.
- Training uses 10 patient-specific vascular anatomies in simulation, with evaluation on 5 held-out anatomies plus fluoroscopy-guided in vitro tests on a patient-specific 3D-printed phantom.
- TD-MPC2 learns a latent dynamics model of how the catheter and wire move, then plans short action sequences inside that learned model instead of reacting step by step only from trial-and-error.
- The study also measures safety with mean and max guidewire tip contact force in simulation and applies sim-to-real augmentation by random scaling, rotation, and randomized insertion points during training.

## Results
- **Held-out simulation:** TD-MPC2 reached **58% mean success rate** vs **36% for SAC** across tasks (**p < 0.001**), and **49% mean path ratio** vs **22%** (**p < 0.001**), but took longer: **17.1 s** vs **9.6 s** (**p < 0.001**).
- **Safety in simulation:** TD-MPC2 had **0.15 N mean tip force** and **0.55 N max tip force**, compared with **0.13 N** and **0.50 N** for SAC. These forces stayed well below the paper's **1.5 N** rupture threshold.
- **Task-level simulation gains:** TD-MPC2 improved success on hard tasks such as **A2L: 38% vs 8%**, **A2R: 52% vs 8%**, and **A3L: 38% vs 16%**; corresponding path-ratio gains were **40% vs 21%**, **48% vs 24%**, and **63% vs 21%**.
- **In vitro phantom tests:** TD-MPC2 achieved **68% mean success** vs **60% for SAC** with **no significant difference** (**p = 0.567**), but had better mean **path ratio 54% vs 44%** (**p < 0.05**) and slower procedures: **111.0 s** vs **66.2 s** (**p < 0.001**).
- **In vitro task detail:** On **A2L**, both methods had **0% success**, but TD-MPC2 improved path ratio to **71% vs 47%** (**p = 0.017**). On **A2R**, TD-MPC2 had **60% success** vs **40%** for SAC; on **A3R**, **80% vs 60%**, though these were not significant in the reported small-sample setting.
- **Training efficiency:** Reported exploration steps for the shown results were **0.5e6** for TD-MPC2 after **25 hours** and **4.5e6** for SAC after **75 hours**, suggesting faster learning for the world-model setup at the reported operating point.

## Link
- [http://arxiv.org/abs/2604.20151v1](http://arxiv.org/abs/2604.20151v1)
