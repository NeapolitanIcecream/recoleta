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
language_code: en
---

# Show HN: LANscape – a fast local network scanner in Python

## Summary
LANscape is a local network scanning tool written in Python with a built-in Web UI for discovering devices, open ports, and running services on a LAN. It is more like documentation for a practical open-source utility than a research paper, so its technical contributions and experimental conclusions are quite limited.

## Problem
- The problem it addresses is how to quickly discover online devices, open ports, and services on a local LAN, making network troubleshooting, asset inventory, and basic security checks easier.
- This matters because home, office, and lab networks often lack a lightweight, easy-to-use, visual local scanning tool.
- The text also points out a real deployment pain point: Docker's network isolation interferes with ARP/ICMP/broadcast scanning, which limits scanning effectiveness in many environments.

## Approach
- The core method is straightforward: it combines **ARP, ICMP, and port probing** to discover LAN devices and collect MAC addresses, open ports, and service information.
- The tool provides a **built-in Web UI**; the frontend was recently migrated to **React** to display scan results and configure scan parameters.
- It can be started and configured through the command line, for example by setting the UI port, debug mode, persistence, log file, log level, and WebSocket service.
- MAC address identification relies on **ARP lookup**, and it notes that administrator privileges may be required on some systems to obtain more accurate results.
- Its handling of container deployment is also practical: it explicitly says that for most users, directly using `pip install lanscape` is more suitable than Docker.

## Results
- The text **does not provide formal quantitative experimental results**; it does not report scan speed, accuracy, recall, false positive rate, or comparison numbers against baseline tools.
- The most specific capability claim is that the tool can “discover devices, open ports, and running services.”
- A clear deployment conclusion is that the Docker approach is generally not recommended; to use Docker on Linux, `--network host` is required, while on Windows/macOS this mode exposes the VM network rather than the physical LAN.
- Several concrete interface/parameter examples are given for running it, such as `python -m lanscape --ui-port 8080`, `--ws-port 9000`, `--persistent`, and `--loglevel WARNING`, but these are usage instructions, not performance results.

## Link
- [https://github.com/mdennis281/LANscape](https://github.com/mdennis281/LANscape)
