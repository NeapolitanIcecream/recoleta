---
source: hn
url: https://github.com/fbongiovanni29/ipfs-oci-registry
published_at: '2026-03-08T23:45:56'
authors:
- noobernetes
topics:
- container-registry
- ipfs
- oci-images
- p2p-distribution
- federation
relevance_score: 0.36
run_id: materialize-outputs
language_code: en
---

# IPFS OCI Registry – now with federation policy and private swarm support

## Summary
This is a decentralized OCI container image registry based on IPFS, supporting federated sharing, pull-through proxy caching, private swarms, and policy-based image sharing. The project has been archived; its greatest value lies in validating that the architecture was feasible, while benchmark testing also showed that IPFS is not suitable as a transport layer for container images at scale.

## Problem
- The work aims to solve the **bottlenecks caused by centralized container registries**: such as Docker Hub rate limits, cloud vendor lock-in, repeated cross-region transfers, and complex image synchronization in isolated environments.
- This matters because container images are foundational infrastructure for modern software delivery; if distribution depends on centralized services, cost, availability, and deployment flexibility are all constrained.
- It also attempts to solve the problem of **automatic shared caching across organizations/regions**, with the goal of making images “pull once, available everywhere,” reducing repeated downloads and operational coordination.

## Approach
- The core method is simple: turn the OCI registry into a **pull-through proxy + IPFS caching layer**. After an image is first pulled from upstream sources such as Docker Hub/GHCR, the blobs are stored in IPFS and a digest→CID mapping is recorded; other nodes can then fetch directly from IPFS.
- It uses **SHA256 digests to verify content**, so there is no need to trust the source node, only the hash; if the bytes do not match, the content is rejected.
- Through a **federation mechanism**, nodes broadcast and query digest→CID mappings: if a lookup misses locally, the node first asks IPFS peers, and only then decides whether to fall back to the upstream registry.
- It uses **federation policy + private-by-default** to control the sharing scope: proprietary images are not shared by default, and only explicitly marked ones (such as `public/`) are propagated in the federation; it also supports private IPFS swarms where only internal enterprise nodes peer with each other.
- From an engineering perspective, it provides deployable capabilities including Helm, fully decentralized DaemonSet mode, health checks, authentication, rate limiting, GC, stale-while-revalidate, Prometheus metrics, and more.

## Results
- The author claims the system is complete and usable: it supports pull-through proxying for **7 upstream registries**, exposes **18 custom Prometheus metrics**, and includes **60+ tests** covering storage, processors, health checks, authentication, rate limiting, TTL, metrics, configuration, and upstream clients.
- The key experimental conclusion is that **for real-world images, IPFS is 3–12x slower than a CDN**; only in **very small image** scenarios might IPFS perform better because network round trips dominate.
- The author explicitly states that the performance bottleneck comes from IPFS Bitswap: it exchanges data in **256KB blocks** and incurs per-block negotiation overhead; this mechanism is suitable for DAG traversal, but not for sequential streaming of large files.
- The work does not provide more fine-grained public benchmark tables (such as specific throughput/latency/data set details), but its strongest quantitative claim is **“real images 3–12x slower than a CDN.”**
- The real “breakthrough” in the conclusion is not outperforming existing solutions, but rather the **negative result**: it shows that “IPFS as a transport layer for container image distribution” is the wrong direction for scaled deployment scenarios, while preserving a registry/federation architecture that can be migrated; the author further suggests that **BitTorrent + DHT** may be a more suitable alternative.

## Link
- [https://github.com/fbongiovanni29/ipfs-oci-registry](https://github.com/fbongiovanni29/ipfs-oci-registry)
