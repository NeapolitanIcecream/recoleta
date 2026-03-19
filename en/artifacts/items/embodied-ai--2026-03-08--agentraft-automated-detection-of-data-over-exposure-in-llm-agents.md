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
- llm-agent-security
- privacy-auditing
- data-flow-analysis
- taint-tracking
- tool-using-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# AgentRaft: Automated Detection of Data Over-Exposure in LLM Agents

## Summary
AgentRaft studies the privacy risk in which LLM agents transmit sensitive data that should not be shared during cross-tool calls, and proposes the first automated detection framework. Its core value is turning this kind of “data over-exposure” from a vague risk into a problem that can be systematically discovered and quantitatively audited.

## Problem
- The paper defines **Data Over-Exposure (DOE)** in LLM Agents: when an agent executes a multi-step tool chain, it passes data beyond user intent and not necessary for the task to downstream/third-party tools.
- This matters because modern Agents often use chained workflows such as “read files/emails → process → send,” where tools often return overly broad data, while LLMs lack a stable sense of contextual privacy boundaries, making sensitive information leakage more likely.
- Traditional static program analysis struggles to handle LLM-driven dynamic, probabilistic tool orchestration; meanwhile, manually designing test prompts is costly and provides poor coverage, so an automated DOE discovery method is needed.

## Approach
- Build a **Cross-Tool Function Call Graph (FCG)**: first use static type compatibility to filter potentially connectable function pairs, then use an LLM to perform semantic validation based on function descriptions, yielding valid cross-tool data-flow paths.
- Traverse source-to-sink call chains along the FCG, and convert each chain into executable **high-fidelity user prompts** to trigger the target multi-step tool calls as deterministically as possible.
- Perform **fine-grained data-flow/taint tracking** at runtime to record which source data is ultimately transmitted to downstream sink tools.
- Use a **multi-LLM voting committee** based on the data minimization principles of GDPR, CCPA, and PIPL to determine which transmitted data was explicitly intended by the user, which is truly necessary for the task, and which constitutes over-exposure.

## Results
- The evaluation environment is drawn from **6,675 real-world tools**, covering **4 mainstream scenarios**: Data Management, Software Development, Enterprise Collaboration, and Social Communication.
- The paper claims DOE is a systemic risk: **57.07%** of potential tool call chains contain unauthorized sensitive data exposure; at the field level, **65.42%** of transmitted data fields are judged to be over-exposed.
- Compared with an unguided random-search baseline, the random method still struggles to exceed **20% vulnerability coverage after 300 attempts**; AgentRaft reaches a **69.15%** discovery rate within **50 prompts** and approaches **99%** DOE coverage at **150 prompts**.
- The multi-LLM voting audit improves DOE identification performance by **87.24%** relative to baselines (described in the paper as “outperforming baselines by 87.24% / improving DOE identification by 87.24%”).
- In terms of audit cost, AgentRaft **reduces per-call-chain verification cost by 88.6%**, enabling larger-scale, lower-cost privacy compliance detection.

## Link
- [http://arxiv.org/abs/2603.07557v1](http://arxiv.org/abs/2603.07557v1)
