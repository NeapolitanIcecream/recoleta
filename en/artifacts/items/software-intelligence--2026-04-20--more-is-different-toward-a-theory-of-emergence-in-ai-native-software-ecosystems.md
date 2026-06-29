---
source: arxiv
url: http://arxiv.org/abs/2604.19827v1
published_at: '2026-04-20T15:09:55'
authors:
- Daniel Russo
topics:
- multi-agent-systems
- software-engineering-theory
- complex-adaptive-systems
- causal-emergence
- ai-native-ecosystems
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# More Is Different: Toward a Theory of Emergence in AI-Native Software Ecosystems

## Summary
This paper argues that AI-native software ecosystems should be modeled as complex adaptive systems, because multi-agent failures come from interaction effects that agent-level software engineering theory does not explain. It proposes a testable way to measure when ecosystem-level structure predicts outcomes better than individual agent actions.

## Problem
- The paper targets a gap in software engineering theory: individual AI agents can perform their assigned tasks correctly while the overall codebase degrades through their interactions.
- This matters because current practice depends on a compositional assumption: if components are correct, the full system should be manageable through tests, contracts, reviews, and local verification.
- The cited evidence suggests that assumption breaks in multi-agent AI settings with shared repositories and natural-language specs, where coordination failures, architectural drift, and cascade failures appear at the ecosystem level.

## Approach
- The paper treats AI-native software ecosystems as **complex adaptive systems (CAS)** using Holland's six properties: agents with internal models, nonlinear interactions, co-evolution, emergent macro-patterns, boundary formation, and perpetual novelty.
- It maps each CAS property to software observables that teams could measure from git, CI/CD, dependency graphs, and policy changes, such as commit fan-out, boundary violations, modularity drift, and entropy trajectories.
- It defines ecosystem-level variables like structural entropy, coupling density, architectural coherence, defect rate, and code quality, then compares them with micro-level agent actions.
- The core measurement idea is **causal emergence** via Effective Information (EI): if a coarse-grained macro description of the ecosystem predicts future states better than the full micro description of agent actions, then the ecosystem level has stronger causal power.
- The paper then derives seven falsifiable propositions, including phase-transition style behavior as agent connectivity increases, and claims at least one proposition is testable with public data.

## Results
- The paper is mainly theoretical. It does **not** report new experimental quantitative results from an executed study in the provided excerpt.
- It cites prior evidence that autonomous coding pipelines show **41% to 86.7% failure rates** (Cemri et al., 2025).
- It cites benchmark evidence that agents solving isolated tasks on **SWE-bench Verified reach 65% issue resolution**, but only **21% on SWE-EVO**, where task dependencies cross agent boundaries (Thai et al., 2025).
- It cites GitClear's analysis over **211 million changed lines**, claiming code quality degradation correlates with higher AI-assisted development intensity.
- It cites **19% productivity slowdown** for experienced developers using AI tools (METR, 2025).
- It cites the 2024 DORA report, which recorded **7.2% lower delivery stability** alongside **25% higher AI-tool adoption**. The paper's own contribution is a theory, a measurement framework, and falsifiable propositions rather than a new benchmark result.

## Link
- [http://arxiv.org/abs/2604.19827v1](http://arxiv.org/abs/2604.19827v1)
