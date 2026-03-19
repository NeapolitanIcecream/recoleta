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
- robot-manipulation
- vision-language-action
- long-horizon-planning
- non-markovian-memory
- keyframe-retrieval
relevance_score: 0.2
run_id: materialize-outputs
language_code: en
---

# Non-Markovian Long-Horizon Robot Manipulation via Keyframe Chaining

## Summary
This paper proposes Keyframe-Chaining VLA, which enables robots to remember the truly important past in long-horizon, non-Markovian manipulation tasks by automatically selecting and chaining a small number of key historical frames. Its core value lies in replacing dense history windows with sparse semantic memory, significantly improving long-term dependency reasoning under lower temporal redundancy.

## Problem
- Existing VLA models often rely mainly on the current observation or a very short history window, making them difficult to apply to **non-Markovian** tasks, where the correct action depends on certain past states rather than the current scene.
- Directly extending the context window causes attention computation costs to surge, making it difficult to meet the real-time control requirements of robots.
- Existing retrieval, compression, or hierarchical planning methods either lose fine-grained spatial information or infer too slowly, and they also struggle to stably resolve state aliasing.

## Approach
- Proposes **Keyframe-Chaining VLA**: instead of preserving an entire dense video sequence, it extracts a small number of “semantic keyframes” online and feeds them together with the current observation into the VLA policy.
- Designs a two-stage **Keyframe Selection Module (KSM)**: first trains a visual encoder with metric learning to learn an embedding space that can distinguish task stages; then uses a task-modulated query network to match whether a key milestone has been reached based on the current task/stage.
- The query mechanism uses **FiLM** to inject task identity into a shared stage representation, and then uses cross-attention to determine from the recent visual window whether a keyframe should be triggered, thereby enabling “progress-aware” historical retrieval.
- To reduce online jitter and false detections, it adds greedy temporal smoothing: a candidate keyframe is only formally written into the history buffer after a validation window.
- On the policy side, it uses **GR00T-N1.5** as the backbone, forming a sparse semantic history from historical keyframes and current observations, and conditions a flow-matching action head with interleaved visual tokens / structured prompt tokens.

## Results
- On the **4 ManiSkill non-Markovian tasks** constructed by the authors, the method achieves an average success rate of **92.0%**, significantly higher than the strongest baseline at **57.0%**, an absolute improvement of **35.0 percentage points**.
- Compared with **GR00T-N1.5** without history, its average success rate improves from **16.0%** to **92.0%**; compared with short-history GR00T (best table average **27.0%**), the improvement is even larger.
- For the four tasks, it achieves: **Spatial 70.0%**, **Temporal 98.0%**, **Identity 100.0%**, and **Counting 100.0%**.
- The strongest fixed-step long-horizon sampling baseline is **GR00T-N1.5, N_h=3, I=40**, with an average of **57.0%**; the authors’ method further exceeds this baseline by **35.0 percentage points** while maintaining a sparse memory representation.
- Other representative baselines perform substantially worse: **π0** averages **15.5%**, and **Diffusion Policy** averages **15.5%**, indicating that relying only on the current or short local context is insufficient for solving memory-dependent tasks.
- The paper also claims that the method outperforms baselines in real-world long-horizon deployment, but the provided excerpt does not include corresponding quantitative results on real robots.

## Link
- [http://arxiv.org/abs/2603.01465v1](http://arxiv.org/abs/2603.01465v1)
