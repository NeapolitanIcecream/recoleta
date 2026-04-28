---
source: arxiv
url: http://arxiv.org/abs/2604.17473v1
published_at: '2026-04-19T15:03:38'
authors:
- Kangyi Wu
- Pengna Li
- Kailin Lyu
- Lin Zhao
- Qingrong He
- Jinjun Wang
- Jianyi Liu
topics:
- vision-language-navigation
- video-llm
- world-model
- instruction-following
- long-horizon-navigation
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Dual-Anchoring: Addressing State Drift in Vision-Language Navigation

## Summary
Dual-Anchoring targets state drift in vision-language navigation by forcing a Video-LLM to track instruction progress and remember visited landmarks. The paper claims this reduces long-horizon failures and sets new or near-best results on VLN-CE benchmarks.

## Problem
- In long navigation episodes, VLN agents lose track of which instruction steps are already done and which landmarks they have passed. The paper calls these failures **progress drift** and **memory drift**.
- Standard next-action training can produce correct local moves without keeping an accurate internal task state, so errors compound over long trajectories.
- This matters because VLN in continuous 3D environments depends on sustained alignment between language, visual history, and current position, especially on long instructions such as RxR-CE.

## Approach
- The method adds two training signals to a StreamVLN-style Video-LLM backbone, with no extra inference cost at deployment.
- **Instruction Progress Anchoring:** the model generates a short structured text description of completed vs. remaining sub-goals before predicting the next action. Training data for this comes from **3.6M** synthesized progress-description samples produced with Qwen3-VL.
- **Memory Landmark Anchoring:** the model learns to reconstruct SAM-based object-centric features for the most recently passed landmark, using a retrospective world-model loss. Supervision comes from **937K** grounded landmark samples mined with Qwen3/Qwen3-VL plus SAM features.
- The landmark branch uses a learnable spatial-query decoder with cross-attention over Video-LLM outputs, then minimizes MSE against frozen SAM features of the mined landmark frame.
- Training uses a two-stage pipeline: navigation pretraining with action loss plus the two anchoring losses, then DAgger and mixed fine-tuning with general vision-language data.

## Results
- On **R2R-CE val unseen**, the method reports **SR 65.6**, **SPL 62.1**, **OSR 69.2**, **NE 4.15**.
- On **RxR-CE val unseen**, it reports **SR 61.7**, **SPL 53.3**, **NE 4.42**.
- Compared with **StreamVLN**, performance improves from **56.9 to 65.6 SR** on R2R-CE (**+8.7 points**) and from **52.9 to 61.7 SR** on RxR-CE (**+8.8 points**). SPL improves from **51.9 to 62.1** on R2R-CE and from **46.0 to 53.3** on RxR-CE.
- Compared with **DualVLN**, the method is higher on **R2R-CE SR** (**65.6 vs 64.3**), **R2R-CE SPL** (**62.1 vs 58.5**), **RxR-CE SR** (**61.7 vs 61.4**), and **RxR-CE SPL** (**53.3 vs 51.8**), though **R2R-CE NE/OSR** are slightly worse (**4.15 vs 4.05**, **69.2 vs 70.7**).
- The abstract also claims a **15.2% improvement in Success Rate** and a **24.7% gain on long-horizon trajectories**, plus gains in real-world tests, but the excerpt does not show the exact table or baseline for those two aggregate claims.

## Link
- [http://arxiv.org/abs/2604.17473v1](http://arxiv.org/abs/2604.17473v1)
