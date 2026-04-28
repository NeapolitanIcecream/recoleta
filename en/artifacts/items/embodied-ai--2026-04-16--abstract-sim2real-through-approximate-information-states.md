---
source: arxiv
url: http://arxiv.org/abs/2604.15289v1
published_at: '2026-04-16T17:53:16'
authors:
- Yunfu Deng
- Yuhao Li
- Josiah P. Hanna
topics:
- sim2real
- state-abstraction
- reinforcement-learning
- robotics
- history-based-modeling
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Abstract Sim2Real through Approximate Information States

## Summary
This paper studies sim2real transfer when the simulator uses a coarser state than the real robot, so key dynamics are missing. It formalizes that setting as a state-abstraction problem and proposes ASTRA, a history-based simulator grounding method trained with a small amount of real-world data.

## Problem
- The paper targets **abstract sim2real**: training an RL policy in a simplified simulator whose state omits real-world details, then transferring that policy to the real robot.
- This matters because high-fidelity robot simulators are expensive or impractical in large, complex domains, while abstract simulators are faster and easier to build.
- The main technical issue is that abstraction creates **partial observability**. Two different real states can map to the same abstract state, so standard sim2real methods that assume matched state spaces or only parameter mismatch can fail.

## Approach
- The paper formalizes abstract sim2real using **state abstraction** in RL. The key claim is that grounding an abstract simulator requires using **state-action history**, because the abstract state alone is often not Markov.
- It introduces **ASTRA** (Augmented Simulation with self-predicTive abstRAction), which learns a recurrent latent state from abstracted real-world histories.
- ASTRA trains this latent state with three losses on paired simulator/real data: a **latent transition loss** to predict the next latent state, a **reward prediction loss** to keep task-relevant information, and an **abstract next-state correction loss** to adjust the simulator’s next-state prediction toward the real abstracted next state.
- The grounded simulator then rolls forward using the corrected abstract state and the learned latent dynamics, and an RL policy is trained on that grounded simulator. For deployment, a target-side encoder maps real-world histories into the same latent space.

## Results
- The paper claims ASTRA enables successful transfer in both **sim2sim** and **sim2real** settings where direct transfer and several baselines fail.
- In **AntMaze sim2sim navigation**, ASTRA achieves the **highest success rate** on both **U-Maze** and **Long Maze** among the compared methods, including Direct Transfer, Domain Randomization, COMPASS, RMA, NAS, and DT+IQL. The excerpt does not provide the exact success-rate numbers from Figure 3.
- In a **morphology-shift test** on a modified Ant with **1.25× leg length**, the ASTRA policy trained on the standard Ant reaches **65% success** on **U-Maze**, versus **21%** for direct transfer.
- For grounding data in AntMaze, ASTRA and NAS use **200 trajectories** with average length **500 steps** collected by a random behavior policy.
- The abstract-to-target gap in that setup is large: the target AntMaze state has **29 dimensions**, while the abstract simulator uses only **location and velocity**.
- The excerpt states that ASTRA also works on **real NAO humanoid tasks** and simulated humanoid locomotion, but it does not include the final quantitative results for those experiments in the provided text.

## Link
- [http://arxiv.org/abs/2604.15289v1](http://arxiv.org/abs/2604.15289v1)
