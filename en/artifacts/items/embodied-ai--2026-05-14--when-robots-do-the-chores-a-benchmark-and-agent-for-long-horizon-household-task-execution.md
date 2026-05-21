---
source: arxiv
url: https://arxiv.org/abs/2605.14504v1
published_at: '2026-05-14T07:47:53'
authors:
- Zilin Zhu
- Longteng Guo
- Yanghong Mei
- Bowen Pang
- Zongxun Zhang
- Xingjian He
- Ruyi Ji
- Jing Liu
topics:
- long-horizon-planning
- embodied-ai-benchmark
- household-robots
- vision-language-agents
- multimodal-memory
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution

## Summary
LongAct is a benchmark for free-form, long-horizon household task execution, and HoloMind is a VLM-based agent for it. The paper tests planning, memory, and error recovery over tasks that can exceed 2,000 agent steps.

## Problem
- Existing embodied AI benchmarks mostly test short navigation or manipulation tasks, so they miss multi-stage household routines with dependencies across rooms and objects.
- LongAct matters because users can ask for compound chores like desk setup or kitchen reset, which require state tracking, object disambiguation, and replanning over long action sequences.

## Approach
- LongAct uses 300 episodes in 100+ ProcTHOR/AI2-THOR houses across four household scenarios. Each task has free-form instructions, about 9 goals on average, RGB-D plus semantic segmentation, ALFRED-style actions, and a 16,000-step cap.
- It evaluates Success Rate, Goal-Condition Success, step count, and Improvement Rate, a metric based on whether scoring efficiency rises during execution.
- HoloMind decomposes a task into a DAG of dependent goals, then refines each goal with memory before generating executable subgoals.
- It maintains a multimodal spatial memory with 3D semantic maps, object records, CLIP-based retrieval, and VLM verification; episodic memory stores status, completed subgoals, and reusable rules.
- A Critic monitors planner and executor outputs and issues Pass, Refine, or Replan commands when it detects errors.

## Results
- On the LongAct detailed split, pure Qwen3-VL-8B reaches 0.74% Goal-Condition Success (GC) and 0% Success Rate (SR); pure Qwen3-VL-32B reaches 6.14% GC and 0% SR.
- With HoloMind, Qwen3-VL-8B rises to 24.5% GC and 3.00% SR, while Qwen3-VL-32B rises to 51.2% GC and 15.0% SR.
- HoloMind with GPT-5 reports the best model result in the excerpt: 59.0% GC, 16.0% SR in the table, 1,982 navigation steps, 25.3 manipulation steps, and 1.70 Improvement Rate (IR).
- Human performance is reported as 93% goal completion, compared with 59.0% for GPT-5.
- Pure VLM baselines have negative IR (Qwen3-VL-8B: -0.08; Qwen3-VL-32B: -0.32), while HoloMind variants have positive IR (Qwen3-VL-2B: 0.59; Qwen3-VL-8B: 0.99; Qwen3-VL-32B: 1.61; GPT-5: 1.70).
- The excerpt says removing the Critic reduces accuracy by about 40% and can reduce manipulation efficiency and IR by up to 90%, but the shown table does not include those ablation rows.

## Link
- [https://arxiv.org/abs/2605.14504v1](https://arxiv.org/abs/2605.14504v1)
