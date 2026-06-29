---
source: arxiv
url: https://arxiv.org/abs/2606.06832v1
published_at: '2026-06-05T02:16:50'
authors:
- Abhiroop Ajith
- Constantinos Chamzas
topics:
- visual-task-planning
- symbolic-world-models
- strips-planning
- robot-manipulation
- neuro-symbolic-planning
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# STRIPS-WM: Learning Grounded Propositional STRIPS-style World Models from Images

## Summary
STRIPS-WM learns a propositional STRIPS world model from RGB action transitions, then uses the learned predicates and operators for image-to-plan robot manipulation.

## Problem
- It targets long-horizon visual manipulation where the robot sees images but planning depends on discrete facts such as action applicability and action effects.
- Training data contains only tuples of current image, high-level action ID, and next image. It does not use object labels, poses, masks, hand-written predicates, or symbolic goals.
- This matters because planning by predicting future images can waste capacity on visual detail that does not affect task success.

## Approach
- A student-teacher visual dynamics model maps images into finite scalar quantized codes. Unique codes become abstract task-graph nodes, and observed action transitions become labeled graph edges.
- An inverse dynamics head predicts the action from current and next codes, which pushes the code to keep action-relevant information.
- A CP-SAT solver assigns binary predicate vectors to graph nodes and learns one grounded STRIPS operator per action ID, with positive and negative preconditions plus add/delete effects.
- Missing actions from trusted graph states give negative evidence for preconditions. Slack variables handle abstraction errors and noisy aliases.
- A visual predicate classifier maps new start and goal images to learned predicate vectors, then a classical planner searches in predicate space.

## Results
- The excerpt reports 3 domains: BlocksWorld, DinnerTable, and DinnerTable Real.
- BlocksWorld uses 18 actions and 5,000 image transitions. STRIPS-WM recovers 16 learned graph states for 16 ground-truth states, uses 9 predicates, and has 0 transition slack and 0 applicability slack.
- DinnerTable uses 70 actions and 12,000 image transitions. It recovers 101 learned graph states for 101 ground-truth states, uses 35 predicates, has 0 transition slack, and 9 applicability-slack cases.
- DinnerTable Real uses 64 actions and 3,000 image transitions. It learns 111 graph states, compresses them into 71 learned predicate states matching 71 ground-truth states, uses 35 predicates, has 0 transition slack, and 13 applicability-slack cases.
- The paper claims better image-to-plan success than WM-Rollout, WM-BFS, LSR, and LatPlan-AMA3, but the provided excerpt does not include the success-rate table or exact success numbers.

## Link
- [https://arxiv.org/abs/2606.06832v1](https://arxiv.org/abs/2606.06832v1)
