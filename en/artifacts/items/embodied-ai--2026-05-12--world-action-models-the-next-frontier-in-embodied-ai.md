---
source: arxiv
url: https://arxiv.org/abs/2605.12090v1
published_at: '2026-05-12T13:10:52'
authors:
- Siyin Wang
- Junhao Shi
- Zhaoyang Fu
- Xinzhe He
- Feihong Liu
- Chenchen Yang
- Yikang Zhou
- Zhaoye Fei
- Jingjing Gong
- Jinlan Fu
- Mike Zheng Shou
- Xuanjing Huang
- Xipeng Qiu
- Yu-Gang Jiang
topics:
- world-action-models
- embodied-foundation-models
- vision-language-action
- robot-world-models
- generalist-robot-policy
- robot-data-scaling
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# World Action Models: The Next Frontier in Embodied AI

## Summary
This survey defines World Action Models (WAMs) as robot foundation models that predict future observations and actions together. It argues that adding world prediction to VLA policies can improve physical foresight, generalization, and use of video data without action labels.

## Problem
- Standard VLA models train \(p(a \mid o,l)\): they map observation and language directly to actions, without an explicit future-state prediction target.
- This matters in embodied tasks because contact, object motion, and failed actions often need to be anticipated before the robot moves.
- The paper says related terms such as video policies, video action models, world models, and action world models overlap, which makes method comparison hard.

## Approach
- The paper formalizes a WAM objective as \(p(o',a \mid o,l)\), where the model predicts a future observation \(o'\) and an action \(a\) from the current observation \(o\) and language instruction \(l\).
- It defines 2 required properties: forward predictive modeling of future states and action generation tied to the predicted state.
- It splits WAMs into 2 architecture families: Cascaded WAMs and Joint WAMs.
- Cascaded WAMs factorize the task as \(p(o',a \mid o,l)=p(a \mid o',o,l)p(o' \mid o,l)\); Joint WAMs train a shared model for \(p(o',a \mid o,l)\).
- The survey organizes prior work by architecture, training data, and evaluation criteria.

## Results
- The excerpt reports no new robot benchmark result, success rate, or dataset score; the main claimed contribution is a survey and taxonomy.
- It claims 2 main WAM architecture families: Cascaded and Joint.
- It further separates Cascaded WAMs into explicit and implicit representation alignment paths, and Joint WAMs into autoregressive and diffusion-based forms.
- It reviews 4 training data sources for WAMs: robot teleoperation, portable human demonstrations, simulation, and internet-scale egocentric video.
- It groups evaluation into 3 capability areas: visual fidelity, physical commonsense, and action plausibility.
- It contrasts 3 formal objectives: VLA \(p(a \mid o,l)\), world model \(p(o' \mid o,a)\), and WAM \(p(o',a \mid o,l)\).

## Link
- [https://arxiv.org/abs/2605.12090v1](https://arxiv.org/abs/2605.12090v1)
