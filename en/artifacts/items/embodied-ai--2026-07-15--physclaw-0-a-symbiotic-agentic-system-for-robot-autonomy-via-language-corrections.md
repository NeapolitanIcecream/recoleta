---
source: arxiv
url: https://arxiv.org/abs/2607.14047v1
published_at: '2026-07-15T17:16:24'
authors:
- Boyuan Wang
- Zhenyuan Zhang
- Zhiqin Yang
- Peijun Gu
- Shuya Wang
- Xiaofeng Wang
- Xianghui Ze
- Yifan Chang
- Guosheng Zhao
- Jiangnan Shao
- Guan Huang
- Hengyu Liu
- Yonggang Zhang
- Wei Xue
- Chunyuan Guan
- Chenglin Pu
- Yike Guo
- Xingang Wang
- Zheng Zhu
topics:
- robot-data-scaling
- vision-language-action
- generalist-robot-policy
- language-correction
- autonomous-data-collection
- robot-foundation-model
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# PhysClaw-0: A Symbiotic Agentic System for Robot Autonomy via Language Corrections

## Summary
PhysClaw-0 is a human-robot data-collection system that stores operator language corrections as reusable rules, reducing repeated supervision during long-running manipulation sessions. On a real-robot desktop-clearing task, it matched teleoperation-level collection and downstream policy success while using substantially less human working time.

## Problem
- Real-world trajectory collection for VLA and manipulation policies requires either continuous teleoperation or autonomous pipelines that can repeatedly fail on long-tail problems such as incorrect verification criteria, reset drift, and unsuitable grasp strategies.
- Corrections limited to one episode must be repeated whenever the same failure recurs, so human oversight grows with repeated episodes rather than with the number of distinct failure modes.
- This matters because data quantity and quality are major bottlenecks for improving robot policies, while human collection time is expensive.

## Approach
- PhysClaw-0 runs a collect-verify-reset loop in which a VLM checks both collection and reset phases and requests human help only after a phase exceeds an explicit retry budget, set to 3 attempts by default.
- An LLM parses remote operator utterances into structured adjustments to verification prompts, grasp or execution strategies, object priorities, or retry limits.
- Persistent corrections are stored in a human-readable Corrective Memory with trigger, correction, scope, and source-utterance fields; matching rules are consulted in later rounds, while one-off corrections are not retained.
- Episodes are filtered using execution, outcome, and recording-quality labels, then used to fine-tune the underlying VLA policy. The system changes behavior through text during collection and changes policy weights only indirectly through the collected data.

## Results
- On a real-robot dual-arm Piper desktop-clearing testbed, collecting 50 valid demonstrations required 4.8 minutes of human working time with PhysClaw-0 versus 30.0 minutes with full teleoperation, or 16% of the teleoperation time.
- PhysClaw-0 matched the episode collection success rate of full human teleoperation and produced a fine-tuned policy with an 80% deployment success rate, matching the policy trained on teleoperation data.
- Language corrections improved verifier agreement with human labels in all four evaluated settings: three reached 10/10, while the hardest setting improved from 0/10 to 4/10.
- Execution corrections increased average single-attempt collection success from 12.5% to 47.5% through cumulative segmentation and grasp-depth corrections; a controlled arm-selection correction increased it from 20.0% to 50.0%.
- The paper evaluates one collect-train-deploy cycle on a single desktop-clearing task; full multi-round validation of the proposed data flywheel remains future work.

## Link
- [https://arxiv.org/abs/2607.14047v1](https://arxiv.org/abs/2607.14047v1)
