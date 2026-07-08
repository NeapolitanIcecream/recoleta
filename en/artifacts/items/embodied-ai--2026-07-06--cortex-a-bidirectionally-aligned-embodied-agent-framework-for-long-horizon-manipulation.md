---
source: arxiv
url: https://arxiv.org/abs/2607.05377v1
published_at: '2026-07-06T17:55:05'
authors:
- Jiaqi Peng
- Xiqian Yu
- Delin Feng
- Yuqiang Yang
- Wenzhe Cai
- Jing Xiong
- Ganlin Yang
- Jinliang Zheng
- Jiafei Cao
- Xueyuan Wei
- Jiangmiao Pang
- Yuan Shen
- Tai Wang
topics:
- vision-language-action
- long-horizon-manipulation
- generalist-robot-policy
- hierarchical-planning
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Cortex: A Bidirectionally Aligned Embodied Agent Framework for Long-horizon Manipulation

## Summary
Cortex is a hierarchical robot system for long-horizon manipulation that turns high-level goals into executable subtasks for a VLA policy. It reports gains in simulation and zero-shot real-world chemistry and washing tasks where end-to-end VLA baselines fail.

## Problem
- Monolithic VLA policies react to current observations and lose track of progress in long tasks, which causes repeated actions and compounding errors.
- Existing planner-executor systems often produce plans that the low-level robot policy cannot execute, especially when subtasks lack object attributes, spatial cues, or reachability constraints.
- The problem matters because real manipulation tasks such as washing labware or running a multi-step chemistry procedure require progress memory, subtask transitions, and physical grounding.

## Approach
- Cortex uses a high-level VLM to plan subtasks and maintain textual memory, while a low-level VLA executes the current subtask as robot actions.
- The interface limits plans to 32 canonical manipulation skill primitives, such as pick, place, stack, and unscrew, with strict language templates.
- The authors annotate more than 4,000 hours of open-source and real robot video with subtask metadata, then add 30 hours of simulation data with object attributes, spatial identifiers, interaction counts, and reachability-aware routing.
- Training uses event-balanced sampling so the VLM sees more frames near subtask boundaries, where it must decide whether to keep the current subtask, update memory, or emit the next subtask.
- At inference time, Cortex runs the VLM and VLA asynchronously and constrains VLM outputs to the VLA skill library through prompt and post-processing rules.

## Results
- Open-loop VLM evaluation: Cortex with the full harness reaches 8.318 average total score at step level, compared with Gemini at 6.925, Qwen3-VL-8B-Instruct at 6.739, and GPT-5 at 6.268.
- Open-loop episode-level evaluation: Cortex with the full harness scores 7.810 average total, compared with GPT-5 at 7.231, Gemini at 6.860, and Qwen3-VL-8B-Instruct at 6.292.
- LIBERO-Long zero-shot simulation: Cortex reaches 95.5% success, above pi_0.5 at 92.4%, MemoryVLA at 93.4%, OpenVLA-OFT at 94.5%, and Gemini-3.1-Pro at 91.0%.
- RoboTwin: the abstract reports 86.8% success, a 4.1-point gain over the monolithic pi_0.5 baseline; the long-horizon split reports 88.00% success.
- Real-world 14-step chemistry tasks over 20 trials: Cortex reaches 11.0/14 average progress and 65% success, while pi_0.5 and pi_mem both have 0% success.
- Real-world 14-step washing tasks over 20 trials: Cortex reaches 10.5/14 average progress and 55% success, while pi_0.5 and pi_mem both have 0% success; human subtask control with the same style of VLA policy reaches 70% success.

## Link
- [https://arxiv.org/abs/2607.05377v1](https://arxiv.org/abs/2607.05377v1)
