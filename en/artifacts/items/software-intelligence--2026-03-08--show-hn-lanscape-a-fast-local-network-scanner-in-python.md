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
language_code: en
---

# Show HN: LANscape – a fast local network scanner in Python

## Summary
LANscape is a local LAN scanner written in Python, providing a built-in Web UI for discovering devices, open ports, and running services. It emphasizes local deployment and direct LAN access to achieve more reliable scanning results than container-isolated environments.

## Problem
- There is a need for an easy-to-run local network scanning tool that helps users quickly inspect devices, ports, and services on a LAN.
- This matters because home/office network troubleshooting, security auditing, and asset discovery all depend on quickly identifying hosts and services visible within the LAN.
- Constraints in existing runtime environments can affect scan quality, especially Docker network isolation, which interferes with LAN probing methods such as ARP, ICMP, and broadcasts.

## Approach
- The tool discovers devices on the network by combining **ARP, ICMP, and port probing**, and further identifies open ports and running services.
- It provides a built-in **Web UI** (the frontend was recently migrated to React and is stored in a separate repository) so users can view scan results and configuration in the browser.
- Put simply, it sends several common probe requests directly from the local machine to the LAN, then organizes the responses into a displayed list of devices and services.
- It supports multiple run modes and parameters, such as UI port, debug, persistence, logging, and a WebSocket server, but for most users it recommends running locally via `pip install lanscape`.
- MAC address identification depends on ARP lookups, so on some systems administrator privileges may be required to improve result accuracy.

## Results
- The text **does not provide standard paper-style quantitative results**; it does not report datasets, accuracy, recall, scan speed benchmarks, or numerical comparisons with other scanners.
- The strongest concrete capability claim is that it can discover **devices, open ports, running services** and includes a **built-in web UI**.
- The explicit technical claim is that it uses **ARP + ICMP + port probing** for scanning, rather than a single probing mechanism.
- The concrete deployment conclusion is that running in Docker usually requires `--network host`, and this mode **only works on Linux hosts**; in Docker Desktop on Windows/macOS, what is exposed is the VM network rather than the physical LAN.
- The concrete usage recommendation is that most users should use `pip install lanscape` and then run `python -m lanscape`, rather than relying on containerized deployment.

## Link
- [https://github.com/mdennis281/LANscape](https://github.com/mdennis281/LANscape)
