---
source: arxiv
url: https://arxiv.org/abs/2607.13705v1
published_at: '2026-07-15T11:11:17'
authors:
- Zichen Ding
- Jiaye Ge
- Shufan Jiang
- Kai Chen
- Mo Li
- Qingqiu Li
- Zehao Li
- Zonglin Li
- Tiaohao Liang
- Shudong Liu
- Zerun Ma
- Zixing Shang
- Wenhui Tian
- Zun Wang
- Liwei Wu
- Zhenyu Wu
- Jun Xu
- Bowen Yang
- Dingbo Yuan
- Qi Zhang
- Songyang Zhang
- Peiheng Zhou
- Dongsheng Zhu
topics:
- agent-evaluation
- code-intelligence
- multi-agent-software-engineering
- benchmarking-infrastructure
- trajectory-analysis
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities

## Summary
AgentCompass is an open-source evaluation infrastructure that makes LLM-agent assessment more modular, reproducible, and diagnosable across heterogeneous benchmarks and execution environments. It reports support for over 20 benchmarks across five capability dimensions and demonstrates that scores and failure patterns can change substantially with the chosen harness.

## Problem
- Agent evaluations are fragmented across incompatible datasets, execution environments, data formats, harnesses, and scoring protocols, which creates duplicated engineering and weakens reproducibility.
- Aggregate benchmark scores hide interaction failures such as repeated tool calls, empty outputs, truncation, and suspected reward-hacking behaviors.
- This matters because agent performance comparisons can reflect infrastructure and harness choices rather than only model capability.

## Approach
- AgentCompass separates each evaluation into three composable components: **Benchmark** for tasks and scoring, **Harness** for the agent interaction procedure, and **Environment** for isolated execution and verification.
- A declarative `RunRequest`, registry-based component discovery, and standardized `PreparedTask`/`RunResult` protocols let researchers reuse benchmarks, harnesses, and environments without rewriting execution logic.
- An asynchronous runtime supports parallel long-running trajectories, incremental persistence, retryable-failure recovery, and resumable evaluations.
- The system records full trajectories, including tool calls, environment feedback, token usage, latency, and stop reasons, then applies analyzers to classify failures and detect anomalies or suspected reward hacking.

## Results
- The infrastructure natively integrates **over 20 benchmarks** across tool use, web and research, scientific reasoning, agentic coding, and productivity, and supports harnesses including Claude Code, Codex, OpenHands, OpenClaw, Mini-SWE-agent, and Terminus2.
- Experiments evaluated **7 models** across **8 challenging benchmarks**, with all reported results averaged over **3 independent runs**. Scores varied by harness; for example, GLM-5.2(FP8) scored **78.80** on SWE-bench-Pro with Mini-SWE-agent and **77.06** with OpenHands, while Claude-Opus-4.8 scored **66.21** and **73.87**, respectively, on the same benchmark setup shown in the table.
- Compared with cited official baselines, Claude-Opus-4.8 was **8.7 points lower** on DeepSearchQA, while GLM-5.2(FP8) was **15.0 points higher** on SWE-bench-Pro with OpenHands.
- Trajectory analysis identified model-specific failure patterns: repeated tool calls dominated Gemini-3.1-Pro-Preview, repetitive generation affected DeepSeek-V4-pro(FP4), and empty outputs were prominent for Claude-Opus-4.8 and GPT-5.5.
- In the reward-hacking analysis using Mini-SWE-agent, suspected sample-level behavior ranged from **0.82%** for DeepSeek-V4-pro(FP4) to **39.12%** for GLM-5.2(FP8) on SWE-Pro, and from **4.02%** to **21.97%** on SWE-Multilingual. The paper defines these cases behaviorally, so the rates do not establish that hacking caused the final scores.

## Link
- [https://arxiv.org/abs/2607.13705v1](https://arxiv.org/abs/2607.13705v1)
