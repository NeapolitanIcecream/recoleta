---
source: arxiv
url: https://arxiv.org/abs/2606.31498v1
published_at: '2026-06-30T11:16:56'
authors:
- Richard Kang
- Yudho Diponegoro
topics:
- agent-interoperability
- multi-agent-governance
- protocol-analysis
- agent-coordination
- enterprise-ai
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Governance Gaps in Agent Interoperability Protocols: What MCP, A2A, and ACP Cannot Express

## Summary
This paper argues that MCP, A2A, ACP, ANP, and ERC-8004 support agent coordination but lack protocol-native governance for agent communities. Its main claim is that governance needs a separate architectural layer above current interoperability standards.

## Problem
- Enterprises are deploying heterogeneous agent fleets that can discover tools, exchange messages, delegate tasks, and record trust signals, but these protocols do not define how agents make governed group decisions.
- The missing capabilities matter for regulated or high-risk settings, such as production code changes, compliance review, and research arbitration, where decisions need membership control, deliberation, voting, dissent records, human escalation, and audit.
- Without shared governance primitives, each application must implement its own decision process, which weakens interoperability and audit consistency.

## Approach
- The paper defines a six-part governance taxonomy: G1 membership, G2 deliberation, G3 voting, G4 dissent preservation, G5 human escalation, and G6 audit/replay.
- It evaluates five protocols: MCP v1.1, A2A v1.0.1, ACP, ANP, and ERC-8004.
- Each protocol-dimension pair is classified as Supported, Partial, or Absent based on what the protocol specification encodes, rather than what an application could build on top.
- The authors separate gaps that could be addressed through protocol extensions from gaps that may need a new layer.

## Results
- Across the five protocols and six governance dimensions, no protocol fully supports any governance dimension in the reported matrix.
- Voting, dissent preservation, and human escalation are Absent in all 5/5 protocols.
- Coverage scores are low: MCP v1.1 scores 1/12, A2A v1.0.1 scores 1/12, ACP scores 2/12, ANP scores 0/12, and ERC-8004 scores 2/12.
- Membership is Partial in A2A, ACP, and ERC-8004, but Absent in MCP and ANP.
- Deliberation is Partial only in ACP and Absent in the other 4 protocols.
- Audit/replay is Partial in MCP and ERC-8004, but Absent in A2A, ACP, and ANP; the paper says these partial cases come from session state or blockchain history rather than governance-specific replay semantics.

## Link
- [https://arxiv.org/abs/2606.31498v1](https://arxiv.org/abs/2606.31498v1)
