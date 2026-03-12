---
source: hn
url: https://github.com/mdennis281/LANscape
published_at: '2026-03-08T23:02:35'
authors:
- mdennis281
topics:
- network-scanner
- lan-discovery
- port-scanning
- web-ui
- python-tool
relevance_score: 0.16
run_id: materialize-outputs
---

# Show HN: LANscape – a fast local network scanner in Python

## Summary
LANscape 是一个用 Python 编写的本地局域网扫描器，提供内置 Web UI，用于发现设备、开放端口和运行中的服务。它强调本机部署与直接 LAN 访问，以获得比容器隔离环境更可靠的扫描结果。

## Problem
- 需要一种易于运行的本地网络扫描工具，帮助用户快速查看局域网中的设备、端口和服务。
- 这很重要，因为家庭/办公网络排障、安全审计和资产发现都依赖对 LAN 内可见主机与服务的快速识别。
- 现有运行环境限制会影响扫描效果，尤其是 Docker 网络隔离会妨碍 ARP、ICMP 和广播等局域网探测方式。

## Approach
- 工具通过组合 **ARP、ICMP 和端口探测** 来发现网络中的设备，并进一步识别开放端口与运行服务。
- 提供内置 **Web UI**（前端近期迁移为 React，存放在独立仓库）以便用户在浏览器中查看扫描结果和配置。
- 以最简单的话说：它从本机直接向局域网发出几类常见探测请求，再把响应整理成设备和服务列表展示出来。
- 提供多种运行模式与参数，如 UI 端口、调试、持久化、日志和 WebSocket 服务器，但推荐多数用户直接通过 `pip install lanscape` 本机运行。
- 对 MAC 地址识别依赖 ARP 查询，因此某些系统上可能需要管理员权限来提高结果准确性。

## Results
- 文本**没有提供标准论文式定量结果**，没有给出数据集、准确率、召回率、扫描速度基准或与其他扫描器的数值对比。
- 最强的具体能力声明是：可发现 **devices、open ports、running services**，并带有 **built-in web UI**。
- 明确的技术主张是使用 **ARP + ICMP + port probing** 进行扫描，而不是单一探测机制。
- 部署层面的具体结论是：Docker 运行通常需要 `--network host`，且该模式**仅在 Linux 主机上有效**；在 Windows/macOS 的 Docker Desktop 中，暴露的是 VM 网络而非物理 LAN。
- 使用层面的具体建议是：多数用户采用 `pip install lanscape` 后执行 `python -m lanscape`，而不是依赖容器化部署。

## Link
- [https://github.com/mdennis281/LANscape](https://github.com/mdennis281/LANscape)
