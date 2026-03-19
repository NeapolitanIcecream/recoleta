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
- bimanual-manipulation
- dexterous-manipulation
- graph-transformer
- contact-aware-policy
- tool-use
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# PhysGraph: Physically-Grounded Graph-Transformer Policies for Bimanual Dexterous Hand-Tool-Object Manipulation

## Summary
PhysGraph proposes a physically grounded graph Transformer policy for bimanual dexterous hand-tool-object manipulation, representing the entire system as a “link graph” rather than a flat vector. Its core value is enabling the policy to explicitly use kinematic structure, contact, and geometric relations, making it more stable and precise in high-dimensional, contact-rich tasks.

## Problem
- The problem addressed is policy learning for **bimanual dexterous tool use**: the state and action spaces are high-dimensional, contact dynamics are complex, and both hands must coordinate to control the tool and target object.
- Existing methods often compress the full hand-tool-object state into a single vector, ignoring hand joint topology, per-link local states, and dynamic contact structure, forcing the model to “guess” physical relationships from sparse rewards.
- This matters because without explicitly modeling these structures, policies can be fragile, physically inconsistent, and difficult to scale to more complex fine manipulation tool-use tasks.

## Approach
- Represent the two hands, tool, and object as a **physical graph**: nodes are individual rigid bodies/links, and edges are joint connections or dynamic contact relationships.
- Use **per-link tokenization**: each link becomes its own token rather than being aggregated into a global state first, allowing the model to preserve local finger contact and kinematic-chain information.
- Add **physical prior biases** into Transformer attention instead of learning attention purely from data; the biases include four types: kinematic graph distance, edge type/contact state, geometric proximity, and anatomical priors (serial chains and finger coordination).
- These biases are injected directly into multi-head attention in the form of **head-specific composite bias**, so different heads can focus on different physical relationships, such as fingers in contact, adjacent joints, or coordinated fingers.
- The training paradigm remains reinforcement learning / tracking control conditioned on reference trajectories, but the main innovation is parameterizing the policy network with graph structure and physical biases.

## Results
- The paper claims that on “challenging bimanual tool-use tasks,” PhysGraph significantly outperforms the SOTA baseline **ManipTrans** in both **task success rate** and **manipulation precision / motion fidelity**.
- In terms of parameter efficiency, PhysGraph uses only **51% of the parameters of ManipTrans** while still achieving better performance; this is the clearest quantitative conclusion in the excerpt.
- For generalization, the authors report **qualitative zero-shot transfer** to **unseen tool/object geometries**, but the excerpt **does not provide specific numerical metrics**.
- In terms of compatibility, the method is described as trainable on **three robotic dexterous hands**: **Shadow, Allegro, Inspire**, reflecting a degree of cross-morphology generality.
- The excerpt **does not provide more detailed quantitative tables**, so it is not possible to list specific datasets, absolute success rates, improvement margins, or statistical significance values; the strongest concrete numerical claim is that the **parameter count is reduced to 51%** while overall performance remains better than ManipTrans.

## Link
- [http://arxiv.org/abs/2603.01436v1](http://arxiv.org/abs/2603.01436v1)
