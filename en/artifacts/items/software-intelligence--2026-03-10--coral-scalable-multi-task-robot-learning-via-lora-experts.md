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
- robot-learning
- vision-language-action
- lora
- multi-task-learning
- continual-learning
relevance_score: 0.42
run_id: materialize-outputs
language_code: en
---

# CORAL: Scalable Multi-Task Robot Learning via LoRA Experts

## Summary
CORAL proposes a scalable solution for multi-task robot learning: it freezes a pre-trained VLA backbone and assigns an independent LoRA expert to each task. It aims to reduce multi-task gradient conflicts, support continual incremental expansion, and improve task success rates in real-world and simulated environments with very small storage requirements and almost no additional inference overhead.

## Problem
- In multi-task robot fine-tuning, gradients from different tasks can conflict with each other, leading to negative transfer, and a single shared model often sacrifices single-task performance.
- Although storing a full model for each task can avoid interference, storage and deployment costs grow linearly with the number of tasks, making it unsuitable for edge robots.
- When new tasks are added sequentially, standard fine-tuning can also overwrite old knowledge and cause catastrophic forgetting, so a continual learning mechanism is needed that is both scalable and low-overhead.

## Approach
- Freeze a pre-trained Vision-Language-Action backbone model and train only task-specific LoRA adapters, separating general capabilities from task-specialized capabilities.
- Each task corresponds to an independent LoRA expert; during training, only that expert’s parameters are updated, with no trainable parameters shared with other tasks, thereby structurally avoiding parameter-level task interference.
- LoRA is injected into the attention layers of both the vision-language encoder and the action head, allowing experts to adjust both perception/instruction understanding and low-level control policies.
- At inference time, the CORAL Manager directly determines the task from the language instruction and loads the corresponding expert, without needing a learned gating network; by merging LoRA weights into the backbone, it achieves zero additional inference FLOPs.
- This design naturally supports continual expansion: adding a new task only requires introducing a new lightweight LoRA expert, without retraining or overwriting parameters for old tasks.

## Results
- On the LIBERO 40-task benchmark, CORAL with the SimVLA backbone achieves an average success rate of **99.3%**, improving over the SimVLA baseline of **98.6%** by **+0.7** percentage points and surpassing X-VLA’s **98.1%**; on LIBERO-Long, it increases from **96.4%** to **98.8%**, an improvement of **+2.4**.
- On the same LIBERO benchmark, CORAL with the \(\pi_{0.5}\) backbone reaches **98.4%**, improving over the \(\pi_{0.5}\) baseline of **96.9%** by **+1.5**; on the hardest LIBERO-Long split, it improves from **92.4%** to **95.8%**, a gain of **+3.4**.
- On WidowX tasks, CORAL_SimVLA achieves an average success rate of **97.9%**, higher than the SimVLA baseline of **95.8%**, for an improvement of **+2.1**; among individual tasks, Stack and Eggplant improve by **+4.1** to **95.8%**, while Spoon and Carrot both reach **100.0%**.
- On Google Robot tasks, CORAL_SimVLA reaches an average of **84.9%**, improving over the SimVLA baseline of **77.0%** by **+7.9**, and also outperforming X-VLA’s **75.7%** and RT-2-X’s **65.6%**; the Move subtask improves from **81.0%** to **92.8%** (**+11.8**), and Open improves from **67.7%** to **75.9%** (**+8.2**).
- In terms of efficiency, on a typical **0.8B**-parameter VLA model, a rank-16 expert is only about **26 MB**, roughly a **100×** compression relative to the full model; the total storage for **40** experts on LIBERO is about **1 GB**, while a single fully fine-tuned checkpoint is about **3 GB**.
- For deployment, expert switching can be completed within **100 ms** on a single GPU, and is claimed to incur **zero additional inference FLOPs/latency**; on LIBERO, each task’s LoRA is trained for only **50 steps**, highlighting its lightweight adaptation characteristics.

## Link
- [http://arxiv.org/abs/2603.09298v1](http://arxiv.org/abs/2603.09298v1)
