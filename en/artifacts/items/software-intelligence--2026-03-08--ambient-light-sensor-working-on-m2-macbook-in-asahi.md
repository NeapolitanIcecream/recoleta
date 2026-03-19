---
source: hn
url: https://github.com/AsahiLinux/docs/issues/248
published_at: '2026-03-08T23:09:58'
authors:
- cromka
topics:
- asahi-linux
- ambient-light-sensor
- macbook-m2
- linux-driver
- auto-brightness
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Ambient Light Sensor working on M2 MacBook in Asahi

## Summary
This is an implementation note for the Asahi Linux community showing how the ambient light sensor on M2 MacBooks can be made to work under Linux, and how the auto-brightness pipeline can be completed. Its value lies in turning a sensor on Apple hardware that depends on proprietary calibration data into a feature that is practically usable on Asahi Fedora.

## Problem
- The **ambient light sensor (ALS) on M2 MacBooks** needs to work properly on Asahi Linux; otherwise, user-experience features such as automatic brightness cannot be realized.
- The sensor depends on **factory calibration data from macOS**; without this firmware, the driver may still load, but the sensor returns **0 lux**, making it effectively unusable.
- KDE Plasma 6.6.0 on Asahi **does not have built-in ALS auto-brightness support**, so even if the lower layers can read light values, the desktop side still lacks full integration.

## Approach
- Enable/use the **AOP ALS driver** in Asahi's fairydust kernel branch (`CONFIG_IIO_AOP_SENSOR_ALS=m`) as the hardware access foundation.
- Export the `ioreg` XML from macOS, then use a script to extract the calibration blob from `CalibrationData` in the `AppleSPUVD6286` node, generate `aop-als-cal.bin`, and place it in the Linux firmware directory.
- A companion kernel patch (PR #457) makes the **calibration firmware optional**, allowing the driver to complete probe even when the firmware is missing, improving deployability and debugging; however, without calibration, readings will still be 0 lux.
- A lightweight auto-brightness daemon was added on the desktop side: it reads lux from `iio-sensor-proxy` over **D-Bus**, then calls KDE's `ScreenBrightness` interface to adjust brightness smoothly.
- The daemon uses **rolling average + hysteresis** as a simple way to suppress brightness jitter and frequent flicker.

## Results
- On **MacBook Air 15" M2 (J415)** with a **VD6286** sensor, **Asahi Fedora 42**, **KDE Plasma 6.6.0**, and **kernel 6.18.10-402.asahi.fairydust.fc42.aarch64+16k**, the author states the ALS is "**fully working**."
- A key failure/success condition is stated clearly: **without the calibration firmware, the sensor reports 0 lux**; after adding calibration data extracted from macOS, it can provide normal lux readings.
- For desktop experience, the author implemented a working **auto-brightness daemon** and reduced flicker through smooth adjustment, rolling average, and hysteresis, but **did not provide quantitative metrics** such as brightness stability, response time, or error.
- Compatibility claim: beyond the tested **15" M2 Air**, the author believes it **should also work** on other M2 models with **VD6286**, such as the **13" MacBook Air** and **13" MacBook Pro**, but the post does not provide additional measured data or comparison baselines.

## Link
- [https://github.com/AsahiLinux/docs/issues/248](https://github.com/AsahiLinux/docs/issues/248)
