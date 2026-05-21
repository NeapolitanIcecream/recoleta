---
source: arxiv
url: https://arxiv.org/abs/2605.08013v1
published_at: '2026-05-08T17:02:31'
authors:
- Haoyang Su
- Ying Wen
topics:
- cli-agents
- agentic-rl
- code-intelligence
- credit-assignment
- workspace-context
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Learning CLI Agents with Structured Action Credit under Selective Observation

## Summary
The paper trains CLI coding agents by giving better credit to shell actions and selecting a useful initial workspace view. Its main claim is that AST-based action credit plus σ-Reveal improves Qwen3-14B on multi-turn filesystem tasks.

## Problem
- CLI agents must act in large repositories with partial context, so the model may miss task-relevant files before it runs any command.
- Training feedback is often a sparse final reward from terminal output or file state, so standard RL struggles to identify which shell commands helped or hurt.
- This matters for code agents because real software work uses search, execution, editing, and verification over many turns, rather than single input-output prediction.

## Approach
- σ-Reveal chooses an initial file-tree view under a token budget. It scores files and directories using task-name matches, tree depth, and file-extension priors, then keeps a subtree-closed context.
- A3 parses each shell command with a bash AST and converts it into a structural signature with control nodes, command verbs, and normalized literals.
- The method compares shell actions with normalized Levenshtein distance over these AST signatures, so similar commands can share credit even when paths or literals differ.
- A3 builds each turn advantage from three signals: episode-level relative return, a turn-level residual against structurally similar actions, and a tree-level margin over abstract action-history branches.
- The fused advantage trains the policy with a sequence-level PPO-style loss, without a learned critic or external judge for credit assignment.

## Results
- ShellOps contains 1,624 tasks, with 714 in-distribution tasks used for training and evaluation. ShellOps-Pro adds 150 harder out-of-distribution tasks with 4,063 files, averaging 27.1 files per task across 42 readable text extensions plus extensionless files.
- On exact-match ShellOps string tasks, A3 with σ-Reveal scores 48.5%, compared with 27.5% for the strongest non-A3 baseline in the table. On ShellOps hybrid tasks, it scores 24.6%, compared with 11.3% for the strongest non-A3 baseline.
- On ShellOps file-editing tasks, A3 vanilla scores 26.5% and A3 with σ-Reveal scores 25.7%, compared with 11.9% for the strongest non-A3 baseline.
- On DataBench exact match, A3 with σ-Reveal scores 77.9%, compared with 70.1% for GSPO. On TableBench, it scores 31.6%, compared with 25.0% for RetroAgent.
- Pass@3 / Pass@5 on ShellOps reaches 46.2% / 55.7% with A3 plus σ-Reveal, compared with 22.3% / 28.6% for the strongest non-A3 baseline shown.
- The ShellOps-Pro excerpt reports frontier baselines over horizons 6 / 8 / 10: Kimi-K2.6 scores 45.9 / 47.9 / 53.3, GLM-5.1 scores 34.7 / 39.1 / 40.7, and Qwen3-235B-A22B scores 26.7 / 29.3 / 28.3. The excerpt says A3 reaches the Qwen3-235B-A22B range at longer horizons, but the exact A3 ShellOps-Pro numbers are not visible in the provided text.

## Link
- [https://arxiv.org/abs/2605.08013v1](https://arxiv.org/abs/2605.08013v1)
