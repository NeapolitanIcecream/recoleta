---
source: arxiv
url: https://arxiv.org/abs/2606.03461v1
published_at: '2026-06-02T10:37:47'
authors:
- Sidi Yang
- Chaofan Tao
- Jierun Chen
- Tiezheng Yu
- Ruoyu Wang
- Yuxin Jiang
- Yiming Du
- Wendong Xu
- Jing Xiong
- Taiqiang Wu
- Lifeng Shang
- Xiaohui Li
- Ngai Wong
- Haoli Bai
topics:
- terminal-agents
- code-intelligence
- agent-training
- software-foundation-models
- trajectory-distillation
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# What Makes Interaction Trajectories Effective for Training Terminal Agents?

## Summary
The paper finds that the best terminal-agent teacher is not the model with the highest standalone benchmark score. DeepSeek-V3.2 produces better students than Claude Opus 4.6 because its traces show more inspect-act-verify behavior that students can imitate.

## Problem
- Terminal agents are trained on interaction traces, but teacher selection often uses the teacher's task success rate as the main signal.
- This matters because a high-scoring agent may solve tasks with short, hidden, or weakly grounded actions that give students less useful supervision.
- The paper asks which trajectory properties make terminal-agent fine-tuning data transfer well to Qwen3-8B and Qwen3-32B students.

## Approach
- The authors build Terminal-Lego, a pipeline that turns StackOverflow issues into Docker-verified terminal-agent tasks across 90+ technical domains.
- They collect trajectories from DeepSeek-V3.2, Claude Opus 4.6, Qwen3.5-Plus, and GLM-5 using the same Terminus-2 terminal harness.
- They compare teachers on matched task sets where all teachers solved the same instances, then fine-tune the same Qwen3 student models.
- The core mechanism is Environment-Grounded Supervision: useful traces show the agent inspecting files or state, acting, checking outputs, and adapting.
- They define Targeted Observation Ratio (TOR), the share of action commands supported by a relevant earlier observation of the same path or related state.

## Results
- On Terminal-Bench 2.0, Claude Opus 4.6 scores 69.4 as a standalone agent, while DeepSeek-V3.2 scores 39.3; after SFT on 8.1K matched successful traces, DeepSeek-V3.2 trains stronger students: Qwen3-8B reaches 10.5% Pass@1 and Qwen3-32B reaches 20.6%, compared with Claude's 5.6% and 15.5%.
- With 15.3K Terminal-Lego trajectories, Qwen3-32B reaches 24.3% on Terminal-Bench 2.0, reported as a 7x gain over the base model and close to prior SOTA trained with more than 30x the data.
- Longer trajectories alone do not explain the gain: on 1.1K hard instances, shortest DeepSeek-V3.2 successful traces beat longest ones for Qwen3-32B, 13.9% vs 12.7%, even though longest traces have more turns, 12.2 vs 8.9, and more error turns, 3.8 vs 2.7.
- Removing explicit error-message trajectories keeps DeepSeek-V3.2 ahead: on 1.7K error-free traces, Qwen3-32B reaches 19.1% with DeepSeek-V3.2, versus 10.5% with Claude, 11.2% with Qwen3.5-Plus, and 15.4% with GLM-5.
- Masking observation-command supervision in 8.1K DeepSeek-V3.2 traces cuts TOR from 13.4% to 5.3% and drops Qwen3-32B from 20.6% to 13.8%, with Qwen3-8B falling from 10.5% to 3.8%.
- High-TOR selection helps at fixed data size: with 1.1K successful DeepSeek-V3.2 traces, Qwen3-32B reaches 14.6% on high-TOR data, 11.8% on low-TOR data, and 13.8% on random data.

## Link
- [https://arxiv.org/abs/2606.03461v1](https://arxiv.org/abs/2606.03461v1)
