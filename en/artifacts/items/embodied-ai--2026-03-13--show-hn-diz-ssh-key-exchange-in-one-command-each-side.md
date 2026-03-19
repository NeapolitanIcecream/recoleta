---
source: hn
url: https://github.com/noahra/diz
published_at: '2026-03-13T23:29:38'
authors:
- noahra
topics:
- ssh
- key-exchange
- secure-onboarding
- tls-pinning
- developer-tools
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: diz – SSH key exchange in one command each side

## Summary
diz is a small tool for **initial SSH key exchange**: each side runs one command, shares a short code out of band, and can establish authenticated SSH access. It focuses on the narrow scenario where “you can run commands on both machines, but do not want to manually copy public keys or enable password authentication.”

## Problem
- It addresses the cumbersome process of establishing trust for SSH the first time: the traditional approach often requires manually copying public keys and editing `authorized_keys`, which is error-prone and inconvenient.
- This matters because many real-world scenarios only need a one-time, fast, secure way to place your SSH public key onto a target machine, rather than setting up a long-term complex solution.
- It is especially aimed at cases where both sides can run commands, a short code can be shared out of band via chat/voice/etc., but no one wants to deal with pasting a 70+ character public key.

## Approach
- The core mechanism is simple: the target machine runs `diz --listen`, the local machine runs `diz --connect <code>`, and the short code contains the information needed for a secure first connection.
- The short code encodes the IP, port, one-time token, and TLS certificate fingerprint, so the connection is encrypted from the start and protected against MITM through certificate fingerprint pinning.
- After establishing a temporary authenticated channel, `diz` automatically exchanges the user's public key, adds it to the target machine's `authorized_keys`, and then drops directly into a shell.
- By design it is single-use and short-lived: each session generates a one-time certificate, uses a 128-bit one-time token, keeps no persistent listener, and does not depend on a central server/relay.
- Across networks, it does not perform NAT traversal itself; it is intended to be paired with VPNs such as Tailscale, ZeroTier, or WireGuard, working the same way within the same virtual network.

## Results
- The text **does not provide formal experiments, benchmarks, or quantitative evaluation results**, so there are no accuracy, throughput, latency, or baseline comparison numbers to report.
- The strongest concrete functionality claim is that **one command on each side** is enough to complete the initial SSH key exchange and drop directly into a shell, simplifying the process compared with manually copying public keys or editing `authorized_keys`.
- Specific security-related claims include the use of **TLS + certificate fingerprint pinning**, with the fingerprint embedded in the share code; if tampering occurs, the connection is aborted immediately.
- Sessions use a **one-time 128-bit token**, and there is **no persistent listener and no central server/relay**, emphasizing a short-lived, single-use initial access model.
- The boundaries of applicability are also clearly stated: it is **not suitable** for high-security production servers, environments where the share code cannot be verified out of band, or scenarios where both machines are behind aggressive NAT without a VPN.

## Link
- [https://github.com/noahra/diz](https://github.com/noahra/diz)
