---
source: arxiv
url: https://arxiv.org/abs/2606.23654v1
published_at: '2026-06-22T17:39:43'
authors:
- Jincheng Zhong
- Weizhi Wang
- Che Jiang
- Kai Tian
- Zhenzhao Yuan
- Junlin Yang
- Dianqiao Lei
- Kaiyan Zhang
topics:
- agent-benchmark
- enterprise-agents
- workspace-automation
- artifact-evaluation
- skill-transfer
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions

## Summary
EnterpriseClawBench is a protocol for turning real enterprise agent sessions into reproducible workplace tasks and scoring agents on delivered files, quality, cost, and runtime. The strongest Lite result is 0.663, so the paper claims current enterprise agents still miss many artifact-delivery and content-quality requirements.

## Problem
- Enterprise agents work inside file-based workspaces, where success depends on finding inputs, using tools, preserving state, and producing usable artifacts, not only writing a correct chat answer.
- Existing agent benchmarks often use public, simulated, or hand-written tasks, so they miss many messy demands found in workplace sessions.
- Enterprise teams need scores by harness-model pair, task class, artifact type, cost, runtime, and skill transfer because a base model score alone can hide delivery failures.

## Approach
- The pipeline starts with internal workplace sessions from March to May 2026 at an AI startup with more than 100 employees.
- It splits and merges session turns into task candidates, then filters them for length, recoverable input fixtures, redaction recovery, network dependence, and self-contained user intent.
- Accepted tasks are rewritten as single-turn prompts and packaged with recovered files, role classes, 45 skill subclasses, expected deliverables, hard rules, and text or visual rubrics.
- Each harness-model pair runs in a fresh Linux sandbox; the runner uploads inputs, calls the agent, downloads outputs and traces, and records completion, time, token use, cost, and tool calls.
- Scoring combines objective file checks with semantic judges for grounded accuracy, task relevance, substantive depth, practical utility, and communication quality.

## Results
- The construction funnel starts from 5,291 raw TaskInstances and yields 852 final benchmark tasks; the manually audited Lite subset has 120 tasks.
- On the 120-task Lite set, the best of 32 harness-model combinations is Codex with GPT-5.5 at 0.663, with Sonnet 4.6 around 0.62-0.64 under Claude Code, DeepAgents, and OpenClaw, but 0.458 under Hermes.
- On the full 852-task set under DeepAgents, GPT-5.5 scores 0.766 overall, with 0.813 text, 0.642 visual, and 0.959 rule score; Sonnet 4.6 scores 0.749, Haiku 4.5 scores 0.632, and GPT-4.1-mini scores 0.336.
- Skill injection on held-out frontend page generation tasks shows creator-dependent transfer: GPT-5.5 skills average +0.0681, Kimi K2.6 skills average +0.0518, and Haiku 4.5 skills average -0.0941.
- Judge checks show strong LLM-LLM agreement for text scores, with GPT-5.4-text vs Sonnet 4.6 at Spearman 0.918 over 1,853 cases; visual agreement is lower at 0.866 over 1,428 cases.
- Human audit over 48 packets finds better text calibration than visual calibration: text MAE is 0.134 with Spearman 0.790, while visual MAE is 0.303 with Spearman -0.259.

## Link
- [https://arxiv.org/abs/2606.23654v1](https://arxiv.org/abs/2606.23654v1)
