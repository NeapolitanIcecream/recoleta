---
source: hn
url: https://vouch.sh
published_at: '2026-03-02T23:19:07'
authors:
- jplock
topics:
- developer-credentials
- hardware-authentication
- fido2
- credential-broker
- access-control
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Vouch - Hardward based developer credentials

## Summary
Vouch is a developer credential broker based on FIDO2 hardware verification, using a single physical touch to obtain multiple short-lived, scoped developer credentials. It aims to address the problems of long-lived key sprawl, inability to confirm whether a human is actually present, and AI agents sharing high-privilege human credentials.

## Problem
- Modern developer workflows suffer from **credential sprawl**: SSH keys, long-lived AWS access keys, GitHub PATs, and similar credentials are often long-lived, stored in scattered locations, and difficult to govern centrally.
- Existing MFA often verifies only devices and **cannot confirm that a real human is present**; once a laptop or cached credentials are compromised, an attacker may be treated as the legitimate user.
- AI coding assistants often directly inherit developer credentials, creating problems of **excessive privilege, lack of scope restriction, and difficult auditing**, while also making it hard to distinguish whether an action was performed by a human or an agent.

## Approach
- The core mechanism is simple: the user first **touches a FIDO2 hardware security key** and completes a hardware-level verification with a PIN, proving that a real human is present.
- Vouch then acts as a **credential broker** that issues **short-lived, scoped, hardware-attested, device-bound** credentials for different tools, instead of requiring users to keep long-lived static secrets.
- It can issue multiple types of native credentials, including **SSH certificates, AWS sessions, GitHub tokens, Kubernetes configs**, and integrates natively with SSH, AWS CLI, git, kubectl, docker, cargo, and more, with no extra wrapper required.
- For AI agents, Vouch provides **scope-limited, time-limited** credentials, and claims it can use cryptographic audit trails to distinguish **human actions** from **agent actions**, with support for rapid revocation.
- The system emphasizes **auditability and open source**: the CLI and agent use Apache-2.0/MIT, the server-side code is under BSL 1.1, and converts to Apache-2.0 after 2 years.

## Results
- The text **does not provide standard academic experiments, benchmark data, or quantitative metrics**, so there are no reportable numbers for accuracy, success rate, throughput, or security evaluation.
- The strongest concrete capability claim is that, after **a single FIDO2 hardware verification**, a user can obtain multiple kinds of developer credentials for the span of “**all day**.”
- The explicitly covered credentials/systems include **SSH, AWS, GitHub, Kubernetes**, with native integrations for **AWS CLI, git, kubectl, docker, cargo, CodeArtifact, CodeCommit**, and others.
- The core security claims are that credentials are **short-lived**, **scoped**, **hardware-attested**, and **device-bound**, and that AI agent credentials can be **revoked instantly** with **human/agent-distinguishable auditing**.
- The specific open-source and auditability claims are that the **CLI and agent are open source**, the **server source is visible**, and the server license converts to Apache-2.0 **after 2 years**.

## Link
- [https://vouch.sh](https://vouch.sh)
