---
source: hn
url: https://github.com/rel-s/stringphone
published_at: '2026-03-08T22:54:26'
authors:
- rel0s
topics:
- cli-security
- end-to-end-encryption
- secure-messaging
- ssh-keys
- metadata-blind-relay
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Send secrets/tokens/env-files to teammates directly from CLI

## Summary
This work introduces **stringphone**: a command-line tool that uses existing SSH ed25519 keys to send messages, secrets, and small files directly to teammates from the terminal. It emphasizes end-to-end encryption, short-lived storage, and a “metadata-blind” relay, so the server is responsible for little more than forwarding ciphertext.

## Problem
- The problem it addresses is that developers need a simple way to **send secrets/tokens/env files directly from the CLI** to teammates without relying on chat software, manual encryption, or long-term storage services.
- This matters because credentials and configuration files are often sensitive; if a server can read the contents, identify the communicating parties, or retain data long-term, it creates leakage and operational risk.
- In existing terminal workflows, secure transfer often requires extra key or infrastructure management, leading to higher friction and a less smooth process.

## Approach
- The core mechanism is simple: both parties use their **existing SSH ed25519 keys** to independently derive the same shared key via **X25519 Diffie-Hellman**, without transmitting private keys.
- Based on that shared key, it then uses **BLAKE3** to generate direction-specific mailbox IDs, **HKDF-SHA256** to derive encryption keys, and **ChaCha20-Poly1305** to protect message confidentiality and integrity.
- The relay server only sees **opaque mailbox IDs and ciphertext**; because the mailbox ID incorporates the DH shared secret, even if both public keys are known, it is still difficult for a third party to infer the communication mailbox, reducing participant linkage and overwrite risk.
- Messages are **ephemeral**: the default maximum is 5 KiB with a TTL of 5 minutes; the client stores hashes of seen messages and checks timestamps to resist replay attacks.
- The interaction is designed as a Unix-style CLI: it supports `pair` for pairing, automatically decides send/receive based on stdin, and can import the other party’s ed25519 key from GitHub public keys.

## Results
- The text **does not provide formal paper-style quantitative experiments**: there are no benchmarks, datasets, success rates, or numerical comparisons against baselines.
- The most concrete stated results/capabilities include: the server default **maximum message size of 5 KiB**, and messages are retained on the server for a default **TTL of 5 minutes**.
- The protocol overhead is explicitly given as **37 bytes per message** (1-byte version + 12-byte nonce + 8-byte timestamp + 16-byte authentication tag).
- The mailbox ID is a **64-character hexadecimal string**, and server responses include status codes such as **201 / 413 / 429 / 400** to indicate successful write, too large, mailbox full, or bad ID.
- The claimed breakthrough is not an accuracy metric but the combination of security and usability: the **server cannot read messages, cannot identify participants, and cannot determine who is talking to whom**, while directly reusing existing SSH ed25519 identities.

## Link
- [https://github.com/rel-s/stringphone](https://github.com/rel-s/stringphone)
