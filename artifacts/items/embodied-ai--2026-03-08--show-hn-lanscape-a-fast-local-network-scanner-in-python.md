---
source: hn
url: https://github.com/mdennis281/LANscape
published_at: '2026-03-08T23:02:35'
authors:
- mdennis281
topics:
- network-scanner
- local-network
- port-scanning
- web-ui
- python
- react
relevance_score: 0.0
run_id: materialize-outputs
---

# Show HN: LANscape – a fast local network scanner in Python

## Summary
LANscape 是一个用 Python 编写的本地网络扫描工具，带有内置 Web UI，用于发现局域网中的设备、开放端口和运行中的服务。它更像是一个实用型开源工具说明，而不是一篇研究论文，因此技术贡献和实验结论都较有限。

## Problem
- 解决的问题是：如何在本地局域网中快速发现在线设备、开放端口和服务，方便网络排查、资产盘点和基础安全检查。
- 这很重要，因为家庭、办公和实验网络里常常缺少一个轻量、易用、可视化的本地扫描工具。
- 文中还指出了实际部署痛点：Docker 的网络隔离会妨碍 ARP/ICMP/广播扫描，导致很多环境下扫描效果受限。

## Approach
- 核心方法很直接：组合使用 **ARP、ICMP 和端口探测** 来发现局域网设备，并收集 MAC 地址、开放端口和服务信息。
- 工具提供 **内置 Web UI**，最近前端被迁移为 **React**，用于展示扫描结果和配置扫描参数。
- 通过命令行启动和配置，例如设置 UI 端口、调试模式、持久化、日志文件、日志级别和 WebSocket 服务。
- 对 MAC 地址识别依赖 **ARP lookup**，并提醒某些系统上可能需要管理员权限才能得到更准确结果。
- 对容器部署的处理也很务实：明确说明大多数用户更适合直接 `pip install lanscape`，而不是 Docker。

## Results
- 文本**没有提供正式的定量实验结果**，没有报告扫描速度、准确率、召回率、误报率或与基线工具的对比数字。
- 最具体的能力声明是：工具可以“发现设备、开放端口和运行中的服务”。
- 部署层面的明确结论是：Docker 方式通常不推荐；若要在 Linux 上使用 Docker，需要 `--network host`，而 Windows/macOS 上该模式暴露的是 VM 网络而非物理 LAN。
- 运行方式给出了若干具体接口/参数示例，如 `python -m lanscape --ui-port 8080`、`--ws-port 9000`、`--persistent`、`--loglevel WARNING`，但这些是使用说明，不是性能结果。

## Link
- [https://github.com/mdennis281/LANscape](https://github.com/mdennis281/LANscape)
