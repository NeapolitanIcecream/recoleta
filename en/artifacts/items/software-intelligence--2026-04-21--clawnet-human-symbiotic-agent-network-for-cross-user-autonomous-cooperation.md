---
source: arxiv
url: http://arxiv.org/abs/2604.19211v1
published_at: '2026-04-21T08:15:05'
authors:
- Zhiqin Yang
- Zhenyuan Zhang
- Xianzhang Jia
- Jun Song
- Wei Xue
- Yonggang Zhang
- Yike Guo
topics:
- multi-agent-systems
- cross-user-collaboration
- identity-governance
- os-level-agents
- human-ai-interaction
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# ClawNet: Human-Symbiotic Agent Network for Cross-User Autonomous Cooperation

## Summary
ClawNet proposes a cross-user agent system where each agent is tied to one human owner and can cooperate with other users' agents under explicit identity, permission, and audit rules. The paper’s main claim is that current agent systems handle single-user automation well but lack the governance needed for multi-user autonomous collaboration.

## Problem
- Current single-agent and multi-agent systems mostly operate for one user or one shared principal, so they do not support agents acting for different people with distinct interests.
- Cross-user autonomous cooperation needs three missing pieces: stable owner identity, scoped authorization, and action-level accountability.
- Without those controls, cross-user agents risk unauthorized access, private data leakage, and decisions made without a clear human mandate.

## Approach
- ClawNet builds a **human-symbiotic agent network** where the network nodes are humans, and agents mediate collaboration between them.
- Each user has a permanently bound agent system with one **manager agent** and multiple **identity agents**. The manager holds broad owner knowledge but is isolated from external communication; identity agents expose only context-specific roles and knowledge.
- Cross-user collaboration requires bilateral approval, authorized visibility between identity agents, and bounded recursive delegation to other users when needed.
- The system enforces three governance mechanisms on every action: identity binding to a specific owner and identity agent, scoped authorization for allowed resources, and append-only audit logging.
- ClawNet uses a cloud-edge design: persistent cloud services handle orchestration and identity state, while a local client executes OS-level file operations with two independent permission checks, backups, and rollback support.

## Results
- The excerpt gives **no benchmark table or aggregate quantitative evaluation metrics** such as accuracy, success rate, latency, or cost.
- The paper claims ClawNet is the first system in its comparison table to fully support all four properties together: **identity binding, scoped authorization, action accountability, and cross-owner collaboration**; competing categories are marked partial or unsupported.
- The system supports **OS-level** file actions such as read, write, move, rename, copy, create, and secure delete through a local node endpoint.
- The authorization path has **two independent layers**: server-side L1 ACL and client-side L2 folder whitelist, with fail-closed rejection if either layer denies a request.
- In the described procurement case, the workflow runs through **9 steps** of inter-agent negotiation and escalation, with human approval required for final decisions and unauthorized requests rejected by governance checks.
- The authors state ClawNet has been **deployed and tested across cross-organizational collaboration scenarios**, with concrete claimed effects including identity isolation, authorization enforcement, full auditability, pre-execution backup, and undo or batch rollback for mutating file operations.

## Link
- [http://arxiv.org/abs/2604.19211v1](http://arxiv.org/abs/2604.19211v1)
