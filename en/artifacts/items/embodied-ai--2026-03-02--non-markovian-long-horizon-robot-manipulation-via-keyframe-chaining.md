---
source: arxiv
url: http://arxiv.org/abs/2603.01465v1
published_at: '2026-03-02T05:26:29'
authors:
- Yipeng Chen
- Wentao Tan
- Lei Zhu
- Fengling Li
- Jingjing Li
- Guoli Yang
- Heng Tao Shen
topics:
- vision-language-action
- long-horizon-manipulation
- non-markovian-memory
- keyframe-retrieval
- generalist-robot-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Non-Markovian Long-Horizon Robot Manipulation via Keyframe Chaining

## Summary
This paper proposes Keyframe-Chaining VLA, which replaces dense short-window history with sparse but semantically critical historical frames, enabling robots to remember the truly important past in long-horizon, non-Markovian manipulation tasks. The core idea is to automatically identify “key moments” during execution and chain these frames together for retrieval by the VLA policy.

## Problem
- Existing VLAs mostly rely on current observations or short dense history, implicitly assuming tasks are approximately Markovian; however, many long-horizon manipulation tasks require remembering critical events that occurred earlier.
- Directly extending the context window increases attention computation cost, making it difficult to meet real-time robot control requirements.
- Existing retrieval, compression, or hierarchical planning methods either lose fine-grained spatiotemporal information or infer too slowly, and still struggle to handle non-Markovian dependencies where **the current action is determined only by specific past states**.

## Approach
- Proposes **Keyframe-Chaining VLA**: first using an independent Keyframe Selection Module (KSM) to select a small number of semantically important frames online from a continuous visual stream, then feeding these keyframes together with the current observation into the VLA policy.
- KSM is trained in two stages: first, it uses triplet loss to learn a visual embedding space that distinguishes different tasks/stages/temporal neighborhoods; then, a task-conditioned query network generates queries based on the task and current execution stage to match whether the next semantic milestone has been reached.
- The query mechanism uses FiLM to modulate the phase embedding, so that “the same stage concept” carries different semantics across tasks; it then uses cross-attention over sliding-window visual features to obtain matching scores, and frames are cached as keyframes once the score exceeds a threshold.
- To reduce jitter and false triggers, the authors add greedy temporal smoothing: the candidate keyframe is continuously updated within a validation window, and is only finally committed after the score falls back and stabilizes.
- The action policy uses a GR00T-N1.5/flow-matching backbone, without modifying the backbone architecture; it only injects historical keyframes as interleaved visual tokens and structured prompts, achieving global temporal awareness at relatively low cost.

## Results
- On **4 non-Markovian ManiSkill tasks** newly built by the authors, the method achieves an average success rate of **92.0%**, significantly higher than the strongest baseline at **57.0%**, an absolute gain of **35.0 percentage points**.
- By task, Keyframe-Chaining VLA achieves: **Spatial 70.0%**, **Temporal 98.0%**, **Identity 100.0%**, **Counting 100.0%**.
- Compared with representative baselines: **π0** averages only **15.5%**; **Diffusion Policy** averages **15.5%**; **GR00T-N1.5 (No History)** averages **16.0%**.
- Short-term dense history is still insufficient: when GR00T-N1.5 uses short-term history, the best average is only about **27.0%** (**N_h=3, I=1**), far below the authors’ **92.0%**.
- The strongest fixed-stride long-horizon sampling configuration averages **57.0%** (**GR00T-N1.5, N_h=3, I=40**), still clearly behind keyframe-chained history; this suggests that “choosing the right historical frames” is more effective than “mechanically extending history.”
- The paper also claims significantly better performance than baselines in real-world long-horizon deployment, but the provided excerpt does not include corresponding quantitative results.

## Link
- [http://arxiv.org/abs/2603.01465v1](http://arxiv.org/abs/2603.01465v1)
