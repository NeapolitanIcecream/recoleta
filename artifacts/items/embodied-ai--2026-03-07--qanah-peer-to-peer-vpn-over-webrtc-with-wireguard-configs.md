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
---

# Qanah: Peer‑to‑peer VPN over WebRTC with WireGuard configs

## Summary
Qanah 是一个点对点 VPN 工具：它复用 WireGuard 风格配置，但不走 WireGuard 的 UDP 传输，而是把 IP 数据包加密后放进 WebRTC 数据通道中传输。其核心价值是在 CGNAT、受限网络或无法开端口的环境下，仍能建立无需中心化 VPN 服务器的加密隧道。

## Problem
- 传统 WireGuard 依赖 UDP 传输，常常要求公网 IP、端口转发，或对上游网络有控制权；在 **CGNAT**、企业网络或受审查网络中，这些条件往往不满足。
- 当 WireGuard 协议或出站 UDP 被封锁时，常规 VPN 很难连通，导致远程访问、站点互联和临时安全连接部署成本高。
- 小型团队或个人场景常不想维护中心化 VPN 服务器，但仍需要多节点互联、基本路由与加密通信能力。

## Approach
- Qanah 读取标准 **WireGuard `.conf`**，提取接口地址、私钥、公钥和 `AllowedIPs`，并据此创建本地 **TUN** 设备，因此用户可以沿用熟悉的 WireGuard 配置方式。
- 它使用本地 **X25519 私钥** 与对端 **公钥**导出共享密钥，再派生出独立的隧道加密密钥与信令密钥；实际数据包使用 **ChaCha20-Poly1305** 加密。
- 与传统 WireGuard 不同，它不直接发送 UDP VPN 包，而是把从 TUN 读出的原始 **IP 包**加密后，通过 **WebRTC data channel**（标签 `vpn-tunnel`）双向转发。
- 为解决 NAT 穿透，它通过 **ICE/STUN/TURN** 建立 WebRTC 连接；默认使用 **MQTT** 自动交换 offer/answer 信令，也支持手工复制粘贴信令。
- 它支持基于配置的 **mesh networking**；如果目标没有直连路由，可将流量封装后经“第一个已连接节点”执行 **单跳 relay**，也可用 `--no-relay` 禁用中继。

## Results
- 文本**没有提供正式基准实验或论文式定量指标**，没有吞吐、时延、成功率或与 WireGuard/OpenVPN/Tailscale 的数值对比。
- 给出的最具体功能性结果是：在 **3 个 peer** 的示例中，节点可自动经 MQTT 发现彼此并建立 WebRTC 直连，随后可互相 `ping` IPv4 地址 `10.0.0.1/2/3` 与 IPv6 地址 `fd00::1/2/3`。
- 论文/项目声称可在 **CGNAT** 后远程访问家庭实验室、NAS 或开发机，且**无需公网 IP、无需端口转发、无需中心 VPN 服务器**；这是一项部署层面的实用突破，但未附数值验证。
- 它声称在 **WireGuard/UDP 被阻断** 或仅允许标准端口、HTTPS/MQTT 出站的网络中仍可工作，因为隧道承载改为 **WebRTC/ICE**；但没有给出成功率或覆盖网络环境统计。
- 它支持 **多 peer mesh** 与 **1 跳 relay**，意味着在某个目标离线或无直连时，流量仍可能通过中间节点到达；不过没有提供路由开销或中继性能数据。
- 适用条件也较明确：当前需要 **Linux**、**TUN 设备支持**、**root/sudo** 权限，以及两端至少能访问一个共同 **STUN** 服务器。

## Link
- [https://github.com/xlmnxp/qanah](https://github.com/xlmnxp/qanah)
