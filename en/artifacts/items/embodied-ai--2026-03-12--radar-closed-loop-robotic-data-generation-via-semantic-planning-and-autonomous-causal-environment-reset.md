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
- autonomous-data-collection
- vision-language-models
- in-context-imitation-learning
- robot-manipulation
- environment-reset
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset

## Summary
RADAR proposes a fully autonomous closed-loop system for robotic manipulation data collection, aiming to continuously generate high-quality real-world interaction data with almost no human involvement. It decomposes the process into four modules: “what to do, how to do it, whether it succeeded, and how to reset,” scaling from a small number of human demonstrations to continuous autonomous collection.

## Problem
- Robot foundation models require large-scale, high-quality physical interaction data, but human teleoperation-based collection is expensive, slow, and difficult to scale.
- Existing automation approaches often break down between semantic planning and physical execution: VLMs are prone to 2D/pixel-level hallucinations, while low-level policies lack the ability to autonomously generate tasks and verify outcomes.
- More importantly, most systems cannot autonomously reset the environment, preventing the collection pipeline from becoming truly closed-loop and ultimately still requiring human intervention.

## Approach
- Use only **2-5** 3D human demonstrations to build an affordance library as geometric and action priors, instead of having the VLM directly “guess” 3D coordinates.
- The VLM first performs **semantic target identification + hierarchical task planning**: it identifies objects that actually exist in the scene, generates atomic tasks or long-horizon task chains, and retrieves the best-matching skill examples from the demonstration library.
- Low-level execution uses **GNN-based in-context imitation learning / graph diffusion policy**, taking current observations and retrieved demonstrations as context to generate continuous robot action trajectories.
- After execution, the system uses a **three-stage VQA success evaluation**: it converts the command into visual questions, has the VLM judge them, and then uses a parser to convert the output into strict boolean values, reducing linguistic redundancy and misjudgment.
- To achieve a truly closed loop, the system simultaneously generates a **reverse reset plan** while planning the forward task, and an FSM executes the reset according to a strict **LIFO causal order**; if reset fails, it uses asymmetric data retention and replanning so the process can continue running.

## Results
- In simulation, RADAR achieves **up to 90% success rates on complex long-horizon tasks**.
- The paper claims that on some challenging tasks, traditional baselines **drop to near 0% performance**, while RADAR still solves them reliably; however, the excerpt does not provide more detailed dataset information, baseline names, or full table values.
- The system requires only **2-5 manually provided atomic demonstrations** to bootstrap the automatic data generation pipeline, significantly reducing the burden of manual data collection.
- In real robot deployments, the system can adapt via **one-shot or few-shot** execution of a variety of contact-rich skills, including **deformable object manipulation** (such as towel folding) and **high-precision alignment/insertion** (such as inserting a paper roll), and does so **without domain-specific fine-tuning**.
- The excerpt does not provide quantitative success rates for real-world experiments, so the strongest current evidence is mainly the qualitative and partially quantitative claim that it works across both simulation and real environments, while supporting autonomous reset and continuous data collection.

## Link
- [http://arxiv.org/abs/2603.11811v1](http://arxiv.org/abs/2603.11811v1)
