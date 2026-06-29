---
source: arxiv
url: http://arxiv.org/abs/2604.21924v1
published_at: '2026-04-23T17:59:04'
authors:
- Isabella Liu
- An-Chieh Cheng
- Rui Yan
- Geng Chen
- Ri-Zhao Qiu
- Xueyan Zou
- Sha Yi
- Hongxu Yin
- Xiaolong Wang
- Sifei Liu
topics:
- vision-language-action
- long-horizon-planning
- robot-manipulation
- hierarchical-policy
- trace-conditioning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Long-Horizon Manipulation via Trace-Conditioned VLA Planning

## Summary
LoHo-Manip is a hierarchical long-horizon manipulation system that pairs a task-management vision-language model with a short-horizon VLA executor. Its main idea is to replan from the current observation at each step and guide the executor with a predicted 2D visual trace.

## Problem
- Long-horizon robot manipulation is hard because tasks unfold over many dependent steps, the next action depends on task progress, and small execution errors compound over time.
- Monolithic VLA policies struggle to both plan and control across long sequences, and they are hard to swap across robot embodiments or action spaces.
- This matters for real robot tasks such as refill, cook, or organize, where success depends on progress tracking, recovery after failed steps, and handling new objects or scenes.

## Approach
- The paper splits the system into two modules: a task manager and an executor. The manager predicts what remains to be done, and the executor handles short-horizon motor control.
- At each step, the manager takes the current image, the instruction, and a compact text memory of completed subtasks, then outputs a progress-aware remaining plan plus a 2D keypoint trace for where to move or what to approach next.
- The executor VLA is fine-tuned to condition on the rendered trace, so long-horizon planning becomes repeated local control by following the trace.
- The manager runs in a receding-horizon closed loop. If an earlier subtask failed, it still appears in the next remaining plan, and the trace updates, which gives implicit replanning and recovery without hand-written recovery rules.
- Training uses Bridge robot demonstrations for subtask and trace supervision, plus RoboVQA and EgoPlan-BenchIT for planning and reasoning data, with synthetic failure-recovery examples added for robustness.

## Results
- On RoboVQA, LoHo-Manip-4B reaches 63.1 average, beating RynnBrain-8B at 62.1, Fast-ThinkAct-3B at 60.8, ThinkAct-7B at 59.8, and Qwen3-VL-8B at 60.8.
- On EgoPlan2, LoHo-Manip-4B gets 56.7 average, above Gemini-3.0-Flash at 48.8, ThinkAct-7B at 48.2, Fast-ThinkAct-3B at 46.4, and RoboBrain2.0-3B at 41.8.
- On trajectory prediction, LoHo-Manip-4B posts the best numbers on ShareRobot-T: DFD 0.2309, HD 0.2058, RMSE 0.1559, improving over Qwen3-VL-4B at 0.3808, 0.3294, 0.2204 and Embodied-R1-3B at 0.3426, 0.3002, 0.2388.
- On VABench-V, LoHo-Manip-4B also leads with DFD 0.2123, HD 0.1821, RMSE 0.1469, compared with Qwen3-VL-4B at 0.2792, 0.2528, 0.2037 and Embodied-R1-3B at 0.3028, 0.2588, 0.2129.
- On EmbodiedBench EB-Alfred, LoHo-Manip-4B reaches 0.38 average versus Qwen3-VL-4B at 0.19 and GPT-4o mini at 0.24. On EB-Habitat, it reaches 0.38 versus Qwen3-VL-4B at 0.30 and GPT-4o mini at 0.33.
- The excerpt claims strong end-to-end gains in simulation and on a real Franka robot, plus better robustness and out-of-distribution generalization, but the provided text does not include the full closed-loop manipulation tables for LIBERO or VLABench.

## Link
- [http://arxiv.org/abs/2604.21924v1](http://arxiv.org/abs/2604.21924v1)
