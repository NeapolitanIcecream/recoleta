---
source: arxiv
url: https://arxiv.org/abs/2605.14859v2
published_at: '2026-05-14T14:05:58'
authors:
- Zheng Yan
- Jingxiang Weng
- Charles Chen
- Dengyun Peng
- Ethan Qin
- Jiannan Guan
- Jinhao Liu
- Qiming Yu
- Yixin Yuan
- Fanqing Meng
- Carl Che
- Mengkang Hu
topics:
- coding-agents
- least-privilege
- authorization
- code-intelligence
- agent-safety
- benchmark
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Do Coding Agents Understand Least-Privilege Authorization?

## Summary
The paper studies whether coding agents can choose file-level permissions for terminal tasks before they act. It introduces AuthBench and a two-step policy-generation method that improves task success and reduces attack paths in the reported tests.

## Problem
- Coding agents now read files, write code, and run shell commands, so broad default permissions can expose secrets, unsafe scripts, and other sensitive files.
- The task is hard because an agent must grant every permission needed for completion while avoiding permissions that open attack paths.
- Current evaluations often assume the permission policy already exists; this paper tests whether models can infer that policy from the task and environment.

## Approach
- The paper defines permission-boundary inference: given a task instruction and terminal environment, a model outputs read, write, and execute allowlists over POSIX path patterns.
- It builds AuthBench with 120 terminal tasks: 80 standard tasks and 40 sensitive tasks with human-reviewed permission labels, utility validators, and attack validators.
- The benchmark scores static permission match with precision, recall, and F1, then runs a fixed GPT-5 execution agent under the generated policy to measure task success rate.
- The proposed Sufficiency-Tightness Decomposition first asks the model to generate a broad policy by simulating the likely task workflow, then audits each permission and removes entries without task grounding or with sensitive exposure.

## Results
- On standard tasks, Full-Access reaches 83.3% TSR and Golden-Permission reaches 77.1% TSR. The best generated policy is Gemini 3.1 Pro at 75.4% TSR, with read F1 78.0, write F1 85.3, and execute F1 49.0.
- On sensitive tasks, Full-Access reaches 94.0% TSR but 65.8% ASR. Golden-Permission reaches 81.7% TSR and 0.0% ASR.
- Gemini 3.1 Pro has the highest sensitive-task TSR among generated policies at 85.8%, with SER 34.8% and ASR 28.3%.
- GPT-5.4 has lower sensitive exposure than Gemini, with SER 21.1% and ASR 19.4%, but its sensitive-task TSR is 61.1%.
- The paper reports that more inference-time reasoning moves models toward model-specific permission styles: Gemini tends to grant broader access, while GPT-5.4 and Claude Opus 4.6 tend to produce tighter policies that miss needed permissions.
- The decomposition method improves sensitive-task success by up to 15.8% on tightness-biased models, reduces attack success across all tested models, and improves execute-axis F1 by up to 16.7% on standard tasks.

## Link
- [https://arxiv.org/abs/2605.14859v2](https://arxiv.org/abs/2605.14859v2)
