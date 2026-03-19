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
- embodied-ai
- synthetic-data
- open-set-assistance
- multimodal-learning
- robotics
- overcooked
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# On the Strengths and Weaknesses of Data for Open-set Embodied Assistance

## Summary
This paper studies the question of **how data should be constructed** for open-set embodied assistance: using only synthetic interaction data, can a model understand long-horizon user behavior and provide either corrective actions or textual guidance for previously unseen deficiencies or new tasks? The authors build multimodal synthetic data in Overcooked and fine-tune a Llama-based model, finding that carefully designed data can significantly improve open-set assistance generalization, though task generalization remains more difficult.

## Problem
- Existing assistive embodied models typically assume **closed corrective categories** or rely on **external planners**, making them poorly suited to real-world settings with open-ended, diverse, and non-predefined user errors.
- Long-horizon, multimodal human-machine interaction data is expensive and noisy, making it difficult to systematically evaluate whether models can generalize to **unseen behavioral deficiencies** and **new task configurations**.
- This matters because interactive systems such as robots and autonomous driving platforms cannot be deployed safely and effectively if they fail to provide reliable assistance for new users and new tasks.

## Approach
- Define **Open-Set Corrective Assistance**: the model reads a user’s multimodal trajectory (image states + action text) and generates one of two kinds of assistance: a **corrective action** or **natural-language feedback**, without being restricted to a fixed label set.
- Generate data with synthetic users in Overcooked: design **5** heuristic policies, **17** deficiency types (including no defect), and **450** procedurally generated maps, and add **20%** random action noise during rollout to create a rich, hierarchical behavior distribution.
- Build two broad categories of training data: grounding data (Image-QA **55k**, Trajectory-QA **54k**, Video-QA **55k**) to improve spatial/temporal understanding, and task data (Coaching **26k**, Corrections **27k**, Defect-Delineation **20k**).
- The model uses a projection-based multimodal architecture with **Llama-3 + ViT-base**: encoded image trajectories are interleaved with action text as input, and the model uniformly decodes text outputs for either feedback or actions.
- Corrective actions are generated from the heuristic next action after removing the defect, while textual feedback and reasoning traces are synthesized by **GPT-4o** to distill assistive capability and behavior analysis ability.

## Results
- For **unseen-defect generalization**, the authors’ **8B** model achieves the best coaching score: **77.80**, outperforming Behavior Critic (**21.00**) and Behavior Critic + Summaries (**55.70**).
- For **corrective actions on unseen defects**, the authors’ **1B** model performs best at **55.70**, exceeding Behavior Critic (**20.40**) and Behavior Critic + Summaries (**19.80**); the **8B** model reaches **54.60**, close to 1B, suggesting this capability is already near saturation around the **1B** scale.
- For **new-task/new-recipe generalization**, the authors’ **8B** model leads by a large margin: coaching **85.96**, above Behavior Critic (**34.21**) and Behavior Critic + Summaries (**71.05**).
- For **corrective actions on new tasks**, the authors’ **8B** model reaches **56.67**, outperforming the **1B** model’s **50.83**, Behavior Critic’s **9.17**, and +Summaries’ **15.83**; this indicates that task generalization depends more on stronger multimodal grounding and larger model scale.
- The authors’ core conclusion is that effective open-set assistance requires data covering **multimodal grounding, defect inference, and scene diversity**; even so, generalization over open-ended task compositions remains difficult.

## Link
- [http://arxiv.org/abs/2603.04819v1](http://arxiv.org/abs/2603.04819v1)
