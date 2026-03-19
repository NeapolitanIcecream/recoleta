---
source: hn
url: https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/
published_at: '2026-03-04T23:18:51'
authors:
- HardwareLust
topics:
- open-hardware
- esp32
- diy-smartphone
- embedded-systems
- mobile-device
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# Neither Android nor iOS: DIY Smartphone Runs on ESP32

## Summary
This is a DIY 4G smartphone prototype based on the ESP32-S3, aiming to provide more complete ownership and openness over both phone hardware and software. It demonstrates the feasibility of implementing basic smartphone functions such as calling, texting, taking photos, and web browsing on an extremely low-end computing platform.

## Problem
- Existing mainstream smartphones are usually closed ecosystems, making it difficult for users to truly control the hardware, software, and modifiability, which weakens the meaning of “owning” the device.
- Even alternative operating system options (such as mobile Linux) often still run on commercial off-the-shelf hardware, so they cannot solve the problem of trust and openness at the underlying hardware level.
- Therefore, there is a need for a phone solution that is more open, DIY-friendly, and documentable from hardware to software, proving that a fully DIY phone is not just a fantasy.

## Approach
- Use the **ESP32-S3** as the main controller to build a standalone working phone, rather than flashing a third-party system onto existing phone hardware.
- Provide cellular connectivity through the **A7682E Simcom 4G modem**, enabling phone calls and text messaging.
- Integrate an **OV2640 Arducam** camera, a **3.5-inch touchscreen**, and a **3.5 mm headphone jack**, covering core functions including photography, interaction, and audio.
- The current version is an alpha prototype made of stacked layered modules; the next plan is to redesign it into a slimmer **four-layer PCB** and add an **SD card adapter**.
- The creator plans to open-source both the **hardware and software** in the next stage and provide documentation, improving reproducibility and enabling community-driven expansion.

## Results
- The prototype already implements several core phone functions: **4G calling, texting, photography, and web browsing**.
- The hardware configuration is clearly identified: the main controller is **ESP32-S3**, the cellular module is **A7682E**, the camera is **OV2640**, the display is a **3.5-inch touchscreen**, and it retains a **3.5 mm audio jack**.
- The article **does not provide standardized quantitative evaluation results**, such as performance benchmarks, battery life, network throughput, latency, camera quality, or benchmark comparisons with Android/iPhone devices.
- The strongest concrete claim is that the device has already achieved key capabilities close to a basic smartphone on a **non-commercial phone mainboard**, with plans to further reduce its size, add **four-layer PCB + SD card** support, and release the full design as open source.
- The article also explicitly states that its performance is **significantly weaker than flagship phones**, so its main contribution is openness, controllability, and DIY feasibility rather than a performance breakthrough.

## Link
- [https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/](https://hackaday.com/2026/03/04/neither-android-nor-ios-diy-smartphone-runs-on-esp32/)
