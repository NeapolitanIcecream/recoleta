---
source: arxiv
url: http://arxiv.org/abs/2603.14523v1
published_at: '2026-03-15T17:59:51'
authors:
- Chaoyang Wang
- Wenrui Bao
- Sicheng Gao
- Bingxin Xu
- Yu Tian
- Yogesh S. Rawat
- Yunhao Ge
- Yuzhang Shang
topics:
- vision-language-action
- embodied-ai
- multimodal-reasoning
- robot-manipulation
- tool-use
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# VLA-Thinker: Boosting Vision-Language-Action Models through Thinking-with-Image Reasoning

## Summary
This paper proposes VLA-Thinker, which turns robot vision from a one-time input into a component that can be actively invoked during reasoning, enabling the model to "look, think, and act" at the same time. It aims to improve the robustness and success rate of vision-language-action models on long-horizon manipulation tasks.

## Problem
- Existing CoT-enabled VLA methods are still mostly based on **text-dominant reasoning**: images are encoded only once at the beginning, and subsequent reasoning cannot actively revisit the environment.
- This static visual context limits the model's ability to handle **ambiguity, subgoal tracking, and error correction during execution**, especially in long-horizon manipulation tasks.
- This matters because directly learning the full mapping from perception to action typically requires large amounts of high-quality demonstration data, whereas stronger reasoning and active perception can improve data efficiency and decision robustness.

## Approach
- The core mechanism is **thinking-with-image**: during reasoning, the model not only generates textual thoughts, but can also invoke tools by treating "requesting new visual information" as an explicit action.
- Specifically, the model alternates among textual reasoning steps, visual tool calls, and final actions, forming an **interleaved perception-reasoning-action trajectory** rather than looking at the image only once at the start.
- The visual tool currently implemented is **ZOOM-IN**, which zooms into a specified region of the image to inspect details, allowing the model to obtain task-relevant local visual evidence during intermediate reasoning stages.
- Training is conducted in two stages: first, **SFT cold start** on synthetic visual CoT data teaches the model the basic reasoning format and when to call tools; then **GRPO** is used for trajectory-level reinforcement learning, aligning full reasoning-action trajectories with task success and format rewards.
- To construct the training data, the authors use Qwen3-VL-30B-A3B-Instruct to generate structured CoT and tool-call annotations for key frames and intermediate frames, with schema and temporal-consistency constraints.

## Results
- On **LIBERO**, VLA-Thinker achieves an average success rate of **97.5%**, an improvement of **+6.5 percentage points** over the backbone **OpenVLA-OFT at 91.0%**.
- LIBERO breakdown: **Spatial 98.7 vs 91.6 (+7.1)**, **Object 99.0 vs 95.3 (+3.7)**, **Goal 95.2 vs 90.6 (+4.6)**, **Long 96.9 vs 86.5 (+10.4)**, indicating especially strong gains on long-horizon tasks.
- On **RoboTwin 2.0**, the authors report hierarchical average success rates of **62.3% (short-horizon)**, **70.7% (medium-horizon)**, and **64.6% (long/extra-long-horizon)**.
- Compared with **OpenVLA-OFT**, the corresponding average improvements on RoboTwin 2.0 are **+41.0**, **+23.6**, and approximately **+18.1** percentage points respectively (computed from 64.6 vs 46.5).
- Several individual RoboTwin tasks show large gains, for example **Lift Pot 64.8 vs 10.1 (+54.7)** and **Beat Hammer Block 82.5 vs 28.1 (+54.4)** in the short-horizon setting, and **Handover Mic 89.9 vs 45.3 (+44.6)** in the medium-horizon setting.
- The paper also claims that this is the **first VLA model to support thinking-with-image**, and that training was completed in about **3 days** on **8×H100** using only single-view image input.

## Link
- [http://arxiv.org/abs/2603.14523v1](http://arxiv.org/abs/2603.14523v1)
