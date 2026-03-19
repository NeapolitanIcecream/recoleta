---
source: hn
url: https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/
published_at: '2026-03-04T23:18:51'
authors:
- HardwareLust
topics:
- open-hardware
- diy-smartphone
- esp32
- 4g-modem
- embedded-systems
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Neither Android nor iOS: DIY Smartphone Runs on ESP32

## Summary
This article introduces a DIY 4G smartphone prototype based on the ESP32-S3, emphasizing the user's complete control over both hardware and software as well as future open-source plans. It is not an academic paper, but rather a hacker/DIY-oriented open hardware project showcase.

## Problem
- Most existing smartphones are built on closed, restrictive commercial hardware and software ecosystems, making it difficult for users to truly "own" and control their devices.
- Even when replacing the operating system (such as with Linux distributions), they still usually run on commercial phone hardware that may carry backdoor risks.
- Therefore, there is a need for a phone solution that is independently controllable, modifiable, and open-source from hardware to software, which matters for privacy, repairability, and technological autonomy.

## Approach
- The core method is simple: use an **ESP32-S3** as the main controller and assemble a modular 4G phone from scratch, rather than relying on an off-the-shelf smartphone SoC platform.
- The communications portion uses an **A7682E simcom 4G modem** to provide basic phone functions such as calling and texting.
- The multimedia and interaction portion adds an **OV2640 Arducam** camera, a **3.5-inch touchscreen**, and retains a **3.5 mm audio jack**.
- The current version is an alpha prototype made by stacking multiple modules; the follow-up plan is to make it into a slimmer **four-layer PCB** and integrate an **SD card adapter**.
- The author promises to **open-source both the hardware and software design** after the next version is completed, along with documentation.

## Results
- The prototype already provides clear phone capabilities: **4G connectivity, phone calls, text messaging, photography, and web browsing**.
- The hardware configuration includes an **ESP32-S3** main controller, **A7682E** 4G module, **OV2640** camera, **3.5\"** touchscreen, and **3.5 mm** headphone jack.
- The article does not provide standardized quantitative evaluation results; it **does not** report specific numbers such as benchmark performance, battery life, latency, throughput, or camera quality.
- The strongest concrete claim is that the device is already a working **alpha DIY 4G smartphone**, with plans to evolve into a slimmer open-source four-layer PCB design.
- The text also explicitly acknowledges that its performance is **significantly weaker than flagship phones**, but its advantages lie in openness, controllability, and the self-built hardware approach.

## Link
- [https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/](https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/)
