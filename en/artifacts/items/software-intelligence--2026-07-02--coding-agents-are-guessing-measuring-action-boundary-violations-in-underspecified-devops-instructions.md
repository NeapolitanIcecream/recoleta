---
source: arxiv
url: https://arxiv.org/abs/2607.02294v1
published_at: '2026-07-02T15:11:39'
authors:
- Zimo Ji
- Zekai Zhang
- Congying Xu
- Zongjie Li
- Yudong Gao
- Shuai Wang
- Shing-Chi Cheung
topics:
- coding-agents
- devops-safety
- code-intelligence
- agent-benchmarks
- human-ai-interaction
- software-automation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions

## Summary
UnderSpecBench tests whether coding agents guess when DevOps instructions omit the intended action, target, or scope. Across OpenCode, Claude Code, and Codex setups, the paper finds that agents often act under ambiguity and cross action boundaries.

## Problem
- Coding agents can run shell commands, edit repositories, and call operational APIs, so a plausible action on the wrong branch, namespace, database, route, or artifact can cause real damage.
- Existing agent benchmarks mostly score task completion. They miss cases where the task appears completed but the agent touched the wrong object or used a broader command than the user authorized.
- The paper targets benign underspecified DevOps requests, such as cleanup, rollback, pruning, and access changes, where the safe response may be to ask for clarification.

## Approach
- The authors build UnderSpecBench with 69 DevOps task families grounded in documented incidents, CVEs, or tool behavior.
- Each task has 32 prompt variants, created by crossing 4 intent-clarity levels, 4 target-certainty levels, and 2 blast-radius levels, for 2,208 prompts.
- The environment and ground-truth safe action stay fixed while only the instruction changes, so behavior changes can be tied to underspecification.
- Deterministic per-task oracles inspect state diffs, command logs, and service-side effects to classify Safe Success, Wrong Target, and OverScope outcomes.
- Non-action runs are classified as Ask, Refuse, or Defer using a DeepSeek-v4-flash judge on the final message.

## Results
- The study evaluates 5 agent-model configurations over all 69 task families and 2,208 prompt variants: OpenCode with Haiku-4.5, Codex-5.1-mini, and DeepSeek-v4; Claude Code with Haiku-4.5; and Codex with Codex-5.1-mini.
- Safe Success rates range from 15.5% for Codex + Codex-5.1-mini to 36.8% for OpenCode + DeepSeek-v4.
- Overstep rates over all scored runs range from 27.0% for Claude Code + Haiku-4.5 to 46.3% for OpenCode + DeepSeek-v4; among acted runs, the paper reports 55.8–67.8% boundary violations.
- Wrong Target rates range from 13.1% to 31.8%, and OverScope rates range from 24.9% to 44.4% across configurations.
- Under Completion rates range from 38.3% to 69.2%, showing that many runs stop without an oracle-recognized safe or unsafe action.
- Target underspecification has the strongest link to Wrong Target behavior; intent underspecification has a weaker effect, and blast-radius cues have little effect on whether agents act.

## Link
- [https://arxiv.org/abs/2607.02294v1](https://arxiv.org/abs/2607.02294v1)
