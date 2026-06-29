---
source: hn
url: https://devfortress.net/blog/semi-annual-2026
published_at: '2026-06-28T23:48:55'
authors:
- arian_
topics:
- ai-agent-security
- credential-management
- software-supply-chain
- mcp-security
- non-human-identity
- code-intelligence
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# AI Agent Credential Crisis: Six Months of Incidents

## Summary
The paper argues that AI agents and developer tools keep exposing real, reusable credentials, and that current security products mostly react after those credentials exist. It proposes DevFortress and token-aliased closed-loop security as a way to keep real secrets out of exposed execution paths.

## Problem
- AI agents, MCP servers, CI/CD tools, IDE plugins, and cloud integrations often run with real API keys, OAuth tokens, session tokens, or build credentials available in files, environment variables, local machines, or runtime contexts.
- The risk matters because agents can search code, invoke tools, and call APIs faster than humans, so one unscoped or leaked credential can delete data, exfiltrate secrets, or compromise supply chains.
- Existing governance, scanning, rotation, and audit products reduce risk after credential creation, but the paper says they do not remove the directly usable credential from the place an attacker or agent can reach.

## Approach
- The core mechanism is credential aliasing: exposed systems receive an alias or isolated identifier, while the real credential stays inside controlled infrastructure.
- DevFortress monitors application, API, and agent sessions for brute force, credential stuffing, token replay, privilege escalation, anomalous request volume, scope deviation, and suspicious machine-to-machine traffic.
- When behavior crosses a policy boundary, the system claims it can revoke sessions, block IPs, or quarantine an agent in under two seconds while keeping an audit trail.
- For API and agent use, the paper describes scoped credentials, payload signing, zero-downtime key rotation, HMAC-SHA256 signed webhooks, timestamp validation, anti-replay controls, and SIEM export.
- The paper positions this as a design change: reduce the blast radius by preventing real credentials from being present at integration and agent execution boundaries.

## Results
- GitGuardian data cited in the paper reports 28,649,024 new secrets exposed on public GitHub in 2025, up 34% year over year; AI-service credentials rose 81.5%.
- GitGuardian also reports that 64% of credentials leaked in 2022 were still active and exploitable in January 2026, and 24,008 unique secrets were found in MCP configuration files.
- The OX Security MCP disclosure is cited as affecting 200,000+ vulnerable instances, 10+ CVEs, and 150 million+ downloads across tools including LiteLLM, LangChain, LangFlow, Flowise, Windsurf, and Cursor.
- The LiteLLM supply-chain compromise is cited as exposing credentials from about 47,000 downloads during a roughly 40-minute PyPI window.
- The PocketOS incident is cited as a Cursor agent deleting a production database in 9 seconds after finding an unscoped Railway CLI token; the most recent recoverable backup was 3 months old.
- The excerpt gives many incident metrics and product claims, but it does not provide a controlled benchmark, ablation, false-positive rate, latency distribution, or third-party evaluation for DevFortress itself.

## Link
- [https://devfortress.net/blog/semi-annual-2026](https://devfortress.net/blog/semi-annual-2026)
