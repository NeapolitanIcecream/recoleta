---
source: arxiv
url: https://arxiv.org/abs/2605.14866v1
published_at: '2026-05-14T14:13:59'
authors:
- Lingzhe Zhang
- Tong Jia
- Kangjin Wang
- Chiming Duan
- Minghua He
- Rongqian Wang
- Xi Peng
- Meiling Wang
- Gong Zhang
- Renhai Chen
- Ying Li
topics:
- multi-agent-systems
- llm-agents
- microservice-observability
- root-cause-localization
- aiops
- software-reliability
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Towards In-Depth Root Cause Localization for Microservices with Multi-Agent Recursion-of-Thought

## Summary
RCLAgent localizes root causes in microservice failures by mapping LLM agents to trace spans and running diagnosis along the trace graph in parallel. It targets context growth and serial tool-use latency in LLM-based root cause localization.

## Problem
- Microservice failures spread across services, pods, nodes, logs, metrics, and traces, so a surface symptom can hide the component that caused the incident.
- Existing graph and deep-learning methods can be hard to transfer across deployments or hard to interpret.
- Existing LLM methods often mix too much runtime evidence into one growing context and reason step by step, which can lose earlier signals and slow diagnosis.

## Approach
- RCLAgent assigns each trace span to a dedicated agent, so each agent checks a small local part of the request path.
- Each agent uses trace, log, and metric tools for its own span, then receives compact evidence from child agents instead of raw downstream data.
- Agents follow the trace graph recursively: parent agents combine their own local findings with child reports and pass a short hypothesis upward.
- Independent branches run in parallel, while an agent pool caps concurrent agents to control cost.
- The root agent makes the final diagnosis using a Root-Level Diagnosis Report and a Global Evidence Graph that keeps local hypotheses available for review.

## Results
- The paper evaluates RCLAgent on AIOPS 2022, Augmented-TrainTicket, and RCAEval.
- It claims RCLAgent beats the second-best root cause localization method by about 7.51% in accuracy across the tested benchmarks.
- It claims more than 1.75× inference speedup over existing LLM-based methods.
- The empirical study includes interviews with 15 developers and SREs from Peking University and Huawei Theory Lab.
- In a post-mortem of 100 failed AIOPS 2022 cases for a single-agent ReAct-style CoT baseline, 43 failures involved evidence dilution and 57 involved shallow reasoning; the 43 evidence-dilution cases include 8 lost-root-cause cases and 35 demoted-root-cause cases.
- The experimental failure definition treats a request as abnormal when its entry span latency exceeds 100× the normal average latency.

## Link
- [https://arxiv.org/abs/2605.14866v1](https://arxiv.org/abs/2605.14866v1)
