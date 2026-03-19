---
source: arxiv
url: http://arxiv.org/abs/2603.07557v1
published_at: '2026-03-08T09:40:54'
authors:
- Yixi Lin
- Jiangrong Wu
- Yuhong Nan
- Xueqiang Wang
- Xinyuan Zhang
- Zibin Zheng
topics:
- llm-agents
- privacy-security
- taint-analysis
- program-analysis
- tool-orchestration
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# AgentRaft: Automated Detection of Data Over-Exposure in LLM Agents

## Summary
This paper proposes AgentRaft, a framework for automatically detecting the risk of **Data Over-Exposure (DOE)** in LLM Agents, where sensitive data beyond the scope of user intent and functional necessity is transmitted during cross-tool calls. It models tool interactions as a graph, automatically generates prompts that trigger deep call chains, and performs runtime data-flow tracking to identify privacy violations.

## Problem
- The paper addresses the problem of **LLM Agents unintentionally leaking excessive sensitive data during multi-tool collaboration**: a user may intend to share only part of some information, but the Agent may pass the entire sensitive content to downstream tools or third parties.
- This matters because data flows in Agent toolchains are dynamic and non-deterministic, making traditional static privacy/taint analysis hard to apply comprehensively; it also directly relates to compliance requirements such as GDPR, CCPA, and PIPL.
- The authors argue that DOE easily arises in current Agent designs, mainly because tools return overly broad data and LLMs lack awareness of fine-grained contextual privacy boundaries.

## Approach
- AgentRaft first constructs a **Cross-Tool Function Call Graph (FCG)**: it combines static compatibility analysis of function signatures with LLM-based semantic validation to identify which tool functions have real data dependency relationships.
- It then traverses source-to-sink call chains in the FCG and converts each chain into a **high-fidelity user prompt** that can reliably trigger that path, enabling systematic exploration of deep tool compositions rather than random probing.
- When executing these prompts, the system performs **runtime data-flow/taint tracking**, recording data retrieved from source tools, intermediate data after LLM processing, and final data sent to sink tools.
- Finally, through a **multi-LLM voting audit mechanism** based on GDPR/CCPA/PIPL, it determines which transmitted data the user explicitly intended to share, which data was actually necessary for the task, and which data constitutes DOE.

## Results
- In a test environment built from **6,675 real-world tools**, the authors find that DOE is a systemic risk: **57.07%** of potential tool interaction paths contain unauthorized sensitive data exposure.
- At a finer granularity, **65.42%** of all transmitted data fields are classified as over-exposed, indicating a serious mismatch between current Agent execution patterns and the principle of data minimization.
- Compared with an unguided random-search baseline that **still struggles to exceed 20% vulnerability coverage after 300 attempts**, AgentRaft reaches a **69.15%** discovery rate within **50 prompts** and achieves nearly **99%** DOE coverage at **150 prompts**.
- Its multi-LLM voting audit improves DOE identification effectiveness by **87.24%** over baselines (described in the paper as within 150 prompts outperforming baselines by 87.24%).
- In terms of audit cost, AgentRaft **reduces per-call-chain verification cost by 88.6%**, suggesting it is suitable for large-scale, low-cost Agent privacy auditing.

## Link
- [http://arxiv.org/abs/2603.07557v1](http://arxiv.org/abs/2603.07557v1)
