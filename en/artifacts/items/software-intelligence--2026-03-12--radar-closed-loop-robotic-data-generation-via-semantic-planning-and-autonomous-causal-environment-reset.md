---
source: arxiv
url: http://arxiv.org/abs/2603.11811v1
published_at: '2026-03-12T11:18:52'
authors:
- Yongzhong Wang
- Keyu Zhu
- Yong Zhong
- Liqiong Wang
- Jinyu Yang
- Feng Zheng
topics:
- robot-data-generation
- vision-language-models
- imitation-learning
- environment-reset
- long-horizon-planning
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset

## Summary
RADAR is a fully autonomous closed-loop system for robotic data acquisition, designed to continuously generate high-quality physical interaction data with כמעט no human involvement. It decomposes the process into four coordinated modules: “what to do, how to execute, whether it succeeded, and how to restore the environment.”

## Problem
- Robot learning requires large amounts of real-world interaction data, but collecting it through human teleoperation is costly, slow, and hard to scale.
- Existing automation methods often cannot reliably convert high-level semantic tasks into executable physical actions, and they frequently depend on fragile 2D guesses or image generation that can produce geometric hallucinations.
- More importantly, many systems cannot automatically determine whether a task succeeded or reset the environment on their own, so they still require human intervention and cannot form a continuous closed-loop collection process.

## Approach
- Use only **2-5** 3D human demonstrations to build an "affordance library," treating it as a geometric prior instead of having the VLM directly hallucinate 3D actions from scratch.
- First, the **VLM** handles semantic-level work: identifying target objects in the scene, generating tasks, decomposing long-horizon tasks, and retrieving skill examples from the demonstration library that best match semantically and geometrically.
- Then a **GNN-based in-context imitation learning / graph diffusion policy** converts "current observation + retrieved examples" into continuous robot action trajectories, effectively using few-shot demonstrations to drive execution.
- After execution, a **three-stage VQA success evaluation** (task-to-question conversion, VLM visual judgment, LLM boolean parsing) automatically filters out failed trajectories, avoiding the instability of one-step VLM judgments.
- To remove manual reset, the system synchronously generates a reverse reset plan while planning the forward task, and an **FSM** executes environment reset in strict **LIFO** causal order; if reset fails, it uses an asymmetric data retention and replanning mechanism to continue collection.

## Results
- In simulation, RADAR achieves **up to 90% success rate** on complex long-horizon tasks.
- The paper claims that on some difficult tasks, traditional baseline methods **drop to near 0**, while RADAR still maintains a high success rate, but the excerpt does not provide more detailed baseline names, dataset names, or per-task value tables.
- With only **2-5** human atomic demonstrations, the system can scale into a continuous data generation pipeline, significantly reducing human involvement.
- In real-robot deployment, RADAR can execute a variety of contact-rich skills through **one-shot or few-shot** adaptation, including **deformable object manipulation** (such as towel folding) and **high-precision alignment** (such as paper roll insertion), and **without domain-specific fine-tuning**.
- The excerpt does not provide quantitative metrics for the real-world experiments, so the strongest concrete conclusion is that the system demonstrates continuous data collection capability in both simulation and reality without human closed-loop intervention.

## Link
- [http://arxiv.org/abs/2603.11811v1](http://arxiv.org/abs/2603.11811v1)
