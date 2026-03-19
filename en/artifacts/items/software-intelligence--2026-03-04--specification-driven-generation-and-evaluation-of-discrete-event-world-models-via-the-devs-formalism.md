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
- devs
- discrete-event-simulation
- llm-code-generation
- trace-based-verification
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Specification-Driven Generation and Evaluation of Discrete-Event World Models via the DEVS Formalism

## Summary
This paper proposes a method for automatically generating executable discrete-event world models from natural-language environment specifications, centered on the DEVS formalism and a staged LLM code-generation process. It also presents an evaluation method based on event traces and specification constraints, used to verify whether a model satisfies requirements when no unique ground-truth implementation exists.

## Problem
- Existing world models often swing between two extremes: hand-built simulators are **reliable but hard to adapt**, while implicit neural models are **flexible but hard to constrain, hard to verify, and prone to long-horizon drift**.
- For environments governed by **event order, timing, and causality** (such as queues, workflows, distributed systems, and message-coordinated multi-agent settings), there is a need for an explicit world model that can be generated online while remaining consistent over long horizons.
- Natural-language specifications usually **do not have a single uniquely correct code implementation**, so evaluation cannot rely only on comparison to a reference implementation; instead, it must judge whether observable behavior satisfies the specification, which is important for reproducible evaluation.

## Approach
- Use **DEVS** as the world-model representation: decompose the environment into atomic and coupled components, with each component explicitly defining state, input/output events, internal/external transitions, and time advance.
- Adopt a **two-stage LLM generation pipeline**: first perform structural generation (component hierarchy, ports, interaction graph, PlanTree), then behavioral generation (event logic and timing logic for each atomic component).
- Constrain generated outputs through **interface contracts/JSON schema**, so each component can be generated independently within local context while preserving global consistency, supporting parallel generation and online on-demand synthesis.
- The generated simulator exposes a standardized execution interface and outputs **JSONL event traces** in a unified schema during runtime, recording time, entity, event type, and payload.
- Evaluation does not depend on code-level ground truth; instead, traces are checked against **temporal constraints and semantic invariants** derived from the specification, with localized diagnostic feedback when violations occur.

## Results
- The abstract and excerpt **do not provide quantitative experimental results**; they do not report specific datasets, pass rates, accuracy, cost, or relative gains over baselines.
- The paper’s strongest concrete claim is that the generated discrete-event world models can maintain more consistent behavior over **long-horizon rollouts**, and are easier to constrain, verify, and debug than implicit world models.
- The authors claim the method supports **efficient on-demand synthesis** of executable simulators from natural language, especially for discrete-event environments such as queueing/service systems, workflows, embodied task planning, and message-driven multi-agent coordination.
- The authors also claim that trace-level verification enables **reproducible black-box evaluation** and **localized error diagnosis**, allowing specification compliance to be checked even when no unique reference implementation exists.

## Link
- [http://arxiv.org/abs/2603.03784v1](http://arxiv.org/abs/2603.03784v1)
