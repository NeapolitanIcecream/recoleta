---
source: arxiv
url: http://arxiv.org/abs/2603.01436v1
published_at: '2026-03-02T04:32:20'
authors:
- Runfa Blark Li
- David Kim
- Xinshuang Liu
- Keito Suzuki
- Dwait Bhatt
- Nikola Raicevic
- Xin Lin
- Ki Myung Brian Lee
- Nikolay Atanasov
- Truong Nguyen
topics:
- robotics
- graph-transformer
- dexterous-manipulation
- bimanual-control
- tool-use
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# PhysGraph: Physically-Grounded Graph-Transformer Policies for Bimanual Dexterous Hand-Tool-Object Manipulation

## Summary
PhysGraph proposes a physically grounded graph Transformer policy for bimanual dexterous hand-tool-object manipulation, representing the system with a graph structure rather than a flat vector. The core idea is to treat each link as a token and directly inject kinematic, contact, geometric, and anatomical priors into the attention mechanism.

## Problem
- It addresses the problem of **tool-use control in high-DoF bimanual dexterous manipulation**, especially tasks involving complex contacts among hands, tools, and objects.
- Existing methods often compress the entire system into a single state vector, ignoring hand kinematic topology, local contact relationships, and cross-hand coordination structure, which leads to low learning efficiency and brittle behavior.
- This matters because fine tool manipulation (such as cutting, shearing, etc.) requires stable grasping, contact reasoning, and bimanual coordination, making it a key challenge on the path toward more general robotic manipulation capabilities.

## Approach
- Models the two hands, tool, and object as a **physical graph**: nodes are links/rigid bodies, and edges are joint connections or dynamic contacts.
- Uses **per-link tokenization**: each link is encoded as an individual token rather than concatenating the global state into one large vector, thereby preserving fine-grained local information.
- Adds a **physically driven composite bias** into Transformer attention, allowing the model to explicitly focus on reasonable physical relationships instead of relying entirely on sparse rewards to discover them on its own.
- The composite bias includes four types of priors: **kinematic graph distance**, **edge type/contact state**, **geometric spatial proximity**, and **anatomical priors** (such as serial relationships within the same finger and same-level coordination across different fingers).
- The policy still follows a reference-trajectory-conditioned reinforcement learning paradigm, but uses a topology-aware graph Transformer to parameterize the policy and value function.

## Results
- The paper claims that PhysGraph significantly outperforms the SOTA baseline **ManipTrans** in both **manipulation precision** and **task success rate**, but the provided excerpt **does not include specific numeric tables, dataset names, or percentage improvement margins**.
- In terms of parameter efficiency, PhysGraph uses only **51% of the parameters** of ManipTrans while achieving better performance.
- For generalization, the authors claim that the architecture's topological flexibility enables **qualitative zero-shot transfer** to **unseen tool/object geometries**, but no quantitative metrics are given in the excerpt.
- In terms of compatibility, the method is described as trainable on **3 robotic hands**: **Shadow, Allegro, Inspire**.
- The paper also claims to be the first graph Transformer policy for **high-DoF bimanual dexterous tool-use tasks**, but this is a positioning claim about the method rather than an independently verifiable quantitative result.

## Link
- [http://arxiv.org/abs/2603.01436v1](http://arxiv.org/abs/2603.01436v1)
