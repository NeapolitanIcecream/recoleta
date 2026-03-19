---
source: hn
url: https://github.com/noahra/diz
published_at: '2026-03-13T23:29:38'
authors:
- noahra
topics:
- ssh-key-exchange
- secure-onboarding
- developer-tooling
- remote-access
- tls-pinning
relevance_score: 0.52
run_id: materialize-outputs
language_code: en
---

# Show HN: diz – SSH key exchange in one command each side

## Summary
diz is a lightweight tool for first-time SSH access: each side runs one command and shares a short code to securely complete SSH public key exchange and log in directly. It removes the tedious process of manually copying public keys, editing `authorized_keys`, and temporarily enabling password authentication.

## Problem
- The problem it solves is that when establishing SSH trust between two machines for the first time, the traditional process requires manually copying a 70+ character public key, editing `authorized_keys`, or relying on password login, which is cumbersome and error-prone.
- This matters because developers, operations engineers, and remote collaboration scenarios often need to quickly and securely establish one-time SSH access, while existing methods usually force a tradeoff between usability and security.
- The tool is specifically aimed at the narrow scenario where both sides can run commands and can share a short code through an out-of-band channel; it is not suitable for high-security production environments or situations where the short code cannot be verified out of band.

## Approach
- The core mechanism is very simple: the target machine runs `diz --listen`, and the connecting side runs `diz --connect <code>`. The short code contains the key information needed to establish a secure first connection.
- This short code encodes the IP, port, one-time token, and TLS certificate fingerprint; based on this, the connecting side initiates a temporary authenticated channel and pins the certificate fingerprint from the start to prevent man-in-the-middle attacks.
- After the channel is established, diz automatically exchanges SSH public keys, adds the connecting side's public key to the target machine's `authorized_keys`, and then drops directly into a shell, with no need to manually copy files or modify configuration.
- By design, it is short-lived and single-use: each session generates a one-time certificate, uses a 128-bit one-time token, has no persistent listener, and does not depend on a centralized server or relay.
- At the network layer, it uses the local network IP by default; for cross-location use, it can be paired with VPNs such as Tailscale, ZeroTier, or WireGuard and works the same way on a virtual LAN.

## Results
- The text does not provide standard paper-style quantitative experimental results; it does not give datasets, baselines, success rates, latency, or performance metrics, so a strict numerical comparison cannot be reported.
- The strongest concrete claim is that each side can complete initial SSH authorization with "one command each," replacing the need to manually copy a 70+ character public key and manually edit `authorized_keys`.
- Security claims include: TLS + certificate fingerprint pinning; a one-time certificate generated for each session; a one-time 128-bit token embedded in the short code; and immediate connection abort if the fingerprint does not match.
- Deployment and runtime claims include: no central server/relay required, no persistent listener; works out of the box on the same LAN; and in cross-network scenarios, VPNs such as Tailscale, ZeroTier, and WireGuard can preserve the same usage model.

## Link
- [https://github.com/noahra/diz](https://github.com/noahra/diz)
