---
source: hn
url: https://interconnected.org/home/2026/05/20/resident
published_at: '2026-05-23T23:41:37'
authors:
- bertwagner
topics:
- ai-authored-code
- firmware-sandbox
- esp32
- embedded-agents
- human-ai-interaction
- edge-software
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)

## Summary
Resident lets AI agents and users hot-load Lua apps onto ESP32 devices through a sandbox, without compiling or flashing firmware. The key claim is that AI should write small device apps that run locally, rather than sit inside the live event loop for physical interactions.

## Problem
- Physical device interfaces need fast local responses; the author cites 150 ms as the threshold for an interaction to feel instant.
- Cloud LLM calls add network latency, and even faster edge inference still needs cloud-hosted personal context such as memory, Gmail, or Wikipedia.
- Letting AI write full firmware is risky because firmware can control hardware, the network stack, and other low-level device capabilities.

## Approach
- Resident adds an embedded Lua runtime to ESP32 devices.
- Device developers expose selected hardware functions as driver APIs, such as button events and display writes, while sandboxed apps cannot access unrestricted capabilities such as the network stack.
- Apps can be pushed over Wi-Fi through a websocket and run immediately in the sandbox, with no compile step and no firmware flashing.
- The release includes Claude skills that create, validate, and push apps to compatible devices, plus examples and a browser simulator for an M5StickS3-style device.
- Resident uses Courier for local inter-device messaging, including UDP multicast when internet connectivity drops.

## Results
- The excerpt reports no benchmark results for Resident and gives no measured app-load latency, memory use, safety test pass rate, or device compatibility count.
- Resident is released as alpha v0.5.0 under the MIT license.
- The authors claim they use Resident for all product prototyping at Inanimate.
- The library targets ESP32 devices and is shown with M5StickS3 hardware, which includes an ESP32, screen, battery, buttons, buzzer, and IMU.
- The strongest concrete capability claim is hot loading: app code can arrive over a websocket and run immediately in the on-device sandbox without recompiling or reflashing firmware.
- A cited motivation point says Taalas delivers 17k tokens per second per user on Llama 3.1 8B, but that is external hardware performance, not a Resident result.

## Link
- [https://interconnected.org/home/2026/05/20/resident](https://interconnected.org/home/2026/05/20/resident)
