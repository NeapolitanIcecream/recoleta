---
source: hn
url: https://nearby-glasses-alert.pages.dev/
published_at: '2026-03-15T23:21:21'
authors:
- modexapps
topics:
- ble-detection
- smart-glasses
- privacy-preserving
- mobile-app
- background-scanning
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Detecting Smart Glasses from your phone

## Summary
This is not an academic paper, but a consumer-facing mobile app description page. It proposes using continuous BLE scanning on a phone to detect nearby camera-equipped smart glasses and provide real-time alerts in a privacy-preserving, on-device manner.

## Problem
- Problem addressed: Smart glasses such as Meta Ray-Ban and Snap Spectacles look similar to ordinary glasses, but may carry cameras, making it hard for bystanders to notice them in time.
- Why it matters: If a phone can detect such devices in real time, users can receive earlier privacy-risk warnings without needing dedicated hardware or cloud services.
- The challenge is that mobile operating systems restrict background scanning and power consumption, while BLE advertising signals are noisy and prone to false positives or missed detections.

## Approach
- The core mechanism is simple: the phone continuously performs BLE scans, matches manufacturer BLE IDs, service UUIDs, and device-name keywords, and immediately notifies the user when suspected smart glasses are found.
- To reduce false positives, the system combines manufacturer IDs, service UUIDs, RSSI, and name keywords into a confidence score, and alerts only on “meaningful matches.”
- To improve background reliability, the app claims to use hardware-level BLE scan filters to bypass Android’s aggressive battery optimization, and supports Doze, background operation, and automatic scan recovery after reboot.
- To improve usability, it offers three precision-recall tradeoff modes—Strict/Balanced/Relaxed—plus per-device cooldown settings (20 seconds to 5 minutes) and RSSI-based distance estimation.
- To protect privacy, all detection is performed locally, raw Bluetooth identifiers are not stored and are only one-way hashed; network access is used only for OTA detection-rule updates.

## Results
- The text **does not provide formal experiments, datasets, baselines, or quantitative evaluation results**, so it is not possible to verify detection accuracy, recall, false-positive rate, power consumption, or background persistence.
- The most specific functional claims include: continuous background scanning; immediate notifications even when the screen is off; continued operation through Android Doze and after reboot; and per-device alert cooldowns of 20s–5min.
- The quantitative distance-related claim is: distance is estimated using a corrected indoor path-loss formula, ranging from “sub-1m to 200m”; however, no error metrics, test environments, or comparison baselines are provided.
- Concrete product details include: price $1.99, support for Android and iOS, no account, no cloud analytics, and internet use only for rule updates.
- Because reproducible experimental results are missing, claims such as “detects when other apps go silent” and “hardware-level filters bypass optimizer” currently read more like engineering assertions than validated research conclusions.

## Link
- [https://nearby-glasses-alert.pages.dev/](https://nearby-glasses-alert.pages.dev/)
