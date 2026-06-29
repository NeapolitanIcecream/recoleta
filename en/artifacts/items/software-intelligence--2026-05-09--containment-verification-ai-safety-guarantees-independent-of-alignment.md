---
source: arxiv
url: https://arxiv.org/abs/2605.09045v1
published_at: '2026-05-09T16:36:45'
authors:
- Royce Moon
- Lav R. Varshney
topics:
- ai-safety
- formal-verification
- agentic-systems
- dafny
- runtime-containment
- software-engineering
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Containment Verification: AI Safety Guarantees Independent of Alignment

## Summary
Containment verification proves safety properties in the agent runtime instead of relying on the model to behave. The paper verifies PocketFlow in Dafny so every typed AI action must pass a checked boundary policy.

## Problem
- Agentic AI systems can trigger external effects such as filesystem reads, tool calls, network access, financial actions, database changes, or infrastructure tampering.
- Model-level safety methods depend on learned behavior, which the paper says cannot be formally verified and can fail in deployment.
- The method matters for boundary failures: if every effect crosses a typed action interface, the runtime can block out-of-policy effects even when the model emits hostile or unexpected actions.

## Approach
- The AI is modeled as a havoc oracle: a Dafny external method that can return any value in the typed `Action` space.
- Safety policies are written over action arguments, modeled boundary events, and system state. The claim depends on effect exclusivity: every relevant external effect must pass through the modeled interface.
- The proof uses forward-simulation refinement between an abstract boundary-safety state machine and the concrete PocketFlow operational model.
- The Dafny proof checks that every concrete boundary event matches an abstract safe event, so rejected actions become no-effect events rather than unmodeled behavior.
- An agentic synthesis pipeline generates the specification, operational model, and refinement proof, with an information barrier and validation gates to reduce tautological or vacuous specs.

## Results
- Theorem 3.2 claims universal boundary safety: for every trace under any concrete oracle, the concrete policy holds at every step, if abstract havoc safety, boundary-event refinement, and effect exclusivity hold.
- The PocketFlow instantiation uses a typed action interface with 4 variants: `NoAction`, `ReadPathAction`, `ToolCallAction`, and `StepAction`.
- The verified boundary policy induces 3 recorded invariants: every read path stays under the workspace root, every tool call is allowlisted, and the step counter stays within its bound.
- The proof is mechanized in Dafny and includes named lemmas such as `RefinementInit`, `RefinementNext`, and `ContainmentVerificationSoundness`.
- The synthesis process has 7 phases and adds resolution, vacuity, and discrimination gates before iterative Dafny proof repair.
- The excerpt gives no runtime benchmark, throughput result, attack-success rate, or comparison table; its strongest empirical claim is a Dafny-checked PocketFlow verification artifact.

## Link
- [https://arxiv.org/abs/2605.09045v1](https://arxiv.org/abs/2605.09045v1)
