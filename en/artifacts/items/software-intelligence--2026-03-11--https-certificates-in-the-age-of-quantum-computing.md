---
source: hn
url: https://lwn.net/SubscriberLink/1060941/4878284e2c9f19ba/
published_at: '2026-03-11T23:11:17'
authors:
- firexcy
topics:
- post-quantum-cryptography
- https-certificates
- pki
- certificate-transparency
- merkle-trees
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# HTTPS certificates in the age of quantum computing

## Summary
This article discusses how the IETF's new working group, PLANTS, aims to introduce post-quantum cryptography for HTTPS authentication and certificate transparency while avoiding certificates becoming unacceptably large due to post-quantum signatures. The core idea is to change certificates from a "signature chain" to "log proofs + observer signatures", and to use Merkle trees to significantly compress certificate size for most connections.

## Problem
- Existing HTTPS post-quantum efforts have mainly focused on key exchange first, but authentication and certificate transparency also need to migrate; otherwise, the Web PKI in the future quantum era will still be constrained.
- Post-quantum signatures are very large: the article states that ML-DSA-44 signatures are about **37 times** the size of Ed25519 signatures, and a direct replacement would make certificate chains roughly **40 times** their current size, increasing bandwidth usage and connection latency.
- Traditional certificate chains and certificate-transparency logs contain redundant information; if the current structure is kept, switching to post-quantum authentication could make certificate overhead for small websites exceed the page content itself.

## Approach
- PLANTS proposes that each CA maintain its own **append-only issuance log**, with third-party observers/mirrors monitoring whether it is truly append-only and signing log checkpoints.
- Browsers would no longer primarily rely on the "signature chain from the site to the root CA", but instead verify: **signatures from the CA/observers over the log state + proof that the server certificate is included in the log**.
- To reduce per-site transmission costs, the system distinguishes between two types of certificates: clients connecting for the first time or not yet synchronized receive a larger **full certificate**; clients that have already seen a checkpoint need only receive a smaller **signatureless certificate**.
- The signatureless certificate relies on a **Merkle-tree inclusion proof**: the CA places many certificates into a tree in batches and signs the root only once; an individual site sends only the small set of hash paths from leaf to root to prove its certificate has been issued.
- Because the size of hash proofs grows only **logarithmically** with tree size, and hashes are not subject to the same quantum-driven size inflation as public-key signatures, this design is especially beneficial for post-quantum certificates.

## Results
- LWN's current traditional certificate chain is about **3.5KB**, already roughly **one third** of the compressed HTML content of its front page; this shows certificate size is already non-negligible.
- The article says that with ML-DSA-44, a single signature is about **37 times** the size of Ed25519; directly switching to post-quantum certificates would make the overall certificate chain nearly **40 times** larger.
- Using Let's Encrypt's issuance of about **6 million certificates per day** and one checkpoint every **1 minute** as an example, the Merkle inclusion proof for a single site would require only **12 SHA-256 hashes**, for a total of **384 bytes**.
- These **384 bytes** are only **16%** of the size of a single ML-DSA-44 signature, showing that the "signatureless certificate" can significantly reduce the average transmission cost of post-quantum authentication.
- For clients without a cached checkpoint, the full certificate is still very large: the article estimates about **133KB** when using ML-DSA-44, clearly much larger than current certificates, though ideally it would be used only for a minority of connections.
- There are not yet any publicly available large-scale performance results for this scheme; the strongest concrete implementation signal at present is that **Google plans to experiment with and deploy a post-quantum CA system based on the PLANTS draft in Chrome by the end of 2027**, while widespread configuration updates may not arrive until **2029–2030**.

## Link
- [https://lwn.net/SubscriberLink/1060941/4878284e2c9f19ba/](https://lwn.net/SubscriberLink/1060941/4878284e2c9f19ba/)
