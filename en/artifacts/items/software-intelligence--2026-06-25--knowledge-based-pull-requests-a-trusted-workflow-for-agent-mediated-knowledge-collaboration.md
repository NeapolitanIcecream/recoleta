---
source: arxiv
url: https://arxiv.org/abs/2606.26721v1
published_at: '2026-06-25T07:57:33'
authors:
- Xinyu Zhang
- Weiwei Sun
topics:
- code-intelligence
- software-agents
- pull-requests
- human-ai-interaction
- software-governance
- multi-agent-software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Knowledge-Based Pull Requests: A Trusted Workflow for Agent-Mediated Knowledge Collaboration

## Summary
KPR changes a cross-boundary PR into a knowledge handoff: external code, tests, and cleaned agent traces become evidence, then project-owned agents regenerate code inside the target repository. The paper is a workflow proposal with a small simulation pilot, so its main claim concerns governance and review control, with no measured productivity gain in the excerpt.

## Problem
- Agent-generated PRs can make code cheap while leaving maintainers with harder work: intent, scope, architecture fit, security policy, and long-term ownership.
- Traditional PRs let an external patch cross the trust boundary as the merge candidate, which is risky for open source, enterprise, vendor, contractor, and customer-submitted changes.
- Raw agent chats are too noisy and may contain stale claims, secrets, irrelevant trials, or untrusted instructions, so dumping traces into review does not solve reviewer load.

## Approach
- An external collaborator uses a local coding agent to explore a change, create code, run tests, and collect evidence.
- An extraction agent turns the local diff, tests, logs, cleaned trace, failed attempts, and human corrections into a structured KPR package with provenance for claims.
- A transformation agent renders that package into reviewer-facing artifacts such as a brief, design memo, risk checklist, test plan, or implementation brief.
- The collaborator confirms the package before submission, and project reviewers approve, reject, or request clarification on the knowledge before any code merge path starts.
- A project-owned inner trusted coding agent regenerates candidate code inside the receiving repository under project context, tests, conventions, and security policy; humans still review and decide merge.

## Results
- The pilot covers 7 merged public PRs and shows that KPR packages can be built from real PR material.
- The pilot stress-tests packages under 3 conditions: description ablation, diff ablation, and synthetic poisoned-patch conditions.
- The paper does not report a measured reduction in review time, merge latency, defect rate, or maintainer workload.
- The paper cites Njoku et al.'s study of 40,214 PRs across 2,807 repositories, including 33,596 agent-authored PRs, as evidence that agent PRs already affect integration outcomes.
- It also cites SWE-chat with about 6,000 coding-agent sessions, where 44% of agent-produced code survived into user commits and users pushed back in 44% of turns, supporting the claim that traces contain useful review evidence beyond the final diff.

## Link
- [https://arxiv.org/abs/2606.26721v1](https://arxiv.org/abs/2606.26721v1)
