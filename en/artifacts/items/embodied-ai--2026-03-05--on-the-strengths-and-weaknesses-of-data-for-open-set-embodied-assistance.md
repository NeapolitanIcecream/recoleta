---
source: arxiv
url: http://arxiv.org/abs/2603.04819v1
published_at: '2026-03-05T05:10:47'
authors:
- Pradyumna Tambwekar
- Andrew Silva
- Deepak Gopinath
- Jonathan DeCastro
- Xiongyi Cui
- Guy Rosman
topics:
- embodied-assistance
- synthetic-data
- multimodal-learning
- open-set-generalization
- overcooked
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# On the Strengths and Weaknesses of Data for Open-set Embodied Assistance

## Summary
This paper studies a core problem in open-set embodied assistance: whether a multimodal assistant trained only on synthetic interactive data can provide corrective actions or natural-language guidance for **unseen user deficiencies** and **new task configurations**. The paper builds an open-set corrective assistance benchmark in Overcooked and shows that data design, rather than simply model invocation, is crucial for generalization.

## Problem
- The goal is **open-set corrective assistance**: the model must read long-horizon, multimodal user behavior trajectories and generate corrective actions or language feedback **without a fixed list of error categories**.
- This matters because real assistive robots and interactive embodied systems must handle **new users, new error patterns, and new tasks**, while real long-horizon interaction data is expensive, noisy, and difficult to collect.
- Existing methods typically rely on **closed-category correction** or **external planners**, making it hard to test whether a model has truly learned assistive capabilities that generalize across deficiencies and tasks.

## Approach
- In Overcooked, the authors generate long-horizon trajectories using **procedural maps + synthetic users + defect injection**: 5 heuristic user policies, 17 defect types (including no defect), 20% random action probability at each step, and 450 procedurally generated maps.
- The model uses a projection-based multimodal architecture built on **Llama-3 + ViT-base**: images from the full trajectory are encoded into visual tokens, interleaved with action text, and then decoded into textual **coaching-style feedback** or **corrective actions**.
- The training data is divided into two groups: **grounding data**, which teaches the model to understand images, temporal changes, and environment events; and **task-specific data**, which teaches it to analyze defects and provide assistance across three tasks: coaching, corrections, and defect-delineation.
- Coaching text, reasoning traces, and other supervision signals are synthesized with GPT-4o assistance, with self-checking/voting-based filtering to improve label quality and stylistic diversity.
- The core mechanism can be simplified as: **first teach the model to “understand what happened,” then to “judge what went wrong,” and finally to generate “how to correct it,”** and test whether it transfers to unseen errors and new recipe tasks.

## Results
- On **generalization to unseen defects**, the authors' method outperforms the GPT-4o behavior critic baseline. Coaching: Behavior Critic 21.00, Behavior Critic + Summaries 55.70, Ours 1B 76.60, Ours 8B **77.80**.
- On **corrective actions for unseen defects**, Ours 1B **55.70** and Ours 8B 54.60, significantly outperforming Behavior Critic 20.40 and Behavior Critic + Summaries 19.80; this suggests that performance in this setting is already nearing saturation around 1B scale.
- On **generalization to new tasks/new recipes**, model scaling is more important. Coaching: Behavior Critic 34.21, Behavior Critic + Summaries 71.05, Ours 1B 50.88, Ours 8B **85.96**.
- On **corrective actions for new tasks**, Ours 8B **56.67**, outperforming Ours 1B 50.83, Behavior Critic 9.17, and Behavior Critic + Summaries 15.83.
- For data scale and composition, the paper explicitly reports the training set breakdown: Image-QA 55,000, Trajectory-QA 54,000, Video-QA 55,000, Coaching 26,000, Corrections 27,000, Defect-Delineation 20,000; the strongest takeaway is that **diverse and complementary data coverage (grounding, defect understanding, and scenario diversity) is the key to open-set assistive generalization**.

## Link
- [http://arxiv.org/abs/2603.04819v1](http://arxiv.org/abs/2603.04819v1)
