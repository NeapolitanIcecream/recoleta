---
source: arxiv
url: https://arxiv.org/abs/2605.20251v1
published_at: '2026-05-18T08:34:48'
authors:
- Jiawei He
- Jie Jia
- Chenbo Liu
- Chaoyi Xue
- Yapeng Song
- Xikai Yang
- Dong Sun
topics:
- llm-coding-agents
- code-agent-evaluation
- process-defects
- control-preservation
- software-benchmarks
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# ProcBench: Evaluating Process-Level Defects and Control Preservation in LLM Coding Agents

## Summary
ProcBench evaluates LLM coding agents by scoring the execution trace, not only the final patch or test result. It finds repeated process defects, estimates their risk, and reports control-preservation scores for coding-agent runs.

## Problem
- Existing coding-agent benchmarks usually score task completion, compilation, or test pass rate, so they can miss brittle runs that still finish the task.
- The paper targets failures during multi-step coding work, including stale context, repeated tool calls, dead steps, long chains, weak workflow structure, and poor handoff control.
- This matters because autonomous coding agents may need supervision, rollback, or correction during execution, not only final grading after a run ends.

## Approach
- ProcBench converts raw agent logs into a shared trajectory format made of ordered events with text, tool calls, tool returns, external operations, context state, and dependency data.
- It checks 11 defect classes grouped under context management, tool-use efficiency, workflow architecture, and tool-system consistency.
- Each defect detector extracts evidence from the trajectory, then maps that evidence to a calibrated posterior risk instead of using only a hard threshold.
- The scorecard reports defect risks, dimension-level quality scores, control preservation, fragile success, and an overall ProcBench score.
- Control preservation is scored through interpretability, interruptibility, correctability, reversibility, and authority handoff.

## Results
- The study uses 200 annotated trajectories: 100 from SWE-bench-Verified, 40 from AndroidBench, and 60 from TerminalBench, across 11 agent-model configurations from Claude Code, Codex CLI, OpenCode, and Qoder.
- Stronger observable defect classes reach high detection scores: Duplicate Step F1 0.85 and AUROC 0.92; Ghost Context F1 0.85 and AUROC 0.91; Dead Step F1 0.82 and AUROC 0.90; Long Chain F1 0.81 and AUROC 0.89.
- Harder structural defect classes score lower: Wrapper Workflow F1 0.59 and AUROC 0.71; Context Coupling F1 0.61 and AUROC 0.73; Weak Tool F1 0.53 and AUROC 0.68.
- Calibration lowers overall Expected Calibration Error from 0.227 with hard thresholding to 0.138 with Bayesian calibration. By dimension, ECE drops from 0.214 to 0.118 for context management, 0.198 to 0.103 for tool-use efficiency, 0.271 to 0.196 for workflow architecture, and 0.223 to 0.134 for tool-system consistency.
- Claude Code with Claude Sonnet 4.6 has the highest reported ProcBench score at 0.742, with CP 0.75 and fragile success 10.8%. Codex CLI with gpt-5.4-0305-global scores 0.731, with the highest tool-use quality shown in the table at 0.75.
- OpenCode with Qwen3 Coder Plus has the lowest reported overall score at 0.648 and the highest fragile-success rate at 20.2%, showing that ProcBench separates agents with similar endpoint performance by process quality and control risk.

## Link
- [https://arxiv.org/abs/2605.20251v1](https://arxiv.org/abs/2605.20251v1)
