---
source: arxiv
url: https://arxiv.org/abs/2606.07386v1
published_at: '2026-06-05T15:23:54'
authors:
- Mengze Tian
- Yiming Li
- Sichao Liu
- Auke Ijspeert
- Sylvain Calinon
topics:
- robot-imitation-learning
- spline-policy
- action-representation
- vision-language-action
- dexterous-manipulation
- flow-field-control
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Spline Policy: A Structured Representation for Robot Policies

## Summary
Spline Policy changes the action output of robot imitation policies from fixed action chunks to spline parameters, while leaving the policy backbone unchanged. The paper claims this gives the same learned policy a continuous trajectory object that can be resampled, constrained, converted to a local flow field, and used with controllers.

## Problem
- Modern robot imitation policies often output fixed-resolution action chunks, which hide useful motion structure such as continuity, derivatives, boundary conditions, and resampling before execution.
- This matters because robot controllers often need smooth trajectories, correction after tracking errors, and constraint handling at execution time.
- Existing movement primitive and dynamical-system methods expose this structure, but they are not usually plugged into current diffusion, flow-matching, transformer, or VLA-style policy backbones as a simple output replacement.

## Approach
- The policy predicts spline parameters instead of a sequence of discrete actions. The spline decoder maps those parameters to a continuous trajectory at any queried time.
- The main implementation uses piecewise quadratic Bernstein splines, where each segment has 3 control points and can enforce C0 or C1 continuity with linear constraints.
- For quadratic splines, the predicted curve can be converted into a state-dependent flow field by projecting the current state to the closest point on the spline, then combining attraction toward the curve with motion along the curve.
- The same spline parameters support endpoint constraints, zero terminal tangent constraints, convex-hull safety checks for convex sets, derivative constraints through control-point differences, and Gaussian uncertainty propagation through the spline basis.
- The paper attaches this output representation to ACT, Diffusion Policy, Flow Matching Policy, transformer policies, and VLA-style policies by changing the output head, prediction target, and loss, not the backbone.

## Results
- The provided excerpt gives no task success rates, error metrics, dataset sizes, or numeric comparisons against action-chunk baselines.
- The paper claims experiments cover low-dimensional motion learning, simulated manipulation under matched backbones, dexterous manipulation, and real-robot case studies.
- The strongest concrete claim is compatibility across multiple policy families: ACT, diffusion, flow matching, transformer-based policies, and VLA-style models.
- The excerpt states that quadratic spline outputs allow an analytical distance-field construction, and under stated regularity and projection assumptions the induced dynamics do not increase distance to the generated spline.
- The method reduces a dense action sequence to a smaller set of spline parameters, but the excerpt does not provide a compression ratio or runtime number.

## Link
- [https://arxiv.org/abs/2606.07386v1](https://arxiv.org/abs/2606.07386v1)
