---
kind: trend
trend_doc_id: 104
granularity: day
period_start: '2026-04-12T00:00:00'
period_end: '2026-04-13T00:00:00'
topics:
- robotics
- vision-language-action
- goal-conditioning
- slot-placement
- benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-104
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/goal-conditioning
- topic/slot-placement
- topic/benchmarks
language_code: en
pass_output_id: 50
pass_kind: trend_synthesis
---

# Explicit goal markers anchor zero-shot robotic placement

## Overview
This period is dominated by one clear result: robotic placement is being framed as a precision grounding problem with an explicit target state. AnySlot turns a natural-language instruction into a visible goal marker, then lets a goal-conditioned Vision-Language-Action policy handle execution. The paper pairs that design with SlotBench, a tight slot-placement benchmark, and reports nearly 90% average success in zero-shot settings.

## Clusters

### Explicit visual goals for precise placement
AnySlot treats language grounding as a separate visual target before control. The system edits the scene with a colored marker on the intended slot, lifts that point into 3D, and projects it across camera views. The action policy then follows this explicit goal. That design fits the task: slot placement needs both semantic choice and tight geometric alignment, and the paper argues that bundling both into one flat policy makes dense layouts hard to handle.

#### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary describes the two-stage pipeline and why flat policies struggle on slot-level placement.

### Harder evaluation favors slot-aware control
The benchmark pressure is also clear. SlotBench asks for slot selection under tight tolerances, with about 3 cm slots and correctness defined within 2 cm of the true slot center. It spans nine reasoning categories, including ordinal, negation, affordance, and world knowledge. On that setup, the paper reports nearly 90% average success, while a visible flat Diffusion Policy baseline reaches 16% on ordinal reasoning and 0% on the other shown categories. The available excerpt does not expose the full comparison table, so the strongest grounded claim is that the task sharply separates explicit-goal control from flat baselines in the shown results.

#### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary gives SlotBench categories, geometry, tolerance, and reported average success.
