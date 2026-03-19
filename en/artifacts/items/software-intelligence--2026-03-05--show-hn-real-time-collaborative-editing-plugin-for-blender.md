---
source: hn
url: https://github.com/arryllopez/meerkat
published_at: '2026-03-05T23:28:54'
authors:
- arryleo10
topics:
- blender-plugin
- real-time-collaboration
- 3d-scene-editing
- websocket-sync
- collaborative-software
relevance_score: 0.54
run_id: materialize-outputs
language_code: en
---

# Show HN: Real-time collaborative editing plugin for Blender

## Summary
Meerkat is a real-time collaborative editing plugin for Blender, aimed at allowing multiple people to edit the same scene simultaneously and synchronize transforms. It replaces manually passing around `.blend` files with lightweight network synchronization, attempting to reduce version conflicts and overwrite risks in team collaboration.

## Problem
- Blender **lacks built-in real-time collaboration**, so teams typically rely on chat or cloud storage to pass around `.blend` files, which can easily lead to version divergence and accidental overwrites.
- When multiple people edit a 3D scene together, **changes to object position/rotation/scale cannot be shared instantly**, reducing collaboration efficiency.
- Remote collaboration also faces network access issues, so the system needs to support both **LAN direct connections and cloud relay**.

## Approach
- The system is split into two parts: a **Rust backend** and a **Python Blender plugin**; the former handles WebSocket sessions, object ID/transform diffs, and relay logic, while the latter captures local changes inside Blender and applies remote updates.
- The core mechanism is to **synchronize only object IDs and transform deltas**, rather than full mesh data, in order to minimize bandwidth usage.
- The plugin uses Blender’s **depsgraph update handlers** to monitor scene changes and broadcasts local object translation, rotation, and scale changes to other users in the session.
- It supports **shared sessions, multiplayer scene editing, presence indicators, colored selection highlighting**, and provides **conflict handling** to reduce overwrite issues during simultaneous editing.
- At the network layer, it provides both **peer-to-peer connections** (no relay needed on the same network) and an **optional cloud relay** (no port forwarding required for remote teams).

## Results
- The text **does not provide formal quantitative experimental results**, nor does it include benchmark datasets, latency, throughput, bandwidth, or user study metrics.
- The stated functional outcomes include: **multiple users editing the same Blender scene simultaneously**, **real-time synchronization of object position/rotation/scale**, **session host/join**, **conflict handling**, and **display of user presence and selection state**.
- The engineering implementation specifies a clear technical stack and environment: **Rust 1.75+ , Python 3.10+, Blender 4.0+**; the backend uses **tokio + axum + WebSocket**.
- The strongest specific claimed benefit is that by **transmitting only object IDs and transforms** rather than full meshes, it achieves **lower bandwidth overhead**; however, the text **does not provide concrete numerical comparisons**.
- The current status is **Alpha coming soon**, so the result is closer to an early system prototype showcase than a fully evaluated research breakthrough.

## Link
- [https://github.com/arryllopez/meerkat](https://github.com/arryllopez/meerkat)
