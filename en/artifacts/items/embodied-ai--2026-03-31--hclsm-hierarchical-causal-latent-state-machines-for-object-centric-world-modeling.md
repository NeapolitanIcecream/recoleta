---
source: arxiv
url: http://arxiv.org/abs/2603.29090v1
published_at: '2026-03-31T00:11:29'
authors:
- Jaber Jaber
- Osama Jaber
topics:
- object-centric-world-model
- robotics
- causal-representation-learning
- state-space-models
- slot-attention
- hierarchical-dynamics
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# HCLSM: Hierarchical Causal Latent State Machines for Object-Centric World Modeling

## Summary
HCLSM is an object-centric video world model for robot scenes that combines slots, multi-timescale dynamics, and learned interaction graphs. The paper’s main claim is that a staged training schedule is needed to get object-like slots before future prediction pushes the model into flat distributed codes.

## Problem
- Standard video world models predict future latents with one flat state, so they mix objects together, miss different time scales, and do not expose causal interactions.
- For robot planning and counterfactual reasoning, the model should track separate objects, handle continuous motion and discrete events, and capture which objects affect others.
- Existing systems in the paper’s comparison table cover only parts of this: SlotFormer has objects without hierarchy or causality, DreamerV3 has latent dynamics without object decomposition, and V-JEPA-style models use unstructured latents.

## Approach
- HCLSM first encodes video frames with a ViT, then uses slot attention to split the scene into object slots. A spatial broadcast decoder reconstructs frozen ViT features per slot so slots compete for spatial ownership.
- Its dynamics stack has three levels: a per-object selective state space model for frame-to-frame physics, a sparse transformer that runs only on detected event frames, and a compressed transformer that summarizes higher-level goals.
- A GNN passes messages between slots using learned edge weights, and the model adds a NOTEARS-style DAG regularizer for causal structure learning, though the paper says the explicit causal graph did not work well in practice.
- Training has two stages. Stage 1 uses only reconstruction and a diversity term for the first 40% of steps so slots specialize. Stage 2 turns on JEPA-style future prediction after the slots already carry spatial structure.
- The implementation adds a custom Triton kernel for the selective SSM scan, GPU Sinkhorn tracking, and chunked GNN edge computation to keep training feasible.

## Results
- On PushT from LeRobot / Open X-Embodiment, a 68M-parameter HCLSM trained on 206 episodes and 25,650 frames reaches **0.008 next-state prediction MSE** with the two-stage method.
- The same two-stage run reports **SBD loss 0.008** and **diversity loss 0.132**, versus **diversity loss 0.154** for the no-SBD variant. The no-SBD model gets lower prediction loss at **0.002**, which the authors attribute to easier distributed coding rather than object decomposition.
- Throughput in Table 3 is **2.9 steps/s** for the two-stage model versus **2.3 steps/s** for the no-SBD variant on the reported setup.
- The custom Triton SSM kernel gives **39.3x speedup** on the tiny config (**6.22 ms -> 0.16 ms**) and **38.0x** on the base config (**69.64 ms -> 1.83 ms**) on an NVIDIA T4.
- Qualitative results show emerging slot-based spatial decomposition, but the decomposition is weak: all **32 slots** stay alive in a scene with about **3 objects**, and each object is split across many slots.
- Event detection finds about **2-3 events per 16-frame sequence**. The causal adjacency matrix fails to learn useful edges, and only **2 of 4** training runs completed due to bf16 NaN instability.

## Link
- [http://arxiv.org/abs/2603.29090v1](http://arxiv.org/abs/2603.29090v1)
