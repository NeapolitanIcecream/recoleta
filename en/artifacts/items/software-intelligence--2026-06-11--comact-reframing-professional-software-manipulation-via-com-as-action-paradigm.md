---
source: arxiv
url: https://arxiv.org/abs/2606.13239v1
published_at: '2026-06-11T11:53:32'
authors:
- Jiaxin Ai
- Tao Hu
- Xuemeng Yang
- Shu Zou
- Hairong Zhang
- Daocheng Fu
- Yu Yang
- Hongbin Zhou
- Nianchen Deng
- Pinlong Cai
- Zhongyuan Wang
- Botian Shi
- Kaipeng Zhang
- Licheng Wen
topics:
- computer-use-agents
- com
- cad-automation
- software-foundation-model
- code-generation
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# ComAct: Reframing Professional Software Manipulation via COM-as-Action Paradigm

## Summary
ComAct reframes professional software control as code generation over COM interfaces, which matters because GUI agents fail in dense CAD software and API-based agents do not cover commercial tools well.

## Problem
- Professional software automation breaks down in real CAD workflows because GUI control is brittle and long-horizon errors pile up.
- API and MCP tools are too fragmented or unavailable for many commercial applications.
- The paper targets industrial CAD as the main test case because it needs precise geometry, long action chains, and cross-application steps.

## Approach
- It treats COM, the Windows object model used by software such as SolidWorks, AutoCAD, Office, and Adobe apps, as the action space.
- The agent writes executable Python COM scripts instead of issuing many low-level mouse and keyboard steps.
- It builds ComCADBench, a benchmark with 1,000 tasks across SolidWorks, Inventor, and AutoCAD, split into 400 single-task and 600 multi-task cases.
- It trains ComActor in three stages: instruction-to-code supervised fine-tuning, multi-turn correction from execution feedback, and GRPO reinforcement learning with a continuous geometric reward based on Chamfer Distance.
- It uses ComForge, a Dockerized Windows platform with 1,000+ parallel real environments for training and evaluation.

## Results
- ComCADBench contains 1,000 tasks across 3 CAD applications and 7 activities, with evaluation by code validity and task success.
- The paper reports near-zero success for GUI-based agents on the benchmark, while COM-based execution gives large immediate gains.
- In Table 1, the authors report their method at 90.0/81.0, 96.0/89.0, 95.0/88.0, 86.0/86.0, 84.0/75.0, 97.0/87.0, 76.0/61.0, 78.0/58.0, 98.0/86.0, and 95.0/80.0 across the listed single-task and multi-task settings, where each cell is Code Valid Rate / Task Success Rate.
- The strongest baseline in the table reaches 82.0/88.0 on one setting and 76.0/74.0 on another, while many other baselines stay near 0.0 without few-shot prompting.
- The paper also claims generalization to external CAD benchmarks, including Text2CAD and CADPrompt, but the excerpt does not provide their numeric scores.

## Link
- [https://arxiv.org/abs/2606.13239v1](https://arxiv.org/abs/2606.13239v1)
