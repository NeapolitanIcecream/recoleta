---
source: arxiv
url: http://arxiv.org/abs/2603.09298v1
published_at: '2026-03-10T07:28:41'
authors:
- Yuankai Luo
- Woping Chen
- Tong Liang
- Zhenguo Li
topics:
- vision-language-action
- multi-task-learning
- lora-adapters
- robot-policy
- continual-learning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# CORAL: Scalable Multi-Task Robot Learning via LoRA Experts

## Summary
CORAL proposes a parameter-isolated framework for multi-task robot learning: it freezes a pre-trained VLA backbone and adds one lightweight LoRA expert for each task. It aims to simultaneously address negative transfer in multi-task learning, forgetting when continuously adding new tasks, and storage overhead in edge deployment.

## Problem
- During joint fine-tuning for multi-task robotics, gradients from different tasks can conflict with one another, leading to negative transfer, especially when fine-grained language instructions are easily confused.
- If a full model checkpoint is stored for every task, storage and deployment costs grow linearly with the number of tasks, making this unsuitable for real robot systems.
- Sequentially learning new tasks can also overwrite old knowledge and cause catastrophic forgetting, so a solution is needed that can both scale and avoid mutual interference.

## Approach
- Freeze a general pre-trained VLA foundation model and train only a separate LoRA adapter for each task, placing task-specific knowledge into small “experts.”
- LoRA is injected into the attention layers of both the vision-language encoder and the action head, allowing experts to adjust both perception/language features and control policies.
- At inference time, the CORAL Manager determines the task directly from the language instruction and loads the corresponding expert, without requiring a learned gating network or external LLM routing.
- Online switching is implemented by first restoring the clean backbone and then merging the target LoRA weights; after merging, execution follows the original model, so the authors claim there is no additional inference FLOPs or latency overhead.
- Because parameters for different tasks are completely isolated, new tasks can be added sequentially without overwriting old-task parameters, mitigating interference and forgetting by design.

## Results
- **LIBERO (40 tasks)**: CORAL with **SimVLA** achieves an average success rate of **99.3%**, an improvement of **+0.7** over the **SimVLA baseline 98.6%**, and also higher than **X-VLA 98.1%** listed in the paper; on **LIBERO-Long**, it reaches **98.8% vs 96.4%**, an improvement of **+2.4**.
- **LIBERO (same framework, different backbone)**: CORAL with **π0.5** reaches **98.4%**, improving over the **π0.5 baseline 96.9%** by **+1.5**; within this, the **Long** subset is **95.8% vs 92.4%**, an improvement of **+3.4**.
- **WidowX / Simpler-Bridge**: CORAL with **SimVLA** averages **97.9%**, higher than the **SimVLA baseline 95.8%** by **+2.1**; it improves by **+4.1** on the **Stack** and **Eggplant** tasks, and reaches **100%/100%** on **Spoon/Carrot**.
- **Google Robot / Simpler-Fractal**: CORAL with **SimVLA** averages **84.9%**, improving over the **SimVLA baseline 77.0%** by **+7.9**; it is also higher than **X-VLA 75.7%**. By category: **Pick 85.9 (+3.6)**, **Move 92.8 (+11.8)**, **Open 75.9 (+8.2)**.
- **Efficiency and storage**: For a **0.8B** backbone, a single **rank-16 LoRA** expert is about **26MB**; the authors say this is about **100×** smaller than the full model. The expert library for 40 LIBERO tasks is about **1GB**, while a single fully fine-tuned checkpoint is about **3GB**. Expert switching time is about **100ms**, and the paper claims **zero additional inference FLOPs**.
- **Real robot**: The paper claims validation on **Galaxea R1 Lite** for cross-scene generalization, new task acquisition, and resistance to forgetting, but the provided excerpt does not include the full quantitative table for that section, so more specific real-world numbers cannot be listed from the excerpt.

## Link
- [http://arxiv.org/abs/2603.09298v1](http://arxiv.org/abs/2603.09298v1)
