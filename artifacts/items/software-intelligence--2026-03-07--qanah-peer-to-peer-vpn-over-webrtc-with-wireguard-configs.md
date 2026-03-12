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
---

# Qanah: Peer‑to‑peer VPN over WebRTC with WireGuard configs

## Summary
Qanah 是一个点对点 VPN 工具：它复用 WireGuard 配置格式，但不走 WireGuard 的 UDP 传输，而是把原始 IP 包放进 WebRTC 数据通道中传输。其价值在于让处于 CGNAT、受限网络或无法开端口的设备，也能建立加密隧道和小规模 mesh 网络。

## Problem
- 传统 WireGuard 依赖 UDP 直连；当用户位于 **CGNAT**、无法做端口转发、没有公网 IP，或上游网络受限时，部署和连通性会变得困难。
- 一些网络会阻断 WireGuard 协议或出站 UDP，使得常规 VPN 在家庭实验室远程访问、临时安全连接、小团队内网互通等场景下失效。
- 用户往往还希望继续使用熟悉的 **WireGuard 配置文件与密钥体系**，而不是重新维护一套新的 VPN 配置与中心化基础设施。

## Approach
- Qanah 读取标准 **WireGuard `.conf`**，提取接口地址、私钥、公钥和 `AllowedIPs`，并据此创建本地 **TUN** 设备。
- 它使用本地 **X25519 私钥** 与对端公钥导出共享密钥，再派生出独立的隧道加密密钥与信令密钥；实际数据包用 **ChaCha20-Poly1305** 加密。
- 与传统 WireGuard 不同，它把 **原始 IP 包** 从 TUN 设备读出后，通过 **WebRTC data channel**（标签 `vpn-tunnel`）双向转发，从而利用 **ICE/STUN/TURN** 做 NAT 穿透。
- 默认通过 **MQTT** 交换 WebRTC 的 offer/answer 信令，也支持手工 copy-paste 信令；因此不需要中心化 VPN 服务器，只需一个信令路径。
- 支持 **mesh networking**：多个 `[Peer]` 可同时连接；若没有到目标的直连路由，可通过首个已连接节点做 **单跳 relay**，也可用 `--no-relay` 禁用中继。

## Results
- 文本**没有提供正式基准测试或论文式量化指标**（如吞吐、时延、成功率、与 WireGuard/OpenVPN/Tailscale 的对比数字）。
- 给出的最具体功能性结果是：在 **3 个 peer** 的示例中，可自动发现并建立连接，并能互相 `ping`：`10.0.0.1/2/3` 以及 IPv6 `fd00::1/2/3`，说明支持 **IPv4 + IPv6** 的点对点/mesh 连通。
- 声称可在 **无需公网 IP、无需端口转发、无需中心 VPN 服务器** 的情况下，通过 **ICE/STUN** 在 CGNAT 后实现远程访问。
- 声称在 **WireGuard/UDP 被屏蔽** 或仅允许较常见端口/受限出口策略时，仍可通过 **WebRTC over standard ports** 与 MQTT 信令建立隧道。
- 声称支持 **单跳中继**：当目标 peer 不直连或不可达时，数据可经另一已连接 peer 转发；该能力可用于小团队 mesh 或受限网络下的站点互联。
- 运行前提被明确限定为 **Linux + TUN 支持 + root/sudo 权限 + 至少两个能访问同一 STUN 服务器的对等端**，因此其成果更像工程实现与可用性展示，而非经过量化验证的性能突破。

## Link
- [https://github.com/xlmnxp/qanah](https://github.com/xlmnxp/qanah)
