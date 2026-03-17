---
source: hn
url: https://github.com/noahra/diz
published_at: '2026-03-13T23:29:38'
authors:
- noahra
topics:
- ssh
- key-exchange
- secure-onboarding
- tls-pinning
- developer-tools
relevance_score: 0.0
run_id: materialize-outputs
---

# Show HN: diz – SSH key exchange in one command each side

## Summary
diz 是一个用于 **SSH 首次密钥交换** 的小工具：双方各运行一条命令、线下共享一个短码，就能建立经认证的 SSH 访问。它聚焦于“能在两台机器上执行命令，但不想手动复制公钥或启用密码认证”的窄场景。

## Problem
- 解决 SSH 首次建立信任时的繁琐问题：传统做法常需手动复制公钥、编辑 `authorized_keys`，流程易出错且不方便。
- 这很重要，因为很多实际场景只需要一次性、快速、安全地把自己的 SSH 公钥放到目标机器上，而不是配置长期复杂方案。
- 它尤其针对：两边都能运行命令、可以通过聊天/语音等带外方式共享短码，但不想处理 70+ 字符公钥粘贴的情况。

## Approach
- 核心机制很简单：目标机运行 `diz --listen`，本地机运行 `diz --connect <code>`，短码里包含安全首次连接所需的信息。
- 这个短码编码了 IP、端口、一次性令牌和 TLS 证书指纹，因此连接一开始就能加密，并通过证书指纹绑定来防 MITM。
- 建立临时认证通道后，`diz` 会自动交换用户公钥、把公钥加入目标机 `authorized_keys`，然后直接进入 shell。
- 设计上它是一次性、短生命周期：每次会话生成一次性证书，使用 128-bit 一次性 token，不保留持续监听器，也不依赖中心服务器/中继。
- 跨网络时，它不自己做 NAT 穿透；建议与 Tailscale、ZeroTier 或 WireGuard 等 VPN 搭配，在同一虚拟网络中按相同方式工作。

## Results
- 文本**没有提供正式实验、基准测试或量化评测结果**，因此没有可报告的准确率、吞吐、时延或对比基线数字。
- 最强的具体功能性声明是：**每侧一条命令** 即可完成 SSH 首次密钥交换并直接进入 shell，相比手动复制公钥/编辑 `authorized_keys` 更简化。
- 安全相关的具体声明包括：使用 **TLS + 证书指纹 pinning**，并在分享码中嵌入指纹；若发生篡改会立即中止连接。
- 会话使用 **一次性 128-bit token**，并且**无持久监听器、无中心服务器/relay**，强调短期、单次使用的首次接入模型。
- 适用性边界也被明确给出：**不适合**高安全生产服务器、无法带外验证分享码的环境、以及双方都处于激进 NAT 且无 VPN 的场景。

## Link
- [https://github.com/noahra/diz](https://github.com/noahra/diz)
