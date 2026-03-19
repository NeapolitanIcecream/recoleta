---
source: arxiv
url: http://arxiv.org/abs/2603.12243v1
published_at: '2026-03-12T17:56:29'
authors:
- Amber Xie
- Haozhi Qi
- Dorsa Sadigh
topics:
- dexterous-robotics
- sim-to-real
- residual-reinforcement-learning
- robot-piano-playing
- bimanual-manipulation
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# HandelBot: Real-World Piano Playing via Fast Adaptation of Dexterous Robot Policies

## Summary
HandelBot proposes a two-stage method for rapidly adapting dexterous-hand piano policies learned in simulation to the real world, enabling bimanual robot piano playing with very little real interaction data. To address the sim-to-real gap in millimeter-precision tasks, it combines structured trajectory correction with residual reinforcement learning and significantly outperforms direct deployment of the simulation policy.

## Problem
- Real-world bimanual robot piano playing requires **millimeter-level spatial precision, precise timing, and long-horizon bimanual coordination**, and even small simulation-to-reality errors can cause wrong or missed key presses.
- Relying on teleoperation or human demonstrations to collect high-quality dexterous-hand data is **expensive, hard to scale, and even infeasible for fast independent finger motions**.
- Pure simulation RL can learn coarse-grained coordination, but **performs poorly when transferred directly to a real piano**, especially under contact dynamics and controller mismatch.

## Approach
- First, train a base piano policy with RL in simulation to obtain a **rough open-loop trajectory** and structural prior that work in the simulator.
- Stage one performs **policy refinement**: execute the trajectory on a real piano, compare the target keys with the actually pressed keys, and adjust only the fingers' lateral joints according to rules so the fingers gradually align with the correct keys; updates are done in time chunks, with lookahead and step-size annealing to maintain smoothness.
- Stage two performs **residual reinforcement learning**: freeze the refined base trajectory and learn only small corrective actions, which are added to the next-step target joint positions, enabling safer and more efficient adaptation to real dynamics.
- The real-world reward comes directly from **MIDI key outputs**; training uses TD3, and can incorporate guided noise aligned with the “correct lateral movement direction” to help exploration.
- The system runs on a bimanual hardware platform: two Tesollo DG-5F hands, two Franka robot arms, a MIDI keyboard, plus IK and collision constraints to ensure safe deployment.

## Results
- The paper claims, to the best of its knowledge, that this is the **first learning-based real-world bimanual robot piano-playing system**, evaluated on **5 well-known songs**: Twinkle Twinkle, Ode to Joy, Hot Cross Buns, Fur Elise, and Prelude in C.
- Compared with direct sim-to-real deployment, HandelBot achieves an overall **1.8× improvement** and requires only **30 minutes of real interaction data** to complete rapid adaptation (explicitly stated in the abstract and introduction).
- In terms of training budget, the RL method trains on **100 trajectories**; longer pieces require about **30k environment interactions / 1 hour**, while shorter pieces require about **16k interactions / 30 minutes**.
- The simulation policy performs very weakly under direct closed-loop deployment, for example F1×100: **Ode to Joy 5±2.46**, **Twinkle Twinkle 23±6.2**, **Hot Cross Buns 8±2.1**, **Prelude in C 29±2.2**, **Fur Elise 18±3.2**; parallel simulation hybrid execution is slightly better but still low, at **12±2.6, 24±2.5, 9±2.9, 40±1.0, 20±4.9**.
- In the ablation study, HandelBot reaches **81±4.1** F1×100 on Twinkle Twinkle; changing the discount factor reduces it to **73±2.5** (γ=0.75) and **69±0.2** (γ=0.9); removing guided noise still yields **81±0.7**, while always enabling guided noise gives **77±0.9**.
- Although the main text states that “HandelBot achieves the highest F1 on all songs,” the provided excerpt **does not include all specific values from the full main results table**; the strongest verifiable quantitative claims are the **1.8× improvement, 30 minutes of real data, evaluation on 5 songs, and the F1 scores listed above**.

## Link
- [http://arxiv.org/abs/2603.12243v1](http://arxiv.org/abs/2603.12243v1)
