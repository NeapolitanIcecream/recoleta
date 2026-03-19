---
source: arxiv
url: http://arxiv.org/abs/2603.12185v1
published_at: '2026-03-12T17:14:45'
authors:
- Chetan Borse
- Zhixian Xie
- Wei-Cheng Huang
- Wanxin Jin
topics:
- physics-simulation
- contact-rich-robotics
- gpu-parallelism
- analytical-contact-model
- dexterous-manipulation
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# ComFree-Sim: A GPU-Parallelized Analytical Contact Physics Engine for Scalable Contact-Rich Robotics Simulation and Control

## Summary
ComFree-Sim is a GPU-parallel physics engine for contact-rich robotics tasks that replaces traditional iterative optimization with an analytical, complementarity-free contact solver. Its core value is decomposing contact into small problems that can be solved in parallel, significantly improving throughput while maintaining physical fidelity close to MuJoCo Warp and supporting real-time control.

## Problem
- Existing contact-rich robotics simulation is often slowed down by **contact solving**: mainstream methods rely on complementarity constraints or constrained optimization, requiring iterative solves at every step, and the cost typically grows superlinearly as the number of contacts increases.
- This limits real-time deployment for large-scale parallel data generation, differentiable simulation, online MPC/MPPI, and high-frequency, dense-contact control tasks such as dexterous hands.
- A contact backend is needed that is both **lighter-weight and linearly scalable** without significantly sacrificing physical realism and stability, and ideally can serve as a plug-and-play replacement in existing MuJoCo/Warp workflows.

## Approach
- The core mechanism is **complementarity-free** contact modeling: it first predicts the next-step velocity under “no contact force,” then directly computes the contact impulse using an **impedance-style prediction-correction** formula based on the degree of violation of non-penetration/friction constraints, eliminating per-step iterative optimization.
- It performs analytical closed-form updates in the **dual cone of Coulomb friction**, and approximates the friction cone as a polyhedron, so each contact pair and each cone facet can be computed independently, making it naturally suited to GPU kernel parallelism.
- The paper extends the method into a **unified 6D contact model** that simultaneously captures tangential friction, torsional friction, and rolling friction, rather than only simple point-contact sliding friction.
- To avoid the high cost of exactly computing the impedance matrix, the authors propose a **practical dual-cone impedance heuristic**: it uses a small number of global user parameters \(k_{user}, d_{user}\) and gap-dependent scaling to control contact “softness/stiffness,” while preserving a MuJoCo-compatible interface.
- The system is implemented in Warp and exposed through a **MuJoCo-compatible interface** as a drop-in backend alternative to MJWarp, making it easy to integrate into existing robotics simulation and control stacks.

## Results
- In dense collision drop tests, MJWarp has an average penetration depth of **1.7 ± 4.9 mm**; after tuning, ComFree-Sim can achieve **comparable or lower** penetration, for example:
  - at **0.3, 0.001**: **1.6 ± 3.3 mm**;
  - at **0.3, 0.005**: **1.4 ± 2.5 mm**;
  - at **0.5, 0.001**: **1.0 ± 2.1 mm**;
  - at **0.5, 0.005**: **0.9 ± 1.5 mm**.
- The abstract states that in dense contact scenes, compared with MJWarp, ComFree-Sim achieves **near-linear runtime scaling** and delivers **2–3× higher throughput**, because contact solving can be decomposed and parallelized across contact pairs and cone facets.
- In terms of stability, the paper says ComFree-Sim exhibits **monotonic horizontal velocity decay** over a fairly wide parameter range, with no obvious spurious drift or energy growth; it remains stable even at a relatively large step size of **dt = 0.02 s**, though it generally depends more on smaller step sizes than MJWarp. Unless otherwise noted, benchmarks use **dt = 0.002 s** by default.
- For friction behavior, the authors show through controlled experiments that the dissipation trends of **torsional friction** and **rolling friction** vary monotonically with their corresponding friction coefficients, but the excerpt **does not provide specific numerical metrics**.
- For real-robot applications, the abstract states that the engine has been deployed in real-time MPC and dynamics-aware motion retargeting on a **LEAP multi-fingered dexterous hand**, and shows that **lower-latency rollouts can improve closed-loop success rate** and support more practical high-frequency contact control; however, the excerpt **does not provide success-rate percentages or specific comparison figures**.

## Link
- [http://arxiv.org/abs/2603.12185v1](http://arxiv.org/abs/2603.12185v1)
