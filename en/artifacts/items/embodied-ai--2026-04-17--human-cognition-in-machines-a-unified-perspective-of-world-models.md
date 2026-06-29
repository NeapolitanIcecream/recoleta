---
source: arxiv
url: http://arxiv.org/abs/2604.16592v1
published_at: '2026-04-17T17:51:46'
authors:
- Timothy Rupprecht
- Pu Zhao
- Amir Taherin
- Arash Akbari
- Arman Akbari
- Yumei He
- Sean Duffy
- Juyi Lin
- Yixiao Chen
- Rahul Chowdhury
- Enfu Nan
- Yixin Shen
- Yifan Cao
- Haochen Zeng
- Weiwei Chen
- Geng Yuan
- Jennifer Dy
- Sarah Ostadabbas
- Silvia Zhang
- David Kaeli
- Edmund Yeh
- Yanzhi Wang
topics:
- world-models
- cognitive-architecture
- survey-paper
- embodied-ai
- sim2real
- scientific-discovery-agents
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Human Cognition in Machines: A Unified Perspective of World Models

## Summary
This paper is a survey and position paper, not a new trained world model. It argues that world models should be classified by cognitive functions from Cognitive Architecture Theory, and it proposes a unified view that covers video, embodied, and "epistemic" world models.

## Problem
- Current world model surveys mostly group methods by architecture or by a broad split between representation and generation, which the authors argue hides which cognitive functions a system actually improves.
- Many papers describe world models with human-like cognition claims, but the authors argue those claims lack a grounded comparison to Cognitive Architecture Theory, especially for motivation and meta-cognition.
- This matters because research effort can drift toward overstated capabilities while key missing functions for agent behavior, planning, and self-monitoring remain weak or absent.

## Approach
- The paper builds a taxonomy of world models around seven cognitive functions: memory, perception, language, reasoning, imagination, motivation, and meta-cognition.
- It applies this taxonomy across three domains: video world models, embodied world models, and a new proposed category called epistemic world models for scientific discovery over structured knowledge.
- It proposes a conceptual unified world model that combines multimodal perception, latent state memory, language interfaces, imagination through rollout or sim2real transfer, reasoning modules, reward-based motivation, and meta-cognitive control through global workspace style mechanisms.
- It uses examples such as JEPA, Dreamer-style agents, multimodal embodied systems, and agent frameworks to show how prior work fits into specific cognitive functions rather than a single architecture bucket.
- It identifies motivation and meta-cognition as the main research gaps, and points to active inference and global workspace theory as candidate directions.

## Results
- The paper claims it is the **first** survey to classify world models by cognitive functions from Cognitive Architecture Theory; Table 1 compares its scope against **8** prior surveys from **2025-2026** and marks its survey as covering video, embodied, simulation, physics alignment, epistemic models, and CAT-based analysis.
- It introduces **1 new category**, **epistemic world models**, defined as agent systems that operate over structured knowledge spaces for tasks such as scientific discovery.
- It defines a unified taxonomy with **7 cognitive functions**: memory, perception, language, reasoning, imagination, motivation, and meta-cognition.
- It states a concrete gap claim: current state-of-the-art world models largely lack intrinsic motivation beyond hand-crafted rewards, and the paper says **none** demonstrate genuine meta-cognitive abilities such as self-monitoring, self-evaluation, or self-control.
- The excerpt provides **no experimental benchmark results** or new task metrics for a proposed model. Its main contributions are conceptual: a taxonomy, a survey comparison, a unified design proposal, and identified research gaps.

## Link
- [http://arxiv.org/abs/2604.16592v1](http://arxiv.org/abs/2604.16592v1)
