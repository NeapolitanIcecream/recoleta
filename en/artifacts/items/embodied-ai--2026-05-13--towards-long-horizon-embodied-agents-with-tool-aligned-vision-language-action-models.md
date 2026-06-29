---
source: arxiv
url: https://arxiv.org/abs/2605.13119v1
published_at: '2026-05-13T07:40:34'
authors:
- Zixing Lei
- Changxing Liu
- Yichen Xiong
- Minhao Xiong
- Yuanzhuo Ding
- Zhipeng Zhang
- Weixin Li
- Siheng Chen
topics:
- vision-language-action
- robot-foundation-models
- generalist-robot-policy
- long-horizon-manipulation
- robot-tool-use
- instruction-alignment
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Towards Long-horizon Embodied Agents with Tool-Aligned Vision-Language-Action Models

## Summary
The paper proposes VLAs-as-Tools: a VLM planner calls specialized VLA policies as bounded robot tools for long-horizon manipulation. Tool-Aligned Post-Training trains those tools to follow explicit subtask calls and report progress.

## Problem
- Current VLA policies can execute language-conditioned robot actions, but long-horizon tasks require decomposition, state tracking, recovery, and skill composition.
- Planner-based robot agents can decompose tasks, but many use hand-built or narrow skills that are weaker than modern VLA controllers.
- A standard VLA may ignore the exact tool call and follow visual priors or demonstration bias, which makes it unreliable when placed behind a high-level planner.

## Approach
- A high-level VLM handles scene analysis, global planning, tool selection, and recovery.
- Each tool call contains a discrete tool-family label, such as grasp, open, or place, plus a scene-grounded local instruction.
- A selected VLA tool executes only a bounded subtask window, then returns progress feedback so the planner can replan without polling every low-level step.
- Tool-Aligned Post-Training segments demonstrations into invocation-labeled windows and trains on the same unit used at test time: tool family, local instruction, actions, and progress.
- Tool-family residual adapters give each tool family its own low-rank execution path on top of a shared VLA backbone.

## Results
- In imitation-learning results on LIBERO-Long, TAPT with the tool-family interface improves OpenVLA from 77.2% to 82.4% success rate, OpenVLA-OFT from 92.0% to 95.6%, and π0.5 from 92.4% to 97.2%.
- On RoboTwin, the same setup improves OpenVLA from 1.9% to 5.7%, OpenVLA-OFT from 16.9% to 52.4%, and π0.5 from 39.4% to 62.5% success rate.
- For π0.5, the paper claims gains of +4.8 points on LIBERO-Long and +23.1 points on RoboTwin over the corresponding single-model SFT baseline.
- In reinforcement-learning results on LIBERO-Long, TAPT plus the VLA tool-family interface reaches 82.6% for OpenVLA-OFT versus 78.8% with standard RL, and 91.2% for π0.5 versus 80.0% with standard RL.
- On LIBERO-CF-Long invocation fidelity, full TAPT raises OpenVLA-OFT Non-biased Rate from 31.2% to 47.4% and π0.5 Non-biased Rate from 39.6% to 54.6%.
- Full TAPT also raises Faithful Rate on LIBERO-CF-Long from 19.4% to 54.0% for OpenVLA-OFT and from 24.8% to 54.8% for π0.5.

## Link
- [https://arxiv.org/abs/2605.13119v1](https://arxiv.org/abs/2605.13119v1)
