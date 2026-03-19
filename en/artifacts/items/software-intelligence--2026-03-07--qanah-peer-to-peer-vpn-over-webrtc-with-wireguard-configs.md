---
source: hn
url: https://github.com/xlmnxp/qanah
published_at: '2026-03-07T22:36:49'
authors:
- xlmnxp
topics:
- p2p-vpn
- webrtc
- wireguard
- nat-traversal
- mesh-networking
relevance_score: 0.45
run_id: materialize-outputs
language_code: en
---

# Qanah: Peer‑to‑peer VPN over WebRTC with WireGuard configs

## Summary
Qanah is a peer-to-peer VPN tool: it reuses the WireGuard configuration format, but instead of using WireGuard's UDP transport, it carries raw IP packets over WebRTC data channels. Its value lies in enabling devices behind CGNAT, on restricted networks, or unable to open ports to still establish encrypted tunnels and small-scale mesh networks.

## Problem
- Traditional WireGuard relies on direct UDP connectivity; when users are behind **CGNAT**, cannot do port forwarding, lack a public IP, or face upstream network restrictions, deployment and connectivity become difficult.
- Some networks block the WireGuard protocol or outbound UDP, causing conventional VPNs to fail in scenarios such as remote access to home labs, temporary secure links, and internal connectivity for small teams.
- Users often also want to keep using familiar **WireGuard configuration files and key management**, rather than maintaining a new VPN configuration stack and centralized infrastructure.

## Approach
- Qanah reads standard **WireGuard `.conf`** files, extracts interface addresses, private keys, public keys, and `AllowedIPs`, and creates a local **TUN** device accordingly.
- It uses the local **X25519 private key** and the peer's public key to derive a shared key, then derives separate tunnel encryption keys and signaling keys; actual packets are encrypted with **ChaCha20-Poly1305**.
- Unlike traditional WireGuard, it reads **raw IP packets** from the TUN device and forwards them bidirectionally over a **WebRTC data channel** (label `vpn-tunnel`), thereby using **ICE/STUN/TURN** for NAT traversal.
- By default, it exchanges WebRTC offer/answer signaling via **MQTT**, and also supports manual copy-paste signaling; therefore it does not require a centralized VPN server, only a signaling path.
- It supports **mesh networking**: multiple `[Peer]` entries can connect simultaneously; if there is no direct route to the destination, it can use the first connected node as a **single-hop relay**, or disable relaying with `--no-relay`.

## Results
- The text **does not provide formal benchmarks or paper-style quantitative metrics** (such as throughput, latency, success rate, or comparison figures versus WireGuard/OpenVPN/Tailscale).
- The most specific functional result given is that, in an example with **3 peers**, connections can be automatically discovered and established, and the peers can `ping` each other at `10.0.0.1/2/3` and IPv6 `fd00::1/2/3`, indicating support for **IPv4 + IPv6** peer-to-peer/mesh connectivity.
- It claims that remote access behind CGNAT can be achieved via **ICE/STUN** with **no public IP, no port forwarding, and no central VPN server**.
- It claims that when **WireGuard/UDP is blocked** or only more common ports / restrictive egress policies are allowed, tunnels can still be established through **WebRTC over standard ports** plus MQTT signaling.
- It claims support for **single-hop relaying**: when a target peer is not directly connected or reachable, data can be forwarded through another connected peer; this can be useful for small-team mesh networks or site-to-site links over restricted networks.
- The operating prerequisites are explicitly limited to **Linux + TUN support + root/sudo privileges + at least two peers that can access the same STUN server**, so the result is better understood as an engineering implementation and usability demonstration rather than a quantitatively validated performance breakthrough.

## Link
- [https://github.com/xlmnxp/qanah](https://github.com/xlmnxp/qanah)
