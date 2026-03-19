---
source: hn
url: https://github.com/noahra/diz
published_at: '2026-03-13T23:29:38'
authors:
- noahra
topics:
- ssh-key-exchange
- secure-onboarding
- developer-tooling
- remote-access
- tls-pinning
relevance_score: 0.52
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: diz – SSH key exchange in one command each side

## Summary
diz 是一个面向 SSH 初次接入的轻量工具：双方各运行一条命令并共享一个短码，即可安全地完成 SSH 公钥交换并直接登录。它解决了手工复制公钥、编辑 `authorized_keys` 和临时启用密码认证的繁琐流程。

## Problem
- 要解决的问题是：两台机器之间首次建立 SSH 信任时，传统流程需要手动复制 70+ 字符公钥、编辑 `authorized_keys` 或依赖密码登录，操作繁琐且容易出错。
- 这很重要，因为开发者、运维人员和远程协作场景中经常需要快速、安全地建立一次性 SSH 访问，而现有方式在可用性和安全性之间往往需要妥协。
- 该工具专门面向“双方都能执行命令、且能通过带外渠道共享短码”的窄场景，不适用于高安全生产环境或无法带外验证短码的场合。

## Approach
- 核心机制非常简单：目标机器运行 `diz --listen`，连接方运行 `diz --connect <code>`，短码中包含建立安全首次连接所需的关键信息。
- 这个短码编码了 IP、端口、一次性 token 和 TLS 证书指纹；连接方据此发起一次临时认证通道，并从一开始就做证书指纹绑定，防止中间人攻击。
- 建立通道后，diz 会自动交换 SSH 公钥，把连接方的公钥加入目标机器的 `authorized_keys`，随后直接进入 shell，无需手工复制文件或修改配置。
- 设计上它是短生命周期、单次使用：每次会话生成一次性证书、使用 128-bit 一次性 token、没有持久监听器，也不依赖中心化服务器或中继。
- 网络层面默认使用本地网络 IP；若跨地域，可配合 Tailscale、ZeroTier 或 WireGuard 等 VPN，在虚拟局域网中以同样方式工作。

## Results
- 文本未提供标准论文式定量实验结果，没有给出数据集、基准方法、成功率、时延或性能指标，因此无法报告严格的数值对比。
- 最强的具体声明是：双方“各一条命令”即可完成 SSH 首次授权，替代手工复制 70+ 字符公钥和手动编辑 `authorized_keys`。
- 安全性声明包括：使用 TLS + 证书指纹绑定；每个会话生成一次性证书；短码内含一次性 128-bit token；若指纹不匹配则立即中止连接。
- 部署与运行声明包括：无需中心服务器/中继、无持久监听器；在同一局域网可开箱即用；跨网络场景下可借助 Tailscale、ZeroTier、WireGuard 等 VPN 保持相同使用方式。

## Link
- [https://github.com/noahra/diz](https://github.com/noahra/diz)
