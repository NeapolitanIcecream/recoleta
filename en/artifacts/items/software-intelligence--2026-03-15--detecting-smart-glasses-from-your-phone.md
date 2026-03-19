---
source: hn
url: https://nearby-glasses-alert.pages.dev/
published_at: '2026-03-15T23:21:21'
authors:
- modexapps
topics:
- ble-detection
- smart-glasses
- mobile-privacy
- background-scanning
relevance_score: 0.2
run_id: materialize-outputs
language_code: en
---

# Detecting Smart Glasses from your phone

## Summary
This is an app that uses background Bluetooth Low Energy scanning on a phone to detect nearby camera-equipped smart glasses, aiming to provide real-time alerts without uploading data to the cloud. Its core value is helping users identify smart glasses that look ordinary but may be recording, thereby improving privacy awareness and environmental transparency.

## Problem
- Camera-equipped smart glasses (such as Meta Ray-Ban and Snap Spectacles) look similar to ordinary glasses, so people nearby often cannot quickly tell that they may be being recorded.
- Existing mobile operating systems are quite restrictive about background Bluetooth scanning, battery optimization, Doze mode, and scan recovery after reboot, making continuous and reliable detection difficult to achieve.
- Privacy-protection tools that rely on the cloud, account systems, or persistent identifier storage may instead introduce new risks of data leakage and tracking.

## Approach
- Use continuous BLE scanning on the phone to keep looking in the background for Bluetooth signals associated with smart glasses, maintaining detection capability as much as possible even if the app is closed, the screen is off, or the device has restarted.
- Detection rules are based on a combination of multiple Bluetooth features: manufacturer BLE IDs, service UUIDs, device-name keywords, and RSSI signal strength, rather than relying on a single feature.
- These features are combined into a confidence score, and notifications are triggered only when a "meaningful match" is reached, balancing false positives and missed detections.
- Provides three detection modes — Strict, Balanced, and Relaxed — and uses a per-device cooldown period (20 seconds to 5 minutes) to reduce repeated alerts.
- The privacy design emphasizes local processing: scanning and decision-making are done on the phone, raw Bluetooth identifiers are not stored and are only one-way hashed; networking is used only for OTA detection-rule updates.

## Results
- The text does not provide paper-style benchmark tests, public-dataset results, or quantitative comparisons with other methods, so there are no verifiable numerical results such as precision/recall/F1.
- It claims to support continuous background BLE scanning with "one tap" and to "notify immediately" when camera-capable smart glasses are detected, even with the screen off.
- It claims to bypass Android's aggressive power-saving policies through hardware-level BLE scan filters, allowing detection even when other apps go silent; however, it provides no numbers for power consumption, success rate, or device coverage.
- It claims to estimate distance based on a corrected indoor path-loss formula, ranging from under 1 meter to 200 meters; however, it does not report distance-estimation error or validation experiments.
- It provides a configurable per-device alert cooldown from 20 seconds to 5 minutes, and automatically resumes scanning after reboot, emphasizing that "protection is never accidentally off"; however, it includes no stability or long-term runtime statistics.

## Link
- [https://nearby-glasses-alert.pages.dev/](https://nearby-glasses-alert.pages.dev/)
