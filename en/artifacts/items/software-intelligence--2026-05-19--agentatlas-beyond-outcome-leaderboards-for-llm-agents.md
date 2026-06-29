---
source: arxiv
url: https://arxiv.org/abs/2605.20530v1
published_at: '2026-05-19T22:05:12'
authors:
- Parsa Mazaheri
- Kasra Mazaheri
topics:
- llm-agents
- agent-evaluation
- tool-use
- trajectory-diagnosis
- benchmark-audit
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AgentAtlas: Beyond Outcome Leaderboards for LLM Agents

## Summary
AgentAtlas argues that final task success is too narrow for evaluating LLM agents that use tools, edit code, browse, and act in user environments. It proposes shared labels for control decisions and trajectory failures, then shows that prompt format and evaluation axis can change model rankings on the same items.

## Problem
- Agent leaderboards often report one outcome score, which can hide unsafe actions, missed confirmations, over-refusal, loops, bad recovery, and wrong tool use.
- This matters for deployable agents because a correct final answer can still come from a harmful or invalid action path.
- Current agent benchmarks measure different units, such as task success, pass^k consistency, prompt-injection attack success, or failure-step localization, so results are hard to compare across coding, web, OS, tool-use, and security tasks.

## Approach
- The paper defines six control decisions for agents: Act, Ask, Refuse, Stop, Confirm, and Recover.
- It uses a nine-category trajectory-failure taxonomy, then adds two separate labels: `primary_error_source` and `impact`.
- It audits 15 agent benchmarks across six behavior axes to show which agent behaviors are directly scored, partially exercised, or absent.
- It runs a fixed synthetic evaluation with 1,342 items across Control, Trajectory, and Security splits on 8 models: 4 closed models and 4 open-weight models.
- It compares taxonomy-aware prompts, which show the label menu, with taxonomy-blind prompts, which ask for a free-form diagnosis and map it back to the same labels.

## Results
- On the paper’s synthetic run, removing the explicit trajectory label menu drops every model by 14–40 percentage points, and blind-mode trajectory accuracy compresses to 0.54–0.62 across all 8 models.
- Taxonomy-aware control accuracy clusters tightly: 7 of 8 models score 0.870–0.946, while gpt-oss-20B scores 0.743.
- No model wins all three reported axes. Claude Haiku 4.5 scores 0.95 on control and 0.95 on trajectory, but only 0.28 on tool-context utility retention; gpt-5.4-mini scores 0.98 on tool-context utility but 0.82 on trajectory.
- The benchmark audit finds broad strong coverage for tool execution, with 9 of 15 benchmarks scoring strong coverage. Memory and state has strong coverage in only 1 benchmark, ToolSandbox, and efficiency has 0 strong-coverage benchmarks.
- The paper cites external evidence for axis sensitivity: an uncertainty-aware policy on ambiguous SWE-bench Verified tasks raises resolution from 61.2% to 69.4%; tau-bench ranks Claude Opus 4.5 highest at pass^1 with 0.70, while Qwen3.5 ranks highest at pass^4 with 0.56.
- The authors frame the 1,342-item run as a measurement-protocol demonstration, not a public benchmark release, and note that the generated gold labels come from one Claude Opus 4.7 checkpoint without a human-calibrated subset.

## Link
- [https://arxiv.org/abs/2605.20530v1](https://arxiv.org/abs/2605.20530v1)
