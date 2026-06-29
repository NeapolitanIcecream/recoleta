---
source: hn
url: https://github.com/Commonguy25/authproof-sdk
published_at: '2026-04-06T23:18:12'
authors:
- Commomguy
topics:
- agent-authentication
- delegation-protocols
- ai-agent-security
- auditability
- human-ai-interaction
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Cryptographic delegation receipts to close the user-to-operator agent trust gap

## Summary
AuthProof proposes a cryptographic delegation receipt that records what a user actually authorized before an operator sends instructions to an AI agent. The goal is to make operator changes, scope violations, and unauthorized actions detectable with signed receipts, append-only logs, and per-action audit records.

## Problem
- Current IETF agent identity work named in the paper, including AIP, draft-klrc-aiagent-auth, and WIMSE, covers service-to-agent authorization but does not give the user a cryptographic record of their original intent.
- In the chain User → Operator → Agent → Services, the operator can expand, change, or drop instructions before they reach the agent, and the user cannot later prove what they approved.
- That gap matters for audit, compliance, dispute resolution, and agent safety because agents and services lack a signed source of truth for user-approved scope and hard limits.

## Approach
- The core mechanism is a signed Delegation Receipt created by the user with WebAuthn/FIDO2 hardware-backed keys and anchored to an append-only log before any agent action starts.
- The receipt contains a structured allowlist of permitted operations, explicit non-overridable prohibitions, a validity window checked against log time, and a hash of the operator's instruction text at delegation time.
- For executable actions, the receipt points to the hash of a Safescript program's static capability DAG, so a different program cannot be swapped in after approval if the hash does not match.
- Tool servers can publish signed capability manifests, and the receipt references the manifest hash rather than an operator-provided schema, which gives a check on tool description drift.
- Every agent action references the receipt hash and is written to a signed chained Action Log; if an action falls outside scope, the system requires a new user-signed micro-receipt for that specific action.

## Results
- The excerpt does not report benchmark results, formal evaluation metrics, or dataset comparisons against baselines.
- The paper claims a user can prove what they authorized because the receipt is signed and logged before any agent action, and any later mismatch with operator instructions is detectable by comparing hashes.
- The paper claims out-of-scope actions are cryptographically invalid when validated against the receipt, with deny-by-default scope and explicit boundaries such as blocking `deletes` or access to `payment-methods`.
- The Action Log uses SHA-256 links between entries and supports `diff()` to compare authorized scope against recorded actions; the example shows 2 compliant entries and then 1 violation for `Send email` with `0% scope match` and `92% boundary overlap`.
- The paper also states an implementation limitation: v1 timestamps use the client clock, and production compliance deployments should replace this with an RFC 3161 trusted timestamp authority.

## Link
- [https://github.com/Commonguy25/authproof-sdk](https://github.com/Commonguy25/authproof-sdk)
