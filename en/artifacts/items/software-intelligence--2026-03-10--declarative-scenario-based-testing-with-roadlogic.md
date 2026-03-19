---
source: arxiv
url: http://arxiv.org/abs/2603.09455v1
published_at: '2026-03-10T10:11:09'
authors:
- Ezio Bartocci
- Alessio Gambi
- Felix Gigler
- Cristinel Mateis
- "Dejan Ni\u010Dkovi\u0107"
topics:
- autonomous-driving
- scenario-testing
- declarative-specification
- answer-set-programming
- runtime-monitoring
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# Declarative Scenario-based Testing with RoadLogic

## Summary
This paper presents **RoadLogic**, which automatically converts declarative OpenSCENARIO DSL (OS2) into executable and verifiable autonomous driving simulations. It aims to fill the gap in open-source, systematic tooling between "high-level scenario specifications" and "concrete simulation instances."

## Problem
- Existing autonomous driving scenario testing mostly relies on imperative scenario authoring, requiring developers to manually enumerate a large number of variants, resulting in poor coverage and high cost.
- Declarative languages such as OS2 can describe more concisely "what kind of scenario is desired," but lack an open-source method for systematically instantiating specifications into concrete simulations.
- This matters because autonomous driving requires reproducible, scalable simulation-based validation across many traffic situations that are numerous, rare, and safety-critical.

## Approach
- First, OS2 scenarios are translated into a **symbolic automaton**, using states and constrained transitions to represent sequencing, parallelism, choice, and spatial/relational constraints.
- The automaton is then encoded as an **Answer Set Programming (ASP)** planning problem, allowing a solver to generate **high-level discrete plans** that satisfy the scenario constraints.
- Next, the high-level plans are refined into **waypoints/trajectory goals** for each vehicle and passed to the **FrenetiX** motion planner to generate physically feasible simulations in **CommonRoad**.
- Finally, a **specification-based monitor** generated from the same symbolic automaton checks the execution trajectories, retaining only simulation results that conform to the original OS2 semantics.

## Results
- The paper claims that **RoadLogic is the first open-source framework** capable of automatically instantiating declarative OS2 specifications into simulations that are "realistic and specification-satisfying."
- It is evaluated on **CommonRoad** using "multiple representative/diverse OS2 logical scenarios," and completes the end-to-end pipeline by combining **clingo** and **FrenetiX**.
- The core result given in the abstract is that the system can reliably generate simulations that are **highly realistic and specification-satisfying** within **minutes (within minutes)**.
- It also claims that **parameter sampling** can capture **diverse behavioral variants**, thereby supporting more systematic scenario-based testing.
- The provided excerpt **does not include finer-grained quantitative metrics** (such as success rate, average runtime, number of scenarios, or numerical comparisons with specific baselines), so a more complete numerical comparison cannot be reported.

## Link
- [http://arxiv.org/abs/2603.09455v1](http://arxiv.org/abs/2603.09455v1)
