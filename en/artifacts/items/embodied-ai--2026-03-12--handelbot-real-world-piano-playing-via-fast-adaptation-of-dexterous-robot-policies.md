---
source: arxiv
url: http://arxiv.org/abs/2603.12243v1
published_at: '2026-03-12T17:56:29'
authors:
- Amber Xie
- Haozhi Qi
- Dorsa Sadigh
topics:
- dexterous-manipulation
- sim2real
- residual-reinforcement-learning
- robot-piano-playing
- bimanual-control
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# HandelBot: Real-World Piano Playing via Fast Adaptation of Dexterous Robot Policies

## Summary
HandelBot aims to enable general-purpose bimanual robots to perform real-world piano playing, addressing the sim2real challenge in high-precision dexterous manipulation through “simulation pretraining + rapid real-world adaptation.” It decomposes the millimeter-level alignment problem into first performing structured trajectory correction, then using a small amount of real interaction for residual reinforcement learning fine-tuning.

## Problem
- Real-world bimanual piano playing requires **millimeter-level spatial precision, precise timing, and multi-finger coordination**, and policies transferred directly from simulation can easily fail due to small errors.
- Data collection for high-DoF dexterous hands is difficult to scale: teleoperation is challenging, and there is also a significant **morphology gap** between human data and robots.
- Therefore, a method is needed that **depends little on large-scale real-world demonstrations** yet can quickly bridge the sim-to-real gap, which is important for high-precision dexterous manipulation.

## Approach
- First, a base policy is trained in simulation with RL to learn **coarse-grained finger coordination** for bimanual piano playing; then an open-loop trajectory is extracted from that policy for real-world deployment.
- In the first stage, **structured policy refinement** is performed: based on real piano MIDI feedback, the system compares the “target key” with the “actually pressed key,” iteratively adjusts each finger’s **lateral joint**, and uses block-wise updates and a lookahead window to make corrections smoother.
- In the second stage, **residual reinforcement learning** is used: the refined base trajectory is frozen, and only small corrective terms are learned, changing the next target joint position to “base action + residual action,” making the process safer and more sample-efficient.
- Real-world rewards come directly from the piano’s **MIDI key output**; the algorithm uses TD3 and adds **guided noise** inspired by the direction of the target key to help explore correct lateral movements.
- The system is deployed on two Tesollo DG-5F dexterous hands + two Franka robot arms, and for each hand, residuals are learned only for 3 active fingers to reduce action dimensionality and adaptation difficulty.

## Results
- The paper claims this is the **first learning-based real-world bimanual piano playing system**, and reports hardware evaluation on **5 well-known musical pieces**: Twinkle Twinkle, Ode to Joy, Hot Cross Buns, Fur Elise, Prelude in C.
- Compared with direct sim-to-real deployment, HandelBot improves overall performance by **1.8×**, while requiring only **30 minutes** of real interaction data for rapid adaptation (explicitly stated in the abstract and contributions).
- The evaluation metric is **F1 score** (Figure 3 and the tables report F1×100); the authors state that HandelBot is the **best method on all 5 pieces**, outperforming baselines including pure simulation, simulation + residual RL, and real-world RL from scratch.
- Specific reported numbers include: on **Twinkle Twinkle**, HandelBot reaches **81 ± 4.1** F1×100; among its ablations, γ=0.75 yields **73 ± 2.5**, γ=0.9 yields **69 ± 0.2**, guided noise probability=0 yields **81 ± 0.7**, and probability=1 yields **77 ± 0.9**.
- For simulation policy deployment modes, Table 1 shows that closed-loop \(\pi_{sim}\)(CL) is generally worse; for example, **Ode to Joy: 5 ± 2.46 vs 12 ± 2.6** (Hybrid), **Prelude in C: 29 ± 2.2 vs 40 ± 1.0**, indicating that directly executing closed-loop with real observations is strongly affected by dynamics mismatch.
- The excerpt does not provide the full numeric table from Figure 3 for all methods across all 5 pieces, but the strongest concrete claim is: **HandelBot achieves the highest F1 on every song and consistently outperforms methods that do not use real-world data**.

## Link
- [http://arxiv.org/abs/2603.12243v1](http://arxiv.org/abs/2603.12243v1)
