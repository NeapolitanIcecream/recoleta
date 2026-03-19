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
- decentralized-systems
relevance_score: 0.15
run_id: materialize-outputs
language_code: en
---

# Show HN: Iceberg Map

## Summary
Iceberg Map is a browser-based peer-to-peer anonymous sighting report network that emphasizes **no accounts, no servers, no tracking**. It propagates reports directly between browsers via WebRTC, aiming to provide a more private and decentralized way to share information.

## Problem
- Existing reporting/map systems usually rely on centralized servers, creating risks of **single-point control, censorship, log retention, and privacy leakage**.
- Users submitting sensitive sighting information are often required to register accounts or expose traceable metadata, which reduces willingness to participate.
- There is a need for an anonymous sharing mechanism that **does not require trust in a central platform** and can run directly in ordinary browsers.

## Approach
- Use **WebRTC** to establish **direct peer-to-peer connections** between browsers so data is not relayed through a central server.
- The system’s design principle is **no accounts, no servers, no tracking**, meaning it does not require identity registration and does not collect or transmit personally identifiable information.
- Synchronize “sighting reports” across browser nodes through a peer network, with each user’s browser acting as both a client and a network participant.
- The interface displays network operating metrics such as connected peers, reports received/sent, sync count, dedup cache, and blocked connections, indicating that its core is a lightweight P2P synchronization network.

## Results
- The provided text contains **no paper-style quantitative experimental results**; it does not provide datasets, baseline methods, accuracy, latency, throughput, or anonymity evaluation figures.
- The strongest concrete implementation claim is: **all connections are established directly peer-to-peer via WebRTC, and no data passes through a central server**.
- The prototype page shows the system version as **v0.1.0** and uses the **AGPL-3.0** license, indicating this is an early working prototype rather than a mature, evaluated research system.
- The page lists observable operating metrics (such as Connected Peers, Sightings Received/Sent, Syncs Completed, Dedup Cache), but in the excerpt the corresponding values are mostly **0 or disconnected state**, so they cannot be used to demonstrate actual performance gains.

## Link
- [https://icebergmap.com/](https://icebergmap.com/)
