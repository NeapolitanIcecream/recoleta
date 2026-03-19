---
source: hn
url: https://github.com/fbongiovanni29/ipfs-oci-registry
published_at: '2026-03-08T23:45:56'
authors:
- noobernetes
topics:
- decentralized-registry
- ipfs
- container-images
- federation
- content-addressing
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# IPFS OCI Registry – now with federation policy and private swarm support

## Summary
This is a decentralized federated system that builds an OCI container image registry on top of IPFS: the first pull fetches from upstream and caches to IPFS, after which federation nodes can reuse and distribute it. The project proved that this architecture is functionally feasible, but benchmarks showed that IPFS is not suitable for large-scale container image transport, so the author has stopped further development.

## Problem
- The target problem is to address bottlenecks caused by centralized container registries, such as Docker Hub rate limits, cloud vendor lock-in, repeated cross-region transfers, and complex image mirroring in offline/air-gapped environments.
- The core idea the author focused on is: if images could self-distribute like content-addressed objects, enterprises or multi-region nodes could reduce dependence on a single central source.
- At the same time, it also tries to solve image sharing and verification across organizations, clouds, and private networks, replacing trust in the source with hash verification.

## Approach
- The core mechanism is simple: turn the registry into a pull-through proxy. Clients pull images by tag or digest; if the image is not available locally, the system first asks IPFS federation nodes, then fetches from upstream sources such as Docker Hub/GHCR, stores the image blobs in IPFS, gets a CID back, and broadcasts it to other nodes.
- The system maintains a digest→CID mapping, queried locally with BoltDB; content is verified via SHA256 digest, and mismatched bytes are rejected, so there is no need to trust the provider, only the hash.
- The federation uses IPFS pubsub to discover “who has this image,” and supports a private-by-default policy: private images are not shared by default, and only explicitly selected content enters federation distribution.
- It adds private swarm support for internal enterprise scenarios, so nodes connect only to the company’s own nodes, allowing image replication across AWS/GCP/Azure/on-prem without traversing the public internet.
- On the engineering side, it implements Helm deployment, a fully decentralized DaemonSet mode, health checks, authentication, rate limiting, Tag TTL, GC, 18 Prometheus metrics, and 60+ tests to validate usability.

## Results
- The author claims to have built a **fully working** system: supporting a pull-through proxy for **7 upstream registries**, IPFS pubsub federation, private swarms, policy controls, a Web UI, and monitoring.
- In terms of test coverage, the project provides **60+ tests** covering storage, handlers, health, auth, rate limiting, tag TTL, metrics, config, and the upstream client.
- The key quantitative conclusion is performance: benchmarks show that **for real-world-scale images, IPFS is 3–12× slower than a CDN**; only for **very small images**, where network round-trip latency dominates, does IPFS have an advantage.
- The reason given by the author is that IPFS Bitswap uses **256KB blocks** and incurs per-block negotiation overhead; this mechanism is suitable for DAG traversal, but not for sequential streaming of large files.
- The strongest “negative result” of the paper/project is: although in theory multi-node seeding could create network effects, when there is only **1 seeder**, there is essentially only “one pipe,” making the result similar to HTTP and preventing positive feedback from scaling.
- The final conclusion is not that the IPFS approach wins, but that the architectural layer (OCI handler, federation policy, digest→content-ID mapping) is valid, while the **transport layer should be replaced with a protocol better suited for large-file distribution, such as BitTorrent+DHT**.

## Link
- [https://github.com/fbongiovanni29/ipfs-oci-registry](https://github.com/fbongiovanni29/ipfs-oci-registry)
