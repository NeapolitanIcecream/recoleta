---
source: arxiv
url: https://arxiv.org/abs/2605.29562v1
published_at: '2026-05-28T08:14:08'
authors:
- Shengyu Si
- Yuanzhuo Lu
- Ruimeng Yang
- Ziyi Ye
- Zuxuan Wu
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-foundation-model
- procedural-memory
- cross-task-generalization
- lora-adaptation
- manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# VLA-Pro: Cross-Task Procedural Memory Transfer for Vision-Language-Action Models

## Summary
VLA-Pro adds retrievable LoRA procedural memories to VLA policies so they can reuse experience from seen manipulation tasks on unseen tasks. It reports large gains on RoboTwin, RLBench, and real robot tasks with π0.5, RDT, and X-VLA backbones.

## Problem
- VLA robot policies often fail on unseen tasks when objects, scenes, or action patterns differ from training data, even when the new task is close to a seen one.
- Mixed-task fine-tuning can bias the policy toward frequent training behaviors, such as placing objects on a stand when the instruction needs a different spatial relation.
- This matters because generalist robot policies need cross-task transfer without collecting demonstrations or fine-tuning for every new manipulation task.

## Approach
- During training, VLA-Pro first learns a shared base LoRA on all seen tasks, then fine-tunes one task-specific LoRA adapter per seen task.
- Each memory entry pairs that task LoRA with a sequence of structured procedural states: action type, object geometry, end-effector orientation, and target interaction point.
- At inference time, a vision-language model extracts the current procedural state from the image, instruction, and prior interaction history.
- The system retrieves the top-k closest task memories using action-aware matching over the structured fields, then fuses the retrieved LoRA weights with Softmax similarity weights.
- The fused LoRA is loaded for the current action chunk, used to generate actions, then unloaded before the next chunk.

## Results
- On RoboTwin, VLA-Pro raised average success from 17.0% to 30.0% with X-VLA, 11.1% to 34.1% with RDT, and 40.4% to 59.3% with π0.5. The RDT result is the paper's largest reported relative gain, about 207%.
- On the RoboTwin place_bell_behind task, π0.5 improved from 0.0% to 100.0% success.
- On RLBench zero-shot tasks, VLA-Pro with π0.5 had the best average success over the 9 tasks where at least one method succeeded, beating RDT by 10.7 percentage points, AtomicVLA by 6.2 points, and the π0.5 baseline by 7.1 points.
- In real-world tests on a UR7e arm with 6 held-out tasks and 20 trials per task, π0.5 improved from 5.8% to 65.0% average success.
- In the RLBench top-k ablation, k=2 reached 20.9% average success versus 13.8% for the π0.5 baseline, a 51.4% relative gain; k=1 reached 16.9% and k=3 reached 16.4%.

## Link
- [https://arxiv.org/abs/2605.29562v1](https://arxiv.org/abs/2605.29562v1)
