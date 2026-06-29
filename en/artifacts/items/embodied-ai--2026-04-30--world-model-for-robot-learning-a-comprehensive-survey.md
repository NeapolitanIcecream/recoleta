---
source: arxiv
url: https://arxiv.org/abs/2605.00080v1
published_at: '2026-04-30T14:35:31'
authors:
- Bohan Hou
- Gen Li
- Jindou Jia
- Tuo An
- Xinying Guo
- Sicong Leng
- Haoran Geng
- Yanjie Ze
- Tatsuya Harada
- Philip Torr
- Oier Mees
- Marc Pollefeys
- Zhuang Liu
- Jiajun Wu
- Pieter Abbeel
- Jitendra Malik
- Yilun Du
- Jianfei Yang
topics:
- world-models
- robot-learning
- vision-language-action
- video-generation
- learned-simulators
- policy-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# World Model for Robot Learning: A Comprehensive Survey

## Summary
This survey organizes world models for robot learning around one claim: robots need action-conditioned prediction to plan, train, evaluate, and improve policies in physical tasks.

## Problem
- Robot policies such as RT-2, OpenVLA, and π0 can map vision and language to actions, but the excerpt says reactive VLA policies still struggle with long-horizon reasoning, temporal credit assignment, and compounding errors.
- The literature on robot world models is split across policy learning, learned simulation, video generation, navigation, autonomous driving, datasets, and benchmarks, which makes comparison difficult.
- The problem matters because manipulation, navigation, and driving require predictions about contact, motion, and action consequences before the robot acts.

## Approach
- The survey defines a robot world model as a predictive model of agent-environment dynamics: given a current state or observation, action sequence, and optional language goal, it predicts future states or observations.
- It treats video generation models as a common visual form of world model, especially when they are conditioned on robot actions or language instructions.
- It connects policy models, passive world models, controllable world models, and inverse dynamics models as different conditional queries over a shared predictive-control distribution.
- It reviews three main uses: world models coupled with robot policies, world models used as learned simulators, and robotic video world models for controllable future generation and data generation.
- It covers broader embodied domains, including navigation and autonomous driving, and summarizes datasets, benchmarks, and evaluation protocols.

## Results
- The excerpt provides no new quantitative experimental result, benchmark score, or claimed performance gain; this is a survey paper rather than a method paper.
- It gives a formal state-transition view of world models in Eq. 1: p(x_{t+1:t+H} | x_t, a_{t:t+H-1}, l), where H is the prediction horizon.
- It defines embodied video world models in Eq. 2: p(v_{t+1:t+H} | o_t, a_{t:t+H-1}, l), placing future visual prediction inside action-conditioned robot learning.
- It states 3 core capabilities for actionable world models: foresight, imagination-driven planning, and data amplification.
- It structures the survey into 8 sections, with Section 3 on world models for policy, Section 4 on world models as simulators, Section 5 on robotic video world models, Section 6 on navigation and autonomous driving, and Section 7 on benchmarks, datasets, and results.
- The visible taxonomy table lists at least 10 IDM-style methods and 8 single-backbone methods, showing the shift from decoupled video-rollout pipelines toward tighter policy-world-model coupling.

## Link
- [https://arxiv.org/abs/2605.00080v1](https://arxiv.org/abs/2605.00080v1)
