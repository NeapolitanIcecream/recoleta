---
source: hn
url: https://github.com/xlmnxp/qanah
published_at: '2026-03-07T22:36:49'
authors:
- xlmnxp
topics:
- p2p-vpn
- webrtc
- wireguard-compatible
- nat-traversal
- mesh-networking
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Qanah: Peer‑to‑peer VPN over WebRTC with WireGuard configs

## Summary
Qanah is a peer-to-peer VPN tool: it reuses WireGuard-style configuration, but instead of using WireGuard's UDP transport, it encrypts IP packets and sends them through WebRTC data channels. Its core value is that it can still establish encrypted tunnels without a centralized VPN server in environments such as CGNAT, restricted networks, or where opening ports is not possible.

## Problem
- Traditional WireGuard relies on UDP transport and often requires a public IP, port forwarding, or control over the upstream network; in **CGNAT**, enterprise networks, or censored networks, these conditions are often not met.
- When the WireGuard protocol or outbound UDP is blocked, conventional VPNs are difficult to connect, making remote access, site-to-site connectivity, and temporary secure links costly to deploy.
- Small teams or individual users often do not want to maintain a centralized VPN server, but still need multi-node interconnection, basic routing, and encrypted communication.

## Approach
- Qanah reads standard **WireGuard `.conf`** files, extracts the interface address, private key, public key, and `AllowedIPs`, and creates a local **TUN** device accordingly, allowing users to keep using the familiar WireGuard configuration style.
- It uses the local **X25519 private key** and the peer's **public key** to derive a shared key, then derives separate tunnel encryption keys and signaling keys; actual packets are encrypted with **ChaCha20-Poly1305**.
- Unlike traditional WireGuard, it does not directly send UDP VPN packets. Instead, it encrypts raw **IP packets** read from the TUN device and forwards them bidirectionally over a **WebRTC data channel** (label `vpn-tunnel`).
- To solve NAT traversal, it establishes WebRTC connections via **ICE/STUN/TURN**; by default it uses **MQTT** to automatically exchange offer/answer signaling, and it also supports manual copy-paste signaling.
- It supports configuration-based **mesh networking**; if there is no direct route to a destination, it can encapsulate traffic and have the “first connected node” perform a **single-hop relay**, or disable relaying with `--no-relay`.

## Results
- The text **does not provide formal benchmark experiments or paper-style quantitative metrics**; there are no throughput, latency, success-rate, or numerical comparisons with WireGuard/OpenVPN/Tailscale.
- The most concrete functional result given is that, in an example with **3 peers**, nodes can automatically discover each other via MQTT and establish direct WebRTC connections, after which they can `ping` each other's IPv4 addresses `10.0.0.1/2/3` and IPv6 addresses `fd00::1/2/3`.
- The project claims that it enables remote access to a home lab, NAS, or development machine behind **CGNAT**, with **no public IP, no port forwarding, and no central VPN server required**; this is a practical deployment breakthrough, but no numerical validation is provided.
- It claims to still work in networks where **WireGuard/UDP is blocked** or where only standard ports and outbound HTTPS/MQTT are allowed, because the tunnel transport is switched to **WebRTC/ICE**; however, it does not provide success rates or statistics on network-environment coverage.
- It supports **multi-peer mesh** and **1-hop relay**, meaning that when a target is offline or lacks a direct connection, traffic may still reach it through an intermediate node; however, no routing-overhead or relay-performance data is provided.
- The applicable conditions are also fairly clear: it currently requires **Linux**, **TUN device support**, **root/sudo** privileges, and both ends must be able to access at least one common **STUN** server.

## Link
- [https://github.com/xlmnxp/qanah](https://github.com/xlmnxp/qanah)
