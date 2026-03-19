---
source: hn
url: https://github.com/AsahiLinux/docs/issues/248
published_at: '2026-03-08T23:09:58'
authors:
- cromka
topics:
- linux-driver
- ambient-light-sensor
- asahi-linux
- macbook-m2
- auto-brightness
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Ambient Light Sensor working on M2 MacBook in Asahi

## Summary
This is an implementation note about enabling the ambient light sensor (ALS) on M2 MacBooks in Asahi Linux, rather than a traditional academic paper. It addresses the problem that M2 models on Linux cannot properly read ambient light and drive automatic brightness, and provides a complete solution covering the driver, calibration extraction, and a user-space daemon.

## Problem
- The problem being solved is that the VD6286 ambient light sensor on M2 MacBooks does not fully work by default on Asahi Linux; without factory calibration data, it continuously reports **0 lux**.
- This matters because without ALS, the system cannot automatically adjust screen brightness based on ambient light, affecting usability, power experience, and desktop integration.
- In addition, KDE Plasma 6.6.0 on Asahi does not have ready-made ALS auto-brightness support, so an extra user-space component is needed to connect the whole chain.

## Approach
- The core method is simple: first make the kernel driver recognize and load the ALS, then extract Apple factory calibration data from macOS for Linux to use.
- The specific mechanism is to parse the `CalibrationData` inside the `AppleSPUVD6286` node from a macOS `ioreg` export, generate the `aop-als-cal.bin` firmware file, and place it under `/lib/firmware/apple/` for the driver to read.
- Together with a kernel patch (PR #457), the driver is allowed to probe even without the calibration firmware, instead of failing completely because the firmware is missing; however, without calibration the reading will still be 0 lux.
- In user space, the author wrote a lightweight auto-brightness daemon: it reads lux from `iio-sensor-proxy` over D-Bus, then smoothly adjusts brightness through KDE's `ScreenBrightness` API.
- To avoid screen brightness bouncing back and forth, the daemon uses a rolling average and hysteresis to suppress flicker.

## Results
- The author claims to have **fully working VD6286 ALS** on a **MacBook Air 15" M2 (J415)**, with the system environment being **Asahi Fedora 42 + KDE Plasma 6.6.0**.
- The kernel version used is **6.18.10-402.asahi.fairydust.fc42.aarch64+16k**, and it depends on the config option **`CONFIG_IIO_AOP_SENSOR_ALS=m`**.
- The clearest quantitative observation given is that **without factory calibration data, the sensor output is 0 lux**; after adding the extracted calibration file, it works normally.
- A kernel patch **PR #457** is provided, whose purpose is to make the calibration firmware “optional,” so the driver can still probe successfully even when the file is missing.
- The explicitly validated hardware is listed as the **15-inch M2 Air**, and it is claimed that it **should also apply** to other M2 machines with **VD6286**, such as the **13-inch MacBook Air** and **13-inch MacBook Pro**.
- No standardized benchmarks, error metrics, latency data, or quantitative comparisons with other methods are provided, so the main breakthrough is practical engineering deployment: moving from “0 lux/unusable” to “fully usable + end-to-end auto-brightness support.”

## Link
- [https://github.com/AsahiLinux/docs/issues/248](https://github.com/AsahiLinux/docs/issues/248)
