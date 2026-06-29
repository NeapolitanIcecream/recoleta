---
source: arxiv
url: http://arxiv.org/abs/2604.17800v1
published_at: '2026-04-20T04:46:20'
authors:
- Tuan Van Vo
- Tan Q. Nguyen
- Khang Nguyen
- Nhat Xuan Tran
- Duy H. M. Nguyen
- An T. Le
- Ngo Anh Vien
- Minh Nhat Vu
topics:
- vision-language-action
- generalist-robot-policy
- multimodal-reasoning
- teacher-guided-finetuning
- sim2real
- robot-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning

## Summary
ReFineVLA adds teacher-generated natural-language rationales to vision-language-action policy fine-tuning so the robot model learns both actions and the stated reasons behind them. The paper claims this improves generalization and task success on simulated manipulation benchmarks across Google Robot and WidowX setups.

## Problem
- Standard VLA policies usually learn a direct mapping from images and instructions to actions, with no explicit step-by-step reasoning.
- This can hurt interpretability and generalization on long-horizon, compositional, or out-of-distribution manipulation tasks where the robot must account for object relations, task context, and action sequence.
- The paper argues this matters for generalist robot policies because cross-environment and cross-embodiment success depends on more than reactive action prediction.

## Approach
- The method augments robot demonstrations with teacher-written rationales. For each observation-action pair, an expert teacher model such as Gemini generates text that explains observation, situation analysis, spatial reasoning, and task planning.
- It fine-tunes a pretrained VLA backbone on a reasoning-enriched dataset of about 125,000 trajectories built from BridgeData-v2 and Google RT-1 robot data.
- Training uses a joint loss: standard action prediction loss plus a reasoning generation loss weighted by a tuning coefficient, so the model learns to predict actions and generate rationales together.
- To keep the base model's pretrained skills, it freezes most parameters and updates later transformer blocks and the policy head instead of full-model fine-tuning.
- The instantiated model starts from SpatialVLA, a 3.5B-parameter VLA based on PaliGemma 2 and pretrained on Open X-Embodiment and RHT20.

## Results
- On SimplerEnv benchmarks, the paper claims state-of-the-art performance across Google Robot and WidowX tasks.
- On WidowX, ReFineVLA reaches **47.7%** average task success, with a **5.0 percentage point** gain over the second-best method.
- In more diverse settings, it reports **68.8%** success in **variant aggregation**, a **3.5 point** gain, and **76.6%** success in **visual matching**, a **2.3 point** gain.
- On harder individual tasks, it reports a **9.6 point** improvement on **Move Near** and an **8.2 point** improvement on **Open/Close Drawer**.
- The excerpt also reports attention-map analysis: after reasoning-aware fine-tuning, the model attends more to semantically relevant objects and spatial anchors than action-only baselines.
- The provided text does not include the full result tables, dataset-by-dataset breakdowns, or variance measures, so the quantitative evidence available here is limited to the headline benchmark gains above.

## Link
- [http://arxiv.org/abs/2604.17800v1](http://arxiv.org/abs/2604.17800v1)
