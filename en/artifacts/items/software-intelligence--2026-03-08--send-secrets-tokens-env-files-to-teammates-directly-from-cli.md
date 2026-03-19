---
source: hn
url: https://github.com/rel-s/stringphone
published_at: '2026-03-08T22:54:26'
authors:
- rel0s
topics:
- cli-security
- end-to-end-encryption
- secret-sharing
- developer-tooling
- metadata-privacy
relevance_score: 0.39
run_id: materialize-outputs
language_code: en
---

# Send secrets/tokens/env-files to teammates directly from CLI

## Summary
stringphone is a command-line tool that uses existing SSH ed25519 keys to send messages, secrets, and small files directly to teammates from the terminal, reducing leakage risk through end-to-end encryption and short-lived relay storage. It emphasizes metadata blinding and a minimalist CLI experience, making temporary sharing of sensitive information more convenient.

## Problem
- It addresses the problem of securely transferring secrets, tokens, env files, and small configuration files in team CLI/development workflows; traditional chat, email, or manual copy-paste is more likely to leak information or leave long-term traces.
- Encrypting content alone is not enough. If the server can identify the communicating parties, message routing, or retain data long-term, it still exposes sensitive collaboration relationships and operational traces.
- Developers need a solution with თითქმის zero additional infrastructure that can directly reuse existing SSH keys; otherwise, security tools often go unused because the adoption barrier is too high.

## Approach
- The core mechanism is simple: each side uses its own SSH ed25519 key and the other party's public key to perform X25519 Diffie-Hellman, independently deriving the same shared secret without transmitting private keys.
- It then generates a directional mailbox ID with `mailbox_id = BLAKE3(shared_secret || sender_pubkey || recipient_pubkey)`, so `alice→bob` and `bob→alice` are different; because the mailbox ID includes the shared secret, a third party cannot easily infer routing even if both public keys are known.
- For message encryption, HKDF-SHA256 derives a direction-bound encryption key from the shared secret, then ChaCha20-Poly1305 encrypts `[timestamp][plaintext]`, providing confidentiality and integrity protection.
- To resist replay, the client records recently seen message hashes and checks timestamps, rejecting old and duplicate messages; the server sees only opaque mailbox IDs, ciphertext, time, size, and IP.
- Engineering-wise, it provides a minimalist CLI: supports `pair`, auto-detects send/recv, imports public keys from GitHub, uses an online relay by default, with a default message limit of 5 KiB and TTL of 5 minutes.

## Results
- The text does not provide standard benchmark tests, public datasets, or quantitative comparison results against other tools.
- The explicitly stated system parameters include: default maximum message size of **5 KiB** and default server retention time of **5 minutes**.
- Total protocol-layer message overhead is **37 bytes**, consisting of **1-byte version + 12-byte nonce + 8-byte timestamp + 16-byte auth tag**; the ciphertext length seen by the server is approximately plaintext length + **29 bytes**.
- The shared secret length is **32 bytes**; the mailbox ID is **64 hexadecimal characters**; message authentication relies on Poly1305's **16-byte** tag.
- The specific verifiable security claims are that the server **cannot read message contents**, **cannot directly identify participants**, **cannot determine who is talking to whom**, and that messages are **ephemerally stored** and **end-to-end encrypted**.
- The practical usability claim is that it directly reuses existing **SSH ed25519** keys without extra authentication headers; if a user has only RSA/ECDSA, the current scheme **does not support** them, and an ed25519 key must be generated separately.

## Link
- [https://github.com/rel-s/stringphone](https://github.com/rel-s/stringphone)
