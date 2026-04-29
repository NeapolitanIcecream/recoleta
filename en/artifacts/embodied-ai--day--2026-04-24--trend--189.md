---
kind: trend
trend_doc_id: 189
granularity: day
period_start: '2026-04-24T00:00:00'
period_end: '2026-04-25T00:00:00'
topics:
- robotics
- vision-language-action
- evaluation
- safety
- online-rl
- long-horizon-planning
run_id: materialize-outputs
aliases:
- recoleta-trend-189
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/evaluation
- topic/safety
- topic/online-rl
- topic/long-horizon-planning
language_code: en
pass_output_id: 106
pass_kind: trend_synthesis
---

# Robot learning work centers on deployment-grade adaptation, evaluation, and safety

## Overview
This day’s robotics papers are strongest on execution systems that get closer to real deployment. The emphasis is concrete: fast online adaptation, action-grounded evaluation, physical safety testing, and memory for long tasks. RL Token, dWorldEval, and RedVLA anchor the brief with results on real robots or deployment-style proxies, while the survey paper makes clear that data and benchmark design still limit how well these gains can be compared.

## Clusters

### Sample-efficient adaptation with compact control signals
Real-robot adaptation is getting more targeted. RL Token keeps a pretrained vision-language-action model frozen, exposes a compact state for reinforcement learning, and updates only a small actor-critic online. The payoff is concrete on precision work: up to 3× faster execution on the hardest phase and a screw insertion gain from 20% to 65% after minutes to a few hours of practice. GazeVLA attacks the same data bottleneck from another side. It uses human gaze as an intention signal, pretrains on more than 150M egocentric frames, and reports stronger few-shot transfer with only 10 robot trajectories and 50 human trajectories per task, including 85% success on simple pick-and-place and a reported 2× gain over pi0.5 on screw tightening.

#### Evidence
- [RL Token: Bootstrapping Online RL with Vision-Language-Action Models](../Inbox/2026-04-24--rl-token-bootstrapping-online-rl-with-vision-language-action-models.md): RL Token method and real-robot gains
- [GazeVLA: Learning Human Intention for Robotic Manipulation](../Inbox/2026-04-24--gazevla-learning-human-intention-for-robotic-manipulation.md): GazeVLA intention transfer and few-shot results

### Evaluation infrastructure gets treated as core research
Evaluation is moving closer to deployment constraints. dWorldEval treats policy evaluation as action-conditioned future prediction, with language, images, and robot actions in one token space. Its proxy scores track real execution closely, with correlation around 0.91 to 0.93 across LIBERO, RoboTwin, and real-world tasks. The same paper also reports better action controllability and lower long-horizon drift than prior evaluators. The companion survey on VLA data and benchmarks sharpens why this matters: current benchmarks still struggle to separate task complexity from environment structure, and they leave compositional generalization and long-horizon reasoning under-tested.

#### Evidence
- [dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model](../Inbox/2026-04-24--dworldeval-scalable-robotic-policy-evaluation-via-discrete-diffusion-world-model.md): dWorldEval proxy evaluation metrics and correlation with real execution
- [Vision-Language-Action in Robotics: A Survey of Datasets, Benchmarks, and Data Engines](../Inbox/2026-04-24--vision-language-action-in-robotics-a-survey-of-datasets-benchmarks-and-data-engines.md): Survey evidence on benchmark and data gaps

### Safety work targets scene-level physical failure modes
Safety testing is becoming physical and model-specific. RedVLA keeps the task instruction fixed, adds one risk object to the scene, and then refines its placement to trigger unsafe behavior. Across six VLA models, average attack success runs from 64.9% to 95.5%, with cumulative dangerous item misuse at 100% attack success on all six models. The paper also reports that stronger base policies can be easier to exploit in this setup, and that a lightweight guard trained on RedVLA data cuts online attack success by 59.5% with small task cost. This makes safety evaluation look less like prompt filtering and more like adversarial scene design around actual robot motion.

#### Evidence
- [RedVLA: Physical Red Teaming for Vision-Language-Action Models](../Inbox/2026-04-24--redvla-physical-red-teaming-for-vision-language-action-models.md): Physical red teaming setup, vulnerability rates, and guard results

### Long-horizon VLAs add persistent state and planner logic
Long-horizon robot control is getting more explicit memory and task structure. CodeGraphVLP builds a persistent semantic graph, calls an LLM once to write a task-specific planner, and then feeds the executor VLA masked views of only the relevant objects. On three real-world tabletop tasks it reports 81.7% average success, ahead of Gr00T N1.5 + Multi-frame at 56.7% and π0 at 30.0%. The mechanism is clear: earlier observations stay available as graph state, progress checks live in code, and the acting policy sees less clutter at each step.

#### Evidence
- [CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models](../Inbox/2026-04-24--codegraphvlp-code-as-planner-meets-semantic-graph-state-for-non-markovian-vision-language-action-models.md): Semantic graph planner design and real-world task results
