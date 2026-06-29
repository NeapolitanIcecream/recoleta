---
source: arxiv
url: https://arxiv.org/abs/2605.17268v1
published_at: '2026-05-17T05:29:48'
authors:
- Nicanor Mayumu
- Xiaoheng Deng
- Patrick Mukala
topics:
- vision-language-action
- autonomous-driving
- reasoning-faithfulness
- safety-evaluation
- counterfactual-testing
- trajectory-prediction
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation

## Summary
The paper tests whether Chain-of-Causation explanations from a VLA autonomous-driving model match the scene and the generated trajectory. It finds that these explanations often fail as safety evidence.

## Problem
- VLA driving models can output natural-language reasoning and a planned trajectory, but the text may disagree with the objects in the scene or the action taken.
- This matters because a trace such as “stop for the pedestrian” can mislead users or safety monitors when the model misses the pedestrian or keeps moving.
- The paper focuses on Alpamayo-R1-10B and asks whether its reasoning is faithful enough for driving safety checks.

## Approach
- The study evaluates 300 Alpamayo-R1-10B inferences: 100 PhysicalAI-AV test clips with 3 random seeds per clip.
- It defines entity fidelity by comparing objects mentioned in the Chain-of-Causation text with autolabeled 3D obstacles near the prediction time.
- It defines action fidelity by checking whether stated actions match trajectory predicates, such as final speed under 0.5 m/s for “stop,” deceleration over 1.0 m/s² for “decelerate,” and lateral shift over 1.0 m for turning.
- It tests counterfactual faithfulness with front-camera Gaussian blur at σ=3 plus 10% rectangular occlusion, then checks whether reasoning and trajectory change together.
- It estimates trajectory uncertainty by sampling 2 diffusion trajectories and measuring spatial spread.

## Results
- Overall reasoning fidelity is 42.5% on 282 inferences with obstacle context; entity fidelity is 35.3%, and action fidelity is 49.6%.
- The model has an 8.9% hallucination rate, with 25 hallucinated entity instances, and misses 94 pedestrians in 33.3% of pedestrian-relevant scenes.
- Baseline trajectory quality over 300 inferences has mean minADE 1.992 ± 1.752 m, median minADE 1.481 m, 90th percentile 4.018 m, 95th percentile 5.884 m, and 21/300 safety failures above 5 m error.
- Reasoning-action consistency averages 0.483; 53.3% of inferences have low consistency, and 37.9% of claimed stop cases continue instead.
- Under visual perturbation, 97.7% of trajectories change; 38/265 cases, or 14.3%, are silent failures where the trajectory changes but the reasoning stays the same.
- High-fidelity inferences have mean ADE 1.694 m versus 2.278 m for low-fidelity inferences, a 34.5% higher error for the low-fidelity group.

## Link
- [https://arxiv.org/abs/2605.17268v1](https://arxiv.org/abs/2605.17268v1)
