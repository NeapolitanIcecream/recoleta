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
- robotics
- contact-dynamics
- gpu-parallelism
- model-predictive-control
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# ComFree-Sim: A GPU-Parallelized Analytical Contact Physics Engine for Scalable Contact-Rich Robotics Simulation and Control

## Summary
ComFree-Sim is a GPU-parallel analytical contact physics engine for contact-rich robotics tasks, designed to replace traditional contact resolution methods that require iterative solves. By using complementarity-free closed-form impulse computation, it turns contact solving into a naturally GPU-friendly parallel task, thereby improving the efficiency of large-scale simulation and real-time control.

## Problem
- Traditional robotics physics engines typically solve complementarity constraints or optimization problems during contact resolution, and the per-step computational cost grows **superlinearly** with the number of contacts.
- This slows down parallel simulation, differentiable simulation, MPC, and online planning in contact-rich scenarios, and is especially unfavorable for high-frequency closed-loop control.
- A lightweight GPU-suitable contact backend is needed that preserves physically credible contact behavior while scaling nearly linearly with the number of contacts.

## Approach
- The core method is **complementarity-free** contact modeling: it first predicts the next-step object velocity assuming no contact, then applies an **impedance-style prediction-correction update** based on the degree of contact constraint violation, directly computing contact impulses in closed form without per-step iterative solves.
- The method operates in the **dual cone of Coulomb friction** and uses a polyhedral approximation of the friction cone, so each contact pair and each cone facet can be computed **independently and decoupled** from one another.
- The paper extends the model to a **unified 6D contact** formulation, covering tangential friction, torsional friction, and rolling friction, rather than only standard point-contact sliding friction.
- In implementation, it is built on Warp and divided into four GPU kernels: smooth velocity prediction, per-contact per-facet impulse computation, generalized impulse accumulation, and velocity correction; it also provides a **MuJoCo-compatible** interface and can serve as an alternative backend to MJWarp.
- To avoid the high cost of an exact impedance matrix, the authors propose a practical **dual-cone impedance heuristic** that uses a small number of global parameters to control contact “stiffness/softness,” while retaining the possibility of learned parameterization.

## Results
- In dense collision drop tests, MJWarp has an average penetration depth of **1.7 ± 4.9 mm**; under different parameter settings, ComFree-Sim ranges from **3.9 ± 6.9 mm** down to **0.9 ± 1.5 mm**, and under the best setting it is **lower than MJWarp**.
- The paper claims that in dense contact scenarios, ComFree-Sim achieves **near-linear runtime scaling** relative to MJWarp and delivers **2–3× higher throughput**, while maintaining **comparable physical fidelity**.
- In torsional and rolling friction tests, the authors report a **monotonic decay trend** in angular velocity / center-of-mass velocity as friction coefficients vary, indicating that the 6D friction model consistently captures dissipative behavior; however, the excerpt **does not provide specific quantitative metrics**.
- In stability tests, ComFree-Sim shows **monotonic decay of horizontal velocity** over a relatively wide parameter range, with no obvious drift or energy growth; it is also claimed to remain stable at **dt = 0.02 s**, though it generally requires smaller time steps than MJWarp. Most default benchmarks use **dt = 0.002 s**.
- The system was also deployed to real-time MPPI/MPC and motion retargeting tasks on a real **LEAP multi-fingered dexterous hand**. The authors claim that lower-latency simulation yields **higher closed-loop success rates** and more practical high-frequency control, but the excerpt **does not provide specific success-rate numbers**.

## Link
- [http://arxiv.org/abs/2603.12185v1](http://arxiv.org/abs/2603.12185v1)
