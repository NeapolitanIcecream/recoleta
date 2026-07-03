---
source: arxiv
url: https://arxiv.org/abs/2607.01088v1
published_at: '2026-07-01T15:45:08'
authors:
- Wenqi Jiang
- Jason Clemons
- Rowland O'Flaherty
- Hugo Hadfield
- Alperen Degirmenci
- Shuran Song
- Yashraj Narang
- Christos Kozyrakis
topics:
- robot-foundation-model
- robot-serving
- gpu-scheduling
- multi-robot-systems
- vision-language-action
- factory-automation
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ROSA: A Robotics Foundation Model Serving System for Robot Factories

## Summary
Rosa is a serving system for robotics foundation models in robot factories. It routes many robots' model requests to a shared GPU pool and schedules them to maximize SLO-qualified action throughput.

## Problem
- Robot deployments often assign one onboard accelerator or one dedicated GPU server to each robot, which wastes GPU time while robots execute physical actions and leaves little room for request batching.
- Factory robots need more than a single action model: tasks may call a System 1 action model, a System 2 planner, a safety model, and a task monitor, each with its own latency and call-rate target.
- The paper argues that factory serving should optimize weighted robot action rate under SLOs because lower per-request latency only helps when it changes task progress or safety.

## Approach
- Rosa uses a shared pool of server GPUs for a robot fleet, while robot-side compute keeps high-frequency control and local safety fallback on the robot.
- A declarative task file specifies the robot fleet, model components, prompts, SLOs, model call rates, retry rules, and fallback actions such as stop, resend, replan, or call a human.
- The scheduler uses profiling data, heuristics, and integer linear programming to choose model placement, request routing, batching settings, and per-task action rates.
- The implementation runs on Ray Serve and can call vLLM, PyTorch, and JAX backends for models such as GR00T-N1.6-3B and Qwen2.5-VL variants.

## Results
- On 8 NVIDIA H200 GPUs with up to 64 virtual robots, Rosa improves SLO-qualified factory productivity by up to 12.06x over dedicated serving baselines that allocate one GPU per robot or one GPU per model per robot.
- Against shared-server baselines using the same serving infrastructure without the Rosa scheduler, Rosa improves SLO-qualified factory action throughput by up to 2.44x.
- The evaluation includes a real Franka Panda robot and synthetic multi-robot workloads replaying real robot observations.
- The paper reports that gains come from request-rate control, resource allocation across model components, and profiling-guided batching.
- The motivation includes concrete hardware gaps: NVIDIA B100 has 29x the memory bandwidth and 3.5x the FP8 compute of Jetson Thor, while the cited Figure 02 robot has a 2.25 kWh battery with about 5 hours of runtime and dual onboard RTX GPUs taking up to half of system power.

## Link
- [https://arxiv.org/abs/2607.01088v1](https://arxiv.org/abs/2607.01088v1)
