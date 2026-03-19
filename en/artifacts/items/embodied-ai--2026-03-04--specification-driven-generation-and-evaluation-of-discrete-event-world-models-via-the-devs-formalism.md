---
source: arxiv
url: http://arxiv.org/abs/2603.03784v1
published_at: '2026-03-04T06:50:32'
authors:
- Zheyu Chen
- Zhuohuan Li
- Chuanhao Li
topics:
- world-models
- discrete-event-systems
- devs
- llm-code-generation
- trace-based-verification
relevance_score: 0.6
run_id: materialize-outputs
language_code: en
---

# Specification-Driven Generation and Evaluation of Discrete-Event World Models via the DEVS Formalism

## Summary
This paper proposes a method for automatically generating **discrete-event world models** from natural-language specifications: it uses the DEVS formalism to represent environments as executable simulators, and evaluates whether they conform to the specification through rule checking based on event traces. The goal is to find a more verifiable, debuggable, and online-adaptable middle ground between "hand-crafted explicit simulators" and "implicit neural world models."

## Problem
- Existing world models often lie at two extremes: **hand-crafted simulators** are reliable but hard to adapt, while **implicit neural models** are flexible but difficult to constrain, verify, and debug over long-horizon rollouts.
- For many environments governed by **event ordering, timing, and causality** (such as queueing systems, workflows, message-driven multi-agent settings, and some embodied task-planning tasks), there is a need for a world model that is both explicit and quick to generate.
- When generating such models from natural language, there is **no unique code-level ground truth**, so traditional evaluation standards such as comparison against a reference implementation or stepwise prediction accuracy are not suitable.

## Approach
- The paper uses **DEVS (Discrete Event System Specification)** as the representation for world models: the environment is decomposed into atomic components with local state, input/output events, internal/external/confluent transitions, and time-advance functions, which are then connected into a hierarchical system through coupled models.
- It proposes a **staged LLM generation pipeline**: first performing structural synthesis to infer component hierarchies, port schemas, and interaction graphs; then performing behavioral synthesis to generate event-handling and timing code for each atomic component.
- The generated results are constrained through a fixed **interface contract**: the simulator accepts external intervention configurations/input streams and outputs a unified JSONL event trace, reducing coupling and context burden in multi-component code generation.
- Evaluation does not require matching some "standard implementation"; instead, the simulator emits **structured event traces**, and these traces are checked against temporal and semantic constraints derived from the specification, such as precedence relations, response constraints, time bounds, and safety/conservation properties.
- Once a constraint is violated, the framework can provide **localized diagnostics**, identifying which rule was violated and which entities/state variables were involved, making it easier to iteratively refine the generated model.

## Results
- The paper's main contribution is a **method and framework**: it proposes a discrete-event world modeling approach based on "specification-driven generation + trace-driven verification," aiming to achieve **long-horizon consistency, reproducibility, verifiability**, and **fast on-demand synthesis**.
- The paper explicitly claims that the generated models apply to a class of environments dominated by discrete events, including **queueing/service operations, embodied task planning, and message-mediated multi-agent coordination**, but the provided excerpt **does not report specific experimental metrics, dataset sizes, or baseline comparison numbers**.
- The generation pipeline is described as using DEVS modularity to enable **parallel generation of atomic components**, thereby improving the feasibility of online on-demand synthesis; this is a qualitative claim, and the excerpt **does not provide numerical results on generation speed, success rate, or ablation studies**.
- The evaluation framework can perform **reproducible verification and localized diagnostics** based on event traces, replacing code-equivalence-based evaluation; however, the excerpt **does not provide quantitative comparisons such as constraint satisfaction rates, diagnostic accuracy, or comparisons with single-stage generation or implicit world models**.

## Link
- [http://arxiv.org/abs/2603.03784v1](http://arxiv.org/abs/2603.03784v1)
