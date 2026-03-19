---
source: hn
url: https://icebergmap.com/
published_at: '2026-03-07T23:45:19'
authors:
- aosmith
topics:
- p2p-networking
- webrtc
- anonymous-reporting
- privacy-preserving
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: Iceberg Map

## Summary
Iceberg Map is a browser-based peer-to-peer anonymous sighting report network that emphasizes no accounts, no servers, and no tracking. It is primarily a privacy-first WebRTC application, rather than a research paper on robotics or foundation models.

## Problem
- It attempts to solve the problem of **centralized dependence** in anonymous event/sighting reporting: traditional platforms usually require accounts, servers, and logs, creating risks of censorship, single points of failure, and privacy leakage.
- It attempts to solve the problem of **user traceability**: if a reporting system collects identity, device, or network metadata, anonymity is weakened.
- This matters because in reporting scenarios involving sensitive events, users often care most about privacy protection, censorship resistance, and minimizing trust assumptions.

## Approach
- The core mechanism is simple: enable browsers to **communicate directly**, using WebRTC to share reports among peers instead of sending them first to a central server.
- The system design principles are **no accounts, no servers, no tracking**, minimizing identity binding and centralized data retention at the product level.
- The page shows network-layer metrics such as connected peers, sightings received/sent, syncs completed, dedup cache, and blocked connections, indicating that it uses **P2P synchronization and deduplication** mechanisms.
- It explicitly states "**No data passes through a central server**" and "**No identifying information is collected or transmitted**"; its anonymity mainly relies on decentralized transmission and minimal data collection.

## Results
- The provided content includes **no paper-style quantitative experimental results**: there are no datasets, baseline methods, accuracy, latency, throughput, or anonymity evaluation metrics.
- The only visible numbers are product page status values: the version is **v0.1.0**, and in the example interface **Connected Peers = 0**, **Sightings Received = 0**, **Sightings Sent = 0**, and **Syncs Completed = 0**; these are not performance results.
- The strongest specific claim is that **all connections are established directly peer-to-peer via WebRTC**, and **no data passes through a central server**.
- Another core claim is that it uses **no accounts** and **does not collect or transmit identifying information**, so the goal is to enable anonymous reporting.

## Link
- [https://icebergmap.com/](https://icebergmap.com/)
