---
source: arxiv
url: http://arxiv.org/abs/2603.02765v1
published_at: '2026-03-03T04:04:28'
authors:
- George Bredis
- Nikita Balagansky
- Daniil Gavrilov
- Ruslan Rakhimov
topics:
- model-based-rl
- world-model
- representation-learning
- temporal-transformer
- partial-observability
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Next Embedding Prediction Makes World Models Stronger

## Summary
This paper proposes NE-Dreamer, a decoder-free world model for model-based reinforcement learning that learns state representations by predicting the “next-step encoder embedding” rather than reconstructing pixels. The core conclusion is: this temporally predictive representation learning is clearly stronger on partially observable tasks requiring memory and navigation, while not degrading on standard control benchmarks.

## Problem
- Existing world models with pixel inputs often rely on image reconstruction to learn representations, but reconstruction objectives are computationally heavy, difficult to optimize, and can waste capacity fitting visual details unrelated to control.
- Many decoder-free methods only enforce representation alignment at the **same timestep**, lacking explicit cross-time constraints; in partially observable environments, this can lead to representations that are not predictive and therefore struggle to support long-term memory and planning.
- This matters because in memory/navigation tasks such as DMLab, the agent must integrate information from history rather than simply react to the current frame.

## Approach
- NE-Dreamer retains the Dreamer-style RSSM world model and imagination-based actor-critic control backbone, but removes the pixel decoder.
- It uses a **causal temporal Transformer** to predict the next encoder embedding \(\hat e_{t+1}\) from the latent/state/action history up to time \(t\).
- The prediction target is the embedding \(e_{t+1}\) obtained by passing the true next frame through the encoder, but stop-gradient is applied to the target; in other words, the model learns to “predict future representations from history.”
- During training, it uses a **Barlow Twins**-style redundancy-reduction alignment loss so that the predicted embedding aligns with the target embedding on corresponding dimensions while reducing redundancy on non-corresponding dimensions, thereby avoiding collapse.
- Put simply, the core mechanism is: **instead of requiring the model to reconstruct the current image, it requires the model to correctly anticipate the high-level representation it will see at the next step from past information**.

## Results
- On **DMLab Rooms**, the authors claim that under **the same compute and model capacity** (**50M environment steps, 5 seeds, 12M parameters**), NE-Dreamer outperforms strong baselines including **DreamerV3, R2-Dreamer, DreamerPro**; however, the excerpt **does not provide a concrete score table or per-task values**.
- In mechanism ablations, removing the **causal Transformer** (w/o transformer) or removing the **next-step target shift** (w/o shift) causes performance to “substantially reduces / collapses / nearly complete loss of gains”; this supports the view that the performance improvement comes from “predictive sequence modeling,” but the excerpt **does not provide quantified drops**.
- On the **DeepMind Control Suite (DMC)**, under the setting of **1M environment steps, 5 seeds, 12M parameters**, the authors say NE-Dreamer **matches or slightly outperforms** DreamerV3 and other decoder-free baselines; the excerpt likewise **does not provide specific per-task means or aggregate score numbers**.
- In representation diagnostics, the authors freeze the latent and then train a post hoc decoder, claiming that NE-Dreamer’s latent more stably preserves object identity, spatial layout, and task-relevant information, whereas Dreamer/R2-Dreamer are more prone to temporal inconsistency; this is **qualitative evidence** without quantitative metrics.
- The strongest overall concrete claim is: on the **50M-step DMLab Rooms** memory/navigation tasks, NE-Dreamer outperforms existing decoder-based and decoder-free world models under the **same 12M parameter scale** and **5 random seeds**; on **1M-step DMC**, there is no performance regression.

## Link
- [http://arxiv.org/abs/2603.02765v1](http://arxiv.org/abs/2603.02765v1)
