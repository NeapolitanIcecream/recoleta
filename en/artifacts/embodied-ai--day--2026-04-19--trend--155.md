---
kind: trend
trend_doc_id: 155
granularity: day
period_start: '2026-04-19T00:00:00'
period_end: '2026-04-20T00:00:00'
topics:
- robotics
- vision-language navigation
- dexterous manipulation
- memory
- hardware design
run_id: materialize-outputs
aliases:
- recoleta-trend-155
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-navigation
- topic/dexterous-manipulation
- topic/memory
- topic/hardware-design
language_code: en
pass_output_id: 80
pass_kind: trend_synthesis
---

# Robotics research gets more explicit about memory and mechanism

## Overview
This day is small, but the signal is clear: robotics papers are making internal state and physical constraints explicit. Dual-Anchoring improves long-horizon navigation by supervising progress and landmark memory inside a Video-LLM. MM-Hand does the same on hardware, measuring the force and delay costs of remote tendon routing while keeping the hand lighter, more modular, and sensor-ready.

## Clusters

### State tracking in vision-language navigation
Dual-Anchoring makes long-horizon vision-language navigation more explicit about task state. The core idea is simple: force the model to state which instruction sub-goals are done, and force it to retain a landmark-level memory of where it has been. That supervision is large-scale, with 3.6M progress samples and 937K grounded landmark samples. The reported gains are strong on continuous-environment VLN benchmarks: success rate reaches 65.6 on R2R-CE and 61.7 on RxR-CE, with about +8.7 and +8.8 points over StreamVLN. In this small period, that makes memory and progress tracking the clearest algorithmic result.

#### Evidence
- [Dual-Anchoring: Addressing State Drift in Vision-Language Navigation](../Inbox/2026-04-19--dual-anchoring-addressing-state-drift-in-vision-language-navigation.md): Summary of the method, datasets, and benchmark gains.

### Remote-actuated dexterous hand design
MM-Hand focuses on hardware practicality in dexterous manipulation. It is a 21-DOF open-source hand with remote tendon actuation, modular 3D-printed structure, quick tendon connectors, and room for richer sensing in the hand itself. The engineering trade-off is measured, not hidden: a 1 m sheath gives 25 N fingertip force versus about 33 N with a 0.1 m sheath, and the controller still holds steady-state joint error below 0.1° with about 0.2 s delay. The paper also reports that friction matters more than arm-motion disturbance in its tracking tests. That makes this work useful as a research platform paper, not just a concept demo.

#### Evidence
- [MM-Hand: A 21-DOF Multi-modal Modular Dexterous Robotic Hand with Remote Actuation](../Inbox/2026-04-19--mm-hand-a-21-dof-multi-modal-modular-dexterous-robotic-hand-with-remote-actuation.md): Summary of the hand design, sensing stack, and main quantitative results.
