---
source: arxiv
url: http://arxiv.org/abs/2604.18000v1
published_at: '2026-04-20T09:25:30'
authors:
- Haiweng Xu
- Sipeng Zheng
- Hao Luo
- Wanpeng Zhang
- Ziheng Xi
- Zongqing Lu
topics:
- vision-language-action
- robot-benchmarking
- embodied-reasoning
- generalist-robot-policy
- semantic-grounding
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models

## Summary
This paper argues that high scores on standard Vision-Language-Action benchmarks often overstate real embodied reasoning ability. It introduces BeTTER, a diagnostic benchmark that applies controlled task interventions and shows that current VLAs break under shifts that require grounding, state tracking, and subgoal composition.

## Problem
- Standard robotic benchmarks can reward imitation and shortcut use, so strong success rates may not mean a model actually understands instructions, tracks task state, or plans multi-step behavior.
- Existing robustness benchmarks often vary appearance or layout but do not cleanly separate reasoning failures from low-level control or perception limits.
- This matters for robot foundation models because a policy that works in static in-domain settings can fail when object layouts, task order, or semantic distractors change.

## Approach
- The paper introduces **BeTTER** (Benchmark for Testing True Embodied Reasoning), a benchmark with 10 base manipulation tasks expanded into 60 task variations through controlled interventions.
- It probes four reasoning axes at test time: spatial layout shift, primitive recomposition, adversarial object perturbation, and temporal extrapolation.
- The benchmark uses template-based task generation, open-vocabulary 3D asset retrieval, and procedural trajectory amplification from a small set of teleoperated demonstrations.
- It logs privileged simulator state such as depth, boxes, and segmentation masks so failures can be analyzed as reasoning errors rather than pure execution noise.
- The authors evaluate three VLAs: pi_0.5, GR00T-N1.6, and Being-H0.5, and also report real-robot stress tests to check that the failures are not only simulation artifacts.

## Results
- On an instruction-grounding stress test with a 50% random baseline, models show strong polarization instead of stable grounding: **pi_0.5** gets **65.0%** on "top", **50.0%** on "bottom", **70.0%** on "red", **35.0%** on "blue"; **GR00T-N1.6** gets **100.0%**, **100.0%**, **5.0%**, **5.0%**; **Being-H0.5** gets **100.0%**, **30.0%**, **95.0%**, **45.0%**.
- On subgoal recomposition, all three models collapse on the unseen composition **B->C** compared with seen sequences **A->B** and **A->C**. **pi_0.5** drops from **60.0/45.0** to **5.0** success rate (**-47.5**), **GR00T-N1.6** from **75.0/40.0** to **15.0** (**-42.5**), and **Being-H0.5** from **65.0/40.0** to **0.0** (**-52.5**).
- In an adversarial instance-level semantic test, **pi_0.5** rejects a visually similar distractor in **85%** of trials, which the paper presents as partial robustness in a simple setting.
- For cluttered scenes and unseen layouts, the paper says all models show high Distractor Grasp Rate, but the excerpt does not provide the exact DGR numbers.
- The main claimed finding is that current VLAs rely on shortcut correlations such as lexical-kinematic mappings, layout bias, behavioral inertia, and weak causal state tracking, and these failures also appear on real robots according to the authors' stress tests.

## Link
- [http://arxiv.org/abs/2604.18000v1](http://arxiv.org/abs/2604.18000v1)
