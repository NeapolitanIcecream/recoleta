---
source: arxiv
url: http://arxiv.org/abs/2604.13654v1
published_at: '2026-04-15T09:20:02'
authors:
- Hanxuan Chen
- Jie Zheng
- Siqi Yang
- Tianle Zeng
- Siwei Feng
- Songsheng Cheng
- Ruilong Ren
- Hanzhong Guo
- Shuai Yuan
- Xiangyue Wang
- Kangli Wang
- Ji Pei
topics:
- uav-vln
- vision-language-action
- world-models
- sim2real
- embodied-ai
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Vision-and-Language Navigation for UAVs: Progress, Challenges, and a Research Roadmap

## Summary
This paper is a survey of vision-and-language navigation for UAVs. It organizes the field, defines the task formally, reviews methods and benchmarks, and lays out the main blocks to real-world deployment.

## Problem
- UAV-VLN asks a drone to follow natural-language instructions and navigate long distances in complex 3D environments.
- This matters for search and rescue, infrastructure inspection, wildfire monitoring, and GPS-denied operation where manual control or fixed interfaces do not scale well.
- UAVs face harder conditions than ground robots: continuous 3D control, partial observability, language ambiguity, outdoor perception shifts, and a large sim-to-real gap.

## Approach
- The paper frames UAV-VLN as a Partially Observable Markov Decision Process (POMDP), with hidden world state, multimodal observations, a language instruction, and a policy that maps observation history to actions.
- It builds a taxonomy of methods across three stages: modular and early learning systems, long-horizon spatiotemporal models, and foundation-model-driven agentic systems.
- The survey tracks the shift from classical SLAM/planning/control pipelines and CNN-RNN fusion models to transformers, visual-language maps, cognitive maps, VLM planners, VLA policies, and world-model-plus-VLA systems.
- It also reviews the support stack for the field: simulators, datasets, and evaluation metrics such as Success Rate (SR) and Success weighted by Path Length (SPL).
- The roadmap centers on four deployment limits named in the paper: sim-to-real transfer, robust outdoor perception, reasoning under ambiguous language, and running large models on constrained onboard hardware.

## Results
- This is a survey paper, not a new benchmark or model paper. The provided excerpt gives no new quantitative headline results such as SR, SPL, or win rates.
- The paper’s main claim is structural: it offers a unified taxonomy from early modular methods to recent VLM, VLA, and world-model-integrated agents for UAV navigation.
- It formalizes UAV-VLN as a POMDP and notes an extension to DEC-POMDP for multi-agent settings.
- It identifies named method examples across the timeline, including AerialVLN baselines (2023), HAMT (2023), VLMaps (2023), FlightGPT (2024), OpenVLA 7B (2024), $\pi_{0}$ (2024), GR00T N1 (2025), and Cosmos-Reason1 (2025).
- The excerpt includes a few concrete implementation details from cited systems rather than benchmark gains: memory-based DRL at 60 Hz, and GRaD-Nav++ with onboard real-time control at 25 Hz.
- The strongest concrete contribution in the excerpt is the research roadmap: future work should target world-model-guided aerial reasoning, better sim-to-real transfer, safer and more efficient onboard deployment, and multi-agent swarm or air-ground collaboration.

## Link
- [http://arxiv.org/abs/2604.13654v1](http://arxiv.org/abs/2604.13654v1)
