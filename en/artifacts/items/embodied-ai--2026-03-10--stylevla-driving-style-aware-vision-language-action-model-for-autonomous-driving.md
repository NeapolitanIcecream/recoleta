---
source: arxiv
url: http://arxiv.org/abs/2603.09482v1
published_at: '2026-03-10T10:33:58'
authors:
- Yuan Gao
- Dengyuan Hua
- Mattia Piccinini
- "Finn Rasmus Sch\xE4fer"
- Korbinian Moller
- Lin Li
- Johannes Betz
topics:
- vision-language-action
- autonomous-driving
- style-conditioned-policy
- physics-informed-learning
- trajectory-generation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# StyleVLA: Driving Style-Aware Vision Language Action Model for Autonomous Driving

## Summary
This paper proposes StyleVLA, a driving style-aware vision-language-action model for autonomous driving, and simultaneously constructs a dataset annotated with five driving styles. The core conclusion is that by fine-tuning a lightweight 4B multimodal model with physics-constrained supervision, it can outperform general closed-source large models in style consistency and trajectory feasibility.

## Problem
- Existing autonomous-driving VLA/VLM models usually learn only a single driving policy, making it difficult to generate trajectories in different styles such as comfort, sporty, or safety according to user requirements.
- Although public autonomous-driving datasets contain rich perception information, they lack explicit multi-style trajectory supervision, resulting in an insufficient training foundation for “controllable personalized driving.”
- Many methods treat trajectories as discrete token prediction without explicit vehicle kinematic constraints, which can easily produce outputs that are not physically feasible enough.

## Approach
- Construct the **StyleVLA dataset**: based on the CommonRoad + Frenetix motion planner, generate five-style trajectories from **1,484** scenarios, and after statistical filtering obtain **1,216** scenarios, **76,030** BEV samples, and **42,084** FPV samples.
- The five styles are **Default / Balanced / Comfort / Sporty / Safety**; by adjusting weights in the planning cost function for speed, jerk, obstacle distance, visibility, and other factors, different style “ground-truth” trajectories are generated.
- Reformulate the task as multimodal instruction learning: input images, historical ego states, target points, and style instructions, and output structured trajectory JSON for the next **3s or 5s**.
- Use **Qwen3-VL-4B** as the backbone, apply **QLoRA 4-bit** fine-tuning, and add an **MLP regression head** on top of the standard cross-entropy loss to directly regress continuous trajectory states, reducing quantization error introduced by discrete tokens.
- Further add a **physics-informed kinematic consistency loss (PIKC)**, which uses simple kinematic equations to constrain the relationships among position, velocity, heading, and acceleration at adjacent time steps, improving physical consistency and executability.

## Results
- Style statistics after dataset filtering show clear differences: **Sporty** has the highest average speed at **7.32 m/s** and the longest path at **25.13 m**; **Safety** has the lowest average speed at **6.39 m/s** and the shortest path at **21.44 m**; **Comfort** has the lowest RMS jerk at **0.727 m/s^3**.
- BEV ablation experiments show that more data is better: from **4.5k** to **50k** training samples, **ADE 2.08→1.17 m**, **FDE 5.43→3.06 m**, **PSR 20.60%→33.19%**, and **Heading MAE 0.073→0.035 rad**.
- Loss-function ablation shows that physical supervision is effective: on **50k** data, going from **CE** to **CE+REG** changes **FDE 3.82→3.17 m** and **PSR 29.00%→32.08%**; after further adding **PIKC**, performance reaches **ADE 1.17 m, FDE 3.06 m, PSR 33.19%, Heading MAE 0.035 rad**, better than **ADE 1.47 m, FDE 3.82 m, PSR 29.00%, 0.043 rad** with only CE.
- The paper states that base open-source models achieve **0% success** in the zero-shot setting, indicating that general pre-trained models do not naturally possess driving physics and style-control capabilities.
- In the BEV benchmark, the fine-tuned **Qwen3-VL-4B** reaches a success rate of **39.47%**, significantly higher than the best closed-source baseline at **16.38%**; meanwhile, inference time is about **1.92 s**, whereas some proprietary models require **70 s+** for a single inference.
- In the composite style-driving score reported at the beginning of the paper, **StyleVLA** achieves **0.55 (BEV)** and **0.51 (FPV)**, higher than **Gemini-3-Pro** at **0.32** and **0.35**, showing that a specialized, lightweight, physics-constrained model can outperform closed-source general models on tasks in this domain.

## Link
- [http://arxiv.org/abs/2603.09482v1](http://arxiv.org/abs/2603.09482v1)
