---
source: arxiv
url: https://arxiv.org/abs/2605.19769v1
published_at: '2026-05-19T12:40:29'
authors:
- Jinbiao Wei
- Qianran Ma
- Yilun Zhao
- Xiao Zhou
- Kangqi Ni
- Guo Gan
- Arman Cohan
topics:
- computer-use-agents
- desktop-benchmark
- verifiable-evaluation
- software-worlds
- agent-training
- gui-automation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# OpenComputer: Verifiable Software Worlds for Computer-Use Agents

## Summary
OpenComputer builds verifiable desktop software tasks for computer-use agents, with programmatic checks tied to real application state. The paper claims current agents still miss many end-to-end tasks, even when they make partial progress.

## Problem
- Desktop-agent benchmarks are expensive to build because each task needs a realistic initial state, such as files, profiles, settings, documents, or browser data.
- Screenshot-based or LLM-judge scoring can miss hidden state errors in files, metadata, preferences, databases, or saved application state.
- Better training and evaluation need tasks that are reproducible and rewards that can be audited by running checks inside the desktop environment.

## Approach
- OpenComputer creates app-specific Python verifier modules that expose CLI endpoints with JSON outputs for real applications.
- Verifiers inspect state through application-specific channels such as browser debugging protocols, D-Bus, LibreOffice UNO, SQLite profile databases, accessibility state, and saved-file parsing.
- A self-evolving verifier loop runs about 15 calibration tasks per application, compares programmatic verifier verdicts with criterion-level LLM reference judgments, and repairs verifier-side errors in checker code, endpoint code, or documentation.
- The task generator proposes realistic user goals, filters them for difficulty and data generation, keeps tasks whose outcomes can be checked, and packages each task as an instruction, sandbox initializer, and executable success criteria.
- The evaluation harness runs agents in fresh sandboxes, records screenshot-action trajectories, and scores each task as the fraction of verifier checks passed.

## Results
- The released benchmark contains 33 desktop applications and 1,000 finalized tasks, with 17.7 verifier endpoints per app, 6.9 checks per task, and 1.3 seed files per task on average.
- GPT-5.4 scores 68.3% task success and 88.4% average reward, with 19.0 average steps and 16.5 seconds per step.
- Claude-Sonnet-4.6 reaches 64.4% success and 76.6% average reward; Kimi-K2.6 reaches 58.8% success and 70.7% average reward.
- Open-source models fall much lower: Qwen-3.5-27B reaches 32.3% success, EvoCUA-8B reaches 10.9%, Qwen-3.5-9B reaches 7.8%, and GUI-OWL-1.5-8B reaches 5.7%.
- The paper reports large drops versus OSWorld-Verified for some open-source models, such as GUI-OWL-1.5-8B dropping from 52.3% to 5.7% and EvoCUA-8B dropping from 46.1% to 10.9%.
- The excerpt gives no exact human-alignment percentage, but claims hard-coded verifiers align better with human adjudication than LLM-as-judge scoring when success depends on fine-grained application state.

## Link
- [https://arxiv.org/abs/2605.19769v1](https://arxiv.org/abs/2605.19769v1)
