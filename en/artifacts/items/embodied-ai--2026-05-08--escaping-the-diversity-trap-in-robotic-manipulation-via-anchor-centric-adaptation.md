---
source: arxiv
url: https://arxiv.org/abs/2605.07381v1
published_at: '2026-05-08T07:35:24'
authors:
- Yanzhe Chen
- Kevin Yuchen Ma
- Qi Lv
- Yiqi Lin
- Zechen Bai
- Chen Gao
- Mike Zheng Shou
topics:
- vision-language-action
- robot-adaptation
- data-efficient-learning
- real-robot-manipulation
- active-data-collection
- low-rank-adaptation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Escaping the Diversity Trap in Robotic Manipulation via Anchor-Centric Adaptation

## Summary
ACA improves low-budget real-robot VLA adaptation by repeating demonstrations at selected anchor conditions before adding targeted boundary data.

## Problem
- Real-robot demonstrations are costly, so adapting a pretrained VLA to a new robot often has only tens to hundreds of trajectories.
- The paper argues that collecting one demonstration for many different conditions can fail under small budgets because each condition has too little data, which leaves high action-estimation noise.
- This matters for robot deployment because sparse coverage can make policies unstable in physical tasks with embodiment mismatch and workspace variation.

## Approach
- The paper models adaptation as learning a conditional action vector field and splits error into an estimation term and a coverage term.
- With N trajectories and K unique conditions, the simplified bound is Cσ√(K/N) + LcK^(-1/d), so adding more unique conditions reduces coverage error but raises estimation error.
- ACA first trains on repeated demonstrations at a small set of workspace anchors to make a stable base policy.
- It then runs teacher-forced deviation scoring on probe demonstrations, selects the highest-error boundary conditions, and collects local boundary data.
- Stage 2 freezes the Stage-1 policy and trains a LoRA residual branch in the Action Expert, so boundary corrections are added without full-parameter drift.

## Results
- On a 7-DoF Franka Panda with 4 tabletop tasks, ACA is evaluated on Block Stacking, Cup Placement, Table Cleaning, and Toy Tidying across S@1, S@2, and S@3 regions.
- With N=50 trajectories, π0.5 + ACA reaches 46.3% mean success versus 13.8% for π0.5, a +32.5 point gain.
- With N=100 trajectories, π0.5 + ACA reaches 72.5% mean success versus 31.7%, a +40.8 point gain.
- With N=150 trajectories, π0.5 + ACA reaches 83.8% mean success versus 52.9%, a +30.9 point gain.
- The paper reports 20 evaluation rollouts per task-region setting; S@1 covers 25% of the workspace, S@2 covers 50%, and S@3 covers 90%.

## Link
- [https://arxiv.org/abs/2605.07381v1](https://arxiv.org/abs/2605.07381v1)
