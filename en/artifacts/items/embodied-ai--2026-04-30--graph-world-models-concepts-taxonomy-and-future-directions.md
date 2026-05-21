---
source: arxiv
url: https://arxiv.org/abs/2604.27895v1
published_at: '2026-04-30T14:09:14'
authors:
- Jiawei Liu
- Senqiao Yang
- Mingjun Wang
- Yu Wang
- Bei Yu
topics:
- graph-world-models
- world-models
- embodied-ai
- robotics
- graph-representation-learning
- causal-reasoning
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Graph World Models: Concepts, Taxonomy, and Future Directions

## Summary
This survey defines graph world models as world models that store entities as nodes and relations as edges for prediction, planning, and reasoning. It organizes prior work by spatial, physical, and logical relational biases, with links to robotics, embodied AI, navigation, simulation, and LLM agents.

## Problem
- Classical world models built on flat tensors can spend capacity on pixel noise, drift during long rollouts, and miss object or causal relations needed for planning.
- Work using graphs in world models is spread across reinforcement learning, robotics, computer vision, embodied AI, and LLM agents, so the paper aims to give it a shared definition and map.
- The topic matters for agents that need longer-horizon navigation, physical prediction, manipulation, and instruction following with less real-world trial and error.

## Approach
- It defines a standard world model as a vision module V and memory module M over latent state, then defines a graph world model with a graph G_t=(V_t,E_t).
- A graph world model has structural abstraction ψ, which converts observations or latent states into a graph, and relational transition T_G, which updates nodes, edges, and attributes over time under actions.
- The taxonomy uses 3 relational inductive biases: spatial graphs for reachability, physical graphs for object or system dynamics, and logical graphs for semantic or causal reasoning.
- It groups representative methods into connector, simulator, and reasoner classes, then discusses gaps such as dynamic graph updates, probabilistic dynamics, multi-granularity relations, and GWM-specific benchmarks.

## Results
- The paper reports no new benchmark experiments or aggregate accuracy table; it is a survey and taxonomy paper.
- It claims to be the first survey to explicitly define graph world models as a unified research area centered on graph-structured relational inductive biases.
- The taxonomy has 3 main classes: graph as connector, graph as simulator, and graph as reasoner.
- The formal GWM definition adds 2 core operations to a world model: structural abstraction ψ and relational transition T_G.
- Concrete surveyed capability claims include HD-VPD processing more than 100,000 implicit particles in real time for high-fidelity dynamic simulation, and graph navigation methods such as SPTM, SoRB, POINT, L3P, Dreamwalker, and CityNavAgent reducing search over continuous observations to search over nodes and edges.

## Link
- [https://arxiv.org/abs/2604.27895v1](https://arxiv.org/abs/2604.27895v1)
