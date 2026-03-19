---
source: hn
url: https://github.com/arryllopez/meerkat
published_at: '2026-03-05T23:28:54'
authors:
- arryleo10
topics:
- blender-plugin
- real-time-collaboration
- 3d-editing
- websocket-sync
- collaborative-tools
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Show HN: Real-time collaborative editing plugin for Blender

## Summary
Meerkat is a real-time collaborative editing plugin for Blender, aimed at supporting multiple people editing the same scene simultaneously and synchronizing transforms. Through lightweight network synchronization and conflict handling, it attempts to replace the inefficient workflow of manually passing `.blend` files between team members.

## Problem
- Blender lacks built-in real-time collaboration capabilities, so teams usually can only pass `.blend` files back and forth via chat or cloud storage, which easily leads to version confusion and overwriting each other’s work.
- When multiple people edit a 3D scene at the same time, collaboration efficiency is low without low-latency synchronization, conflict handling, and visibility into online presence.
- This problem matters because 3D content creation is often a multi-person workflow, and the lack of real-time collaboration directly slows down creation and review.

## Approach
- The system is divided into two parts: a Rust backend responsible for WebSocket sessions, object ID/transform diff synchronization, and relay logic; and a Python Blender plugin responsible for listening to Blender scene updates and sending/applying remote changes.
- The core mechanism is simple: **it does not transmit full mesh data, only object IDs and transform deltas such as position/rotation/scale**, thereby reducing bandwidth usage and enabling real-time synchronization.
- The plugin hooks into Blender’s depsgraph update handlers to capture local modifications; remote modifications are replayed into the local scene as deltas.
- It supports hosting/joining sessions, peer-to-peer connections on the same LAN, and an optional cloud relay, lowering the deployment barrier for remote collaboration.
- Through conflict resolution, online user visibility, and selection highlighting, it tries to ensure that simultaneous editing does not cause users to overwrite each other’s work.

## Results
- The text **does not provide quantitative experimental results**; it gives no numbers for latency, bandwidth, throughput, user studies, or baseline comparisons with other systems.
- Publicly claimed supported capabilities include: multiplayer scene editing, real-time object transform synchronization, shared sessions, conflict resolution, online member visibility, peer-to-peer mode, and optional cloud relay.
- The text explicitly states that the backend transmits only “object IDs and transforms rather than full mesh data”; its strongest concrete claim is **achieving real-time synchronization with lower bandwidth**, but it provides no specific savings ratio.
- At the code and engineering level, it shows some maturity signals: Rust backend (`tokio` + `axum`), Blender 4.0+ plugin testing, and `cargo test`/`clippy` support, but the project is still in the **Alpha dropping soon / not yet released** stage.

## Link
- [https://github.com/arryllopez/meerkat](https://github.com/arryllopez/meerkat)
