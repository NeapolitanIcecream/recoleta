---
source: arxiv
url: https://arxiv.org/abs/2606.12299v1
published_at: '2026-06-10T16:34:49'
authors:
- Hyun Joe Jeong
- Gokul Swamy
- Andrea Bajcsy
topics:
- vision-language-action
- robot-policy-steering
- language-feedback
- conformal-prediction
- robot-data-scaling
- closed-loop-control
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering

## Summary
The paper trains a language feedback policy that steers a frozen VLA model by changing the language it receives at each replanning step. It claims large success-rate gains while using a conformal prediction gate to avoid steering when the learned feedback is likely to hurt.

## Problem
- VLA models can react very differently to instructions that mean nearly the same thing, so users and zero-shot language models cannot reliably pick prompts that make the robot finish the task.
- Some tasks cannot be improved through language because the base VLA may ignore the language or lack the needed low-level behavior.
- This matters because a bad steering prompt can reduce task success compared with giving the original instruction.

## Approach
- The method keeps the VLA frozen and changes only the language input sent to it during closed-loop execution.
- It captions robot behavior videos with a VLM, then fine-tunes Qwen3-VL-4B-Instruct as a language feedback policy that proposes task-relevant subtask instructions.
- It uses GPT-5.4 to create 16 trajectory-level language perturbations around each proposed sequence, runs the frozen VLA with those sequences, and estimates which sequences improve success over the original task instruction.
- It rejection-fine-tunes the language feedback policy on the best positive-improvement sequences.
- It trains an improvement head to predict when steering will help, then calibrates a threshold with class-conditional conformal prediction so the policy abstains and falls back to the original instruction when predicted benefit is too low.

## Results
- On seen environments, the conformalized language feedback policy improves base VLA performance by 24.7% in simulation and 65.0% on Franka hardware, according to the abstract.
- The simulation setup uses pi0.5-LIBERO on LIBERO-OOD, including LIBERO-10-style long-horizon tasks, 5 semantic perturbations per visual environment, and 200 visual-semantic evaluation combinations.
- The hardware setup uses pi0.5-DROID zero-shot on a Franka robot, with 4 training tasks, visual and semantic perturbations, and 2 unseen tasks for zero-shot LFP generalization.
- Training uses 50 robot videos per task for narration and 16 language-sequence perturbations per interactive search seed.
- The conformal gate gives the stated false-positive guarantee P(steer | steering harms) <= alpha under exchangeability between calibration and test data.
- The paper claims closed-loop language feedback produces recovery behaviors that open-loop prompt rephrasing did not show, but the excerpt does not provide the exact success-rate numbers for that comparison.

## Link
- [https://arxiv.org/abs/2606.12299v1](https://arxiv.org/abs/2606.12299v1)
